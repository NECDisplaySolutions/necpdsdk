# -*- coding: utf-8 -*-
"""protocol.py - Lower level protocol handling functions for communicating with NEC large-screen displays
Revision: 170322
"""
#
#
# Copyright (C) 2016-18 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.
#


import logging


class PDError(Exception):
    pass


class PDTimeoutError(PDError):
    pass


class PDNullMessageReplyError(PDError):
    pass


class PDUnexpectedReplyError(PDError):
    pass


class PDCommandStatusReturnedError(PDError):
    pass


class PDCommandNotSupportedError(PDError):
    pass

unexpectedReply = PDUnexpectedReplyError('Unexpected reply received')
nullMessageReply = PDNullMessageReplyError('NULL message reply (monitor busy or unknown command)')
replyTimeout = PDTimeoutError('Reply timeout (no reply within timeout period)')
commandStatusReturnedError = PDCommandStatusReturnedError('Command status returned error')


def write_command(f, data, destination_address, message_type):
    logging.debug('destination_address=%02xh, message_type=%02xh', destination_address, message_type)
    output_data = []
    checksum = 0
    # SOH
    output_data.append(0x01)
    # fixed
    output_data.append(0x30)
    # destination address
    output_data.append(destination_address)
    # source address
    output_data.append(0x30)
    # message type
    output_data.append(message_type)
    # message length
    length = len(data) + 2
    output_data.extend(ascii_encode_value_2_bytes(length))
    logging.debug('length=%02xh', length)
    # STX
    output_data.append(0x02)
    # data
    output_data.extend(data)
    # ETX
    output_data.append(0x03)
    # checksum
    for x in output_data[1:]:
        checksum ^= x
    # print "checksum:", hex(checksum)
    output_data.append(checksum)
    # delimiter
    output_data.append(0x0D)
    # print "output_data:", output_data
    # send_data(f, output_data)
    for x in output_data:
        logging.debug('output_data: %02xh', x)
    #   print "output_data: ", hex(x)
    send_data(f, bytearray(output_data))
    return


def read_command_reply(f, destination_reply_is_monitor_id):
    payload_data = []
    checksum = 0
    # SOH
    c = read_character_as_ord(f)
    if c != 0x01:
        logging.error('incorrect SOH: received %02xh  (expected 01h)', c)
        raise unexpectedReply
    # reserved
    c = read_character_as_ord(f)
    if c != 0x30:
        logging.error('incorrect reserved: received %02xh  (expected 30h)', c)
        raise unexpectedReply
    checksum ^= c
    # destination address
    c = read_character_as_ord(f)
    if not destination_reply_is_monitor_id:
        if c != 0x30:
            logging.error('incorrect destination: received %02xh  (expected 30h)', c)
            raise unexpectedReply
    logging.debug('destination=%02xh', c)
    checksum ^= c
    # reply destination address
    c = read_character_as_ord(f)
    reply_destination_address = c
    logging.debug('destination address=%02xh', reply_destination_address)
    checksum ^= c
    # message type
    c = read_character_as_ord(f)
    reply_message_type = c
    logging.debug('reply_message_type=%02xh', reply_message_type)
    checksum ^= c
    # message length (2 bytes)
    c = read_data(f, 2)
    message_length = int(c, 16)
    logging.debug('message_length=%02xh', message_length)
    # Python3 is read as int, so don't need the ord
    # Python2 needs the ord
    if (isinstance(c[0], int)):
        checksum ^= c[0]
    else:
        checksum ^= ord(c[0])
    if (isinstance(c[0], int)):
        checksum ^= c[1]
    else:
        checksum ^= ord(c[1])
    # message payload
    if message_length > 0:
        c = read_character_as_ord(f)
        if c != 0x02:
            logging.error('incorrect STX: received %02xh  (expected 02h)', c)
            raise unexpectedReply
        checksum ^= c
        message_length -= 1
        while message_length > 1:
            message_length -= 1
            c = read_character_as_ord(f)
            checksum ^= c
            payload_data.append(c)
    # ETX
    c = read_character_as_ord(f)
    if c != 0x03:
        logging.error('incorrect ETX: received %02xh (expected 03h)', c)
        raise unexpectedReply
    checksum ^= c
    # checksum
    c = read_character_as_ord(f)
    if checksum != c:
        logging.error('incorrect checksum: received checksum = %02xh, calculated checksum = %02xh', c, checksum)
        raise unexpectedReply
    # Delimiter
    c = read_character_as_ord(f)
    if c != 0x0D:
        logging.error('incorrect Delimiter: received %02xh (expected 0Dh)', c)
        raise unexpectedReply
    for x in payload_data:
        logging.debug('payload: %02xh', x)
    logging.debug('reply_message_type: %02xh', reply_message_type)
    if len(payload_data) == 2 and payload_data[0:2] == ascii_encode_value_2_bytes(0xBE):
        # null message reply
        logging.debug('null message received')
        raise nullMessageReply
    return payload_data, reply_message_type, reply_destination_address


def ascii_encode_value_2_bytes(value):
    output_data = []
    assert 0 <= value <= 0xff
    val = value >> 4
    if val > 9:
        val += 65 - 10
    else:
        val += 48
    output_data.append(val)
    val = (value & 0x0f) % 16
    if val > 9:
        val += 65 - 10
    else:
        val += 48
    output_data.append(val)
    return output_data


def ascii_encode_value_4_bytes(value):
    assert 0 <= value <= 0xffff
    data = ascii_encode_value_2_bytes(value >> 8)
    data.extend(ascii_encode_value_2_bytes(value & 0x00ff))
    return data


def ascii_decode_value(data):
    value = 0
    for byte in data:
        value *= 16
        if 48 <= byte <= 57:
            value += byte - 48
        elif 65 <= byte <= 72:
                value += byte - 65 + 10
        elif 97 <= byte <= 104:
                value += byte - 97 + 10
        else:
            # invalid value
            logging.error('invalid hex character: %i', byte)
            value = 0
    return value


def send_data(f, data):
    f.sendall(data)


def read_data(f, length):
    try:
        reply = f.recv(length)
        if len(reply) == 0:
            logging.error('replyTimeout')
            raise replyTimeout
        return reply
    except:
        raise replyTimeout


def read_character_as_ord(f):
    return ord(read_data(f, 1))


def read_two_characters_as_val(f):
    return int(read_data(f, 2), 16)


def read_four_characters_as_val(f):
    return int(read_data(f, 4), 16)


def two_digit_hex(number):
    return '%02x' % number
