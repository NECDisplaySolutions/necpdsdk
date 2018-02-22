"""opcode_decoding.py - Tools for working with opcodes and opcode values
"""
# Reads and parses a text file containing a list of opcodes and their
# textual "nice names". For opcodes that have specific / discrete value
# settings, the values and textual "nice names" for each are included.
# Once the file is parsed, the resulting dictionaries can be accessed
# using the included helper functions.
#
# Copyright (C) 2016-18 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.
#

import os

opcode_to_name_dict = dict()
opcode_values_to_name_dict = dict()


def reverse_dict(d):
    return dict(list(zip(list(d.values()), list(d.keys()))))


def load_opcode_dict():
    """
    Opens and parses a special text file that contains a list of opcodes and their textual "nice names".
    :return:
    """
    global opcode_to_name_dict
    global opcode_values_to_name_dict
    opcode_to_name_dict.clear()
    opcode_values_to_name_dict.clear()
    location = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(location, "controls.txt"), 'r') as f:
        for line in f:
            if line[0] == "#":  # comment line
                # print("Comment:", line)
                continue
            words = line.rstrip('\n').split(',')  # comma delimited. Remove trailing \n
            if len(words) >= 3:  # minimal validation
                try:
                    opcode = int(words[0], 16)  # convert opcode from hex
                    name = words[1][1:-1]   # strip out the quotes
                    opcode_to_name_dict[opcode] = name  # add the opcode name to the dictionary
                    if int(words[2]) == 1:  # this opcode is enumerated (has specific named values)
                        offset = 3
                        vcp_values = dict()
                        while offset+1 < len(words):  # read the opcode's pairs of int values and value text
                            vcp_values[int(words[offset])] = words[offset+1][1:-1]
                            offset += 2
                        opcode_values_to_name_dict[opcode] = vcp_values
                except ValueError:
                    print ("convert error")
    assert len(opcode_to_name_dict) > 0
    assert len(opcode_values_to_name_dict) > 0
    return


def opcode_to_nice_name(opcode):
    """
    Given a numerical opcode it returns the text nice name (if exists)

    Use this to lookup the textual name for an opcode.
    e.g. 0x0060 -> "Input"

    :param opcode: a numerical value for the opcode
    :return: the text "nice name" of the opcode (if exists)
    """
    assert 0x0000 <= opcode <= 0xffff
    assert len(opcode_to_name_dict)  # forgot to load_opcode_dict
    if opcode in opcode_to_name_dict:
        return opcode_to_name_dict[opcode]
    return


def nice_name_to_opcode(name):
    """
    Given a text nice name it returns a numerical opcode (if exists)
    Note: string must be an exact match (case sensitive)

    Use this to lookup the opcode from the textual name of an opcode.
    e.g. "Input" -> 0x0060

    :param name: the text "nice name" of the opcode to lookup
    :return: a numerical value for the opcode (if exists)
    """
    assert len(opcode_to_name_dict)  # forgot to load_opcode_dict
    name_to_opcode_dict = reverse_dict(opcode_to_name_dict)
    if name in name_to_opcode_dict:
        return name_to_opcode_dict[name]
    return


def opcode_value_to_nice_value_name(opcode, value):
    """
    Given a numerical opcode and a value it returns the text nice name of the value (if exists)

    Use this to lookup the nice name for the particular value of an opcode
    e.g. opcode 0x0060 (Input) with value 1 -> "VGA"

    :param opcode: a numerical value for the opcode
    :param value: a numerical value of the opcode value
    :return: the text "nice name" of the opcode value (if exists)
    """
    assert len(opcode_values_to_name_dict)  # forgot to load_opcode_dict
    assert 0x0000 <= opcode <= 0xffff
    assert 0x0000 <= value <= 0xffff
    if opcode in opcode_values_to_name_dict:
        if value in opcode_values_to_name_dict[opcode]:
            return opcode_values_to_name_dict[opcode][value]
    return


def opcode_nice_value_name_to_value(opcode, nice_value_name):
    """
    Given a numerical opcode and a string with the nice name of the value,
      it returns the value (if exists)
    Note: "nice_value_name" string must be an exact match (case sensitive)

    Use this to lookup the value for a particular opcode given the nice name of the value
    e.g. opcode 0x0060 (Input) with "VGA" -> value 1

    :param opcode: a numerical value for the opcode
    :param nice_value_name: the text "nice name" of the opcode value
    :return: a numerical value for the opcode value (if exists)
    """
    assert len(opcode_values_to_name_dict)  # forgot to load_opcode_dict
    assert 0x0000 <= opcode <= 0xffff
    if opcode in opcode_values_to_name_dict:
        name_dict = reverse_dict(opcode_values_to_name_dict[opcode])
        if nice_value_name in name_dict:
            return name_dict[nice_value_name]
    return


def get_opcode_list():
    """
    Use this to get a sorted numerical list of all of the known opcodes

    :return: A numerical list of all of the known opcodes
    """
    assert len(opcode_to_name_dict)  # forgot to load_opcode_dict
    keys = list(opcode_to_name_dict.keys())
    keys.sort()
    return keys


def get_opcode_nice_value_name_list(opcode):
    """
    Given a numerical opcode it returns a list of known opcode value

    Use this to get a list of the known numerical values for a particular opcode.
    e.g. opcode 0x0060 (Input) -> ['VGA', 'RGB/HV',...]

    :param opcode: a numerical value for the opcode
    :return: a list of known opcode values (if exists)
    """
    assert len(opcode_values_to_name_dict)  # forgot to load_opcode_dict
    assert 0x0000 <= opcode <= 0xffff
    if opcode in opcode_values_to_name_dict:
        return list(opcode_values_to_name_dict[opcode].values())
    return


def get_opcode_value_list(opcode):
    """
    Given a numerical opcode it returns a list of known text nice name values for the value

    Use this to get a list of the known text nice names of values for a particular opcode.
    e.g. opcode 0x0060 (Input) -> [1, 2,...]

    :param opcode: a numerical value for the opcode
    :return: a list of known text nice name values for the value (if exists)
    """
    assert len(opcode_values_to_name_dict)  # forgot to load_opcode_dict
    assert 0x0000 <= opcode <= 0xffff
    if opcode in opcode_values_to_name_dict:
        return list(opcode_values_to_name_dict[opcode].keys())
    return


def get_opcode_value_dict(opcode):
    """
    Given a numerical opcode it returns a dict of known text nice name values and values

    Use this to get a dict of the known text nice names and values for a particular opcode.
    e.g. opcode 0x0060 (Input) -> [1: 'VGA', 2: 'RGB/HV',...]

    :param opcode: a numerical value for the opcode
    :return: a dict of known text nice name values and values for the opcode (if exists)
    """
    assert len(opcode_values_to_name_dict)  # forgot to load_opcode_dict
    assert 0x0000 <= opcode <= 0xffff
    if opcode in opcode_values_to_name_dict:
        return opcode_values_to_name_dict[opcode]
    return
