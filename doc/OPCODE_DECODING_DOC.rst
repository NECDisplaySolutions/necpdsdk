Help on module opcode_decoding:

NAME
    opcode_decoding - opcode_decoding.py - Tools for working with opcodes and opcode values

FILE
    /home/pi/development/necpdsdk/nec_pd_sdk/opcode_decoding.py

FUNCTIONS
    get_opcode_list()
        Use this to get a sorted numerical list of all of the known opcodes
        
        :return: A numerical list of all of the known opcodes
    
    get_opcode_nice_value_name_list(opcode)
        Given a numerical opcode it returns a list of known opcode value
        
        Use this to get a list of the known numerical values for a particular opcode.
        e.g. opcode 0x0060 (Input) -> ['VGA', 'RGB/HV',...]
        
        :param opcode: a numerical value for the opcode
        :return: a list of known opcode values (if exists)
    
    get_opcode_value_dict(opcode)
        Given a numerical opcode it returns a dict of known text nice name values and values
        
        Use this to get a dict of the known text nice names and values for a particular opcode.
        e.g. opcode 0x0060 (Input) -> [1: 'VGA', 2: 'RGB/HV',...]
        
        :param opcode: a numerical value for the opcode
        :return: a dict of known text nice name values and values for the opcode (if exists)
    
    get_opcode_value_list(opcode)
        Given a numerical opcode it returns a list of known text nice name values for the value
        
        Use this to get a list of the known text nice names of values for a particular opcode.
        e.g. opcode 0x0060 (Input) -> [1, 2,...]
        
        :param opcode: a numerical value for the opcode
        :return: a list of known text nice name values for the value (if exists)
    
    load_opcode_dict()
        Opens and parses a special text file that contains a list of opcodes and their textual "nice names".
        :return:
    
    nice_name_to_opcode(name)
        Given a text nice name it returns a numerical opcode (if exists)
        Note: string must be an exact match (case sensitive)
        
        Use this to lookup the opcode from the textual name of an opcode.
        e.g. "Input" -> 0x0060
        
        :param name: the text "nice name" of the opcode to lookup
        :return: a numerical value for the opcode (if exists)
    
    opcode_nice_value_name_to_value(opcode, nice_value_name)
        Given a numerical opcode and a string with the nice name of the value,
          it returns the value (if exists)
        Note: "nice_value_name" string must be an exact match (case sensitive)
        
        Use this to lookup the value for a particular opcode given the nice name of the value
        e.g. opcode 0x0060 (Input) with "VGA" -> value 1
        
        :param opcode: a numerical value for the opcode
        :param nice_value_name: the text "nice name" of the opcode value
        :return: a numerical value for the opcode value (if exists)
    
    opcode_to_nice_name(opcode)
        Given a numerical opcode it returns the text nice name (if exists)
        
        Use this to lookup the textual name for an opcode.
        e.g. 0x0060 -> "Input"
        
        :param opcode: a numerical value for the opcode
        :return: the text "nice name" of the opcode (if exists)
    
    opcode_value_to_nice_value_name(opcode, value)
        Given a numerical opcode and a value it returns the text nice name of the value (if exists)
        
        Use this to lookup the nice name for the particular value of an opcode
        e.g. opcode 0x0060 (Input) with value 1 -> "VGA"
        
        :param opcode: a numerical value for the opcode
        :param value: a numerical value of the opcode value
        :return: the text "nice name" of the opcode value (if exists)
    
    reverse_dict(d)

DATA
    opcode_to_name_dict = {}
    opcode_values_to_name_dict = {}


