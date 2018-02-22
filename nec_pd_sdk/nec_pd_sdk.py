# -*- coding: utf-8 -*-
"""nec_pd_sdk.py - High level functions for communicating via LAN or RS232 with NEC large-screen displays.

"""
#
#
# Copyright (C) 2016-18 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.

# TODO == Helper Functions ==
# daylight savings decode
# command_auto_power_save_time_write - helper
# opcode unsupported exception
# POP reserved_1 decode



from collections import namedtuple
import socket
import string
import serial
import logging
import time
import datetime
from enum import Enum
from .protocol import *
from .constants import *


PDDateTimeTuple = namedtuple('PDDateTimeTuple', ['status',
                                                 'year',
                                                 'month',
                                                 'day',
                                                 'weekday',
                                                 'hour',
                                                 'minute',
                                                 'daylight_savings'])

PDScheduleTuple = namedtuple('PDScheduleTuple', ['status',
                                                 'program_no',
                                                 'turn_on_hour',
                                                 'turn_on_minute',
                                                 'turn_off_hour',
                                                 'turn_off_minute',
                                                 'timer_input',
                                                 'week_setting',
                                                 'option',
                                                 'picture_mode',
                                                 'extension_1',
                                                 'extension_2',
                                                 'extension_3',
                                                 'extension_4',
                                                 'extension_5',
                                                 'extension_6',
                                                 'extension_7'])

PDScheduleEnableDisableTuple = namedtuple('PDScheduleEnableDisable', ['status',
                                                                      'program_no',
                                                                      'enable_disable'])

PDAdvancedScheduleTuple = namedtuple('PDAdvancedScheduleTuple', ['status',
                                                 'program_no',
                                                 'event',
                                                 'hour',
                                                 'minute',
                                                 'input',
                                                 'week',
                                                 'type',
                                                 'picture_mode',
                                                 'year',
                                                 'month',
                                                 'day',
                                                 'order',
                                                 'extension_1',
                                                 'extension_2',
                                                 'extension_3'])

PDHolidayTuple = namedtuple('PDHolidayTuple', ['status',
                                        'id',
                                        'type',
                                        'year',
                                        'month',
                                        'day',
                                        'week_of_month',
                                        'day_of_week',
                                        'end_month',
                                        'end_day'])

PDWeekendTuple = namedtuple('PDWeekendTuple', ['status',
                                               'weekend'])

PDDaylightSavingsTuple = namedtuple('PDDaylightSavingsTuple', ['status',
                                                               'begin_month',
                                                               'begin_day1',
                                                               'begin_day2',
                                                               'begin_time_hour',
                                                               'begin_time_minute',
                                                               'end_month',
                                                               'end_day1',
                                                               'end_day2',
                                                               'end_time_hour',
                                                               'end_time_minute',
                                                               'time_difference'])

PDOpCodeGetSetTuple = namedtuple('PDOpCodeGetSetTuple', ['result',
                                                         'opcode',
                                                         'type',
                                                         'max_value',
                                                         'current_value'])

PDProofOfPlayLogItemTuple = namedtuple('PDProofOfPlayLogItemTuple', ['status',
                                                                     'log_number',
                                                                     'input',
                                                                     'signal_h_resolution',
                                                                     'signal_v_resolution',
                                                                     'audio_input',
                                                                     'audio_input_status',
                                                                     'picture_status',
                                                                     'audio_status',
                                                                     'year',
                                                                     'month',
                                                                     'day',
                                                                     'hour',
                                                                     'minute',
                                                                     'second',
                                                                     'reserved_1',
                                                                     'reserved_2',
                                                                     'reserved_3'])


PDHelperProofOfPlayLogItemTuple = namedtuple('PDHelperProofOfPlayLogItemTuple', ['status',
                                                                                 'log_number',
                                                                                 'input',
                                                                                 'signal_h_resolution',
                                                                                 'signal_v_resolution',
                                                                                 'audio_input',
                                                                                 'audio_input_status',
                                                                                 'picture_status',
                                                                                 'audio_status',
                                                                                 'date_time',
                                                                                 'reserved_1',
                                                                                 'reserved_2',
                                                                                 'reserved_3'])

PDProofOfPlayStatusTuple = namedtuple('PDProofOfPlayStatusTuple', ['error_status',
                                                                   'total_number',
                                                                   'maximum_number',
                                                                   'current_status'])


PDTileMatrixProfileTuple = namedtuple('PDTileMatrixProfileTuple',
                                      ['profile_number',
                                       'h_monitors',
                                       'v_monitors',
                                       'position',
                                       'tile_comp'])

PDAutoTileMatrixTuple = namedtuple('PDAutoTileMatrixTuple',
                                   ['h_monitors',
                                    'v_monitors',
                                    'pattern_id',
                                    'current_input_select',
                                    'tile_matrix_mem'])

PDPIPPBPProfileTuple = namedtuple('PDPIPPBPProfileTuple',
                                  ['profile_number',
                                   'pip_pbp_mode',
                                   'picture1_input',
                                   'picture2_input',
                                   'picture3_input',
                                   'picture4_input',
                                   'picture1_size',
                                   'picture2_size',
                                   'picture3_size',
                                   'picture4_size',
                                   'picture1_aspect',
                                   'picture2_aspect',
                                   'picture3_aspect',
                                   'picture4_aspect',
                                   'picture1_h_position',
                                   'picture2_h_position',
                                   'picture3_h_position',
                                   'picture4_h_position',
                                   'picture1_v_position',
                                   'picture2_v_position',
                                   'picture3_v_position',
                                   'picture4_v_position',
                                   'reserved_11',
                                   'reserved_12',
                                   'reserved_13',
                                   'reserved_14',
                                   'reserved_15',
                                   'reserved_16',
                                   'reserved_17',
                                   'reserved_18',
                                   'reserved_19',
                                   'reserved_20',
                                   'reserved_21',
                                   'reserved_22'])

class PDSchedule():
    """
    This class holds the definitions values of schedule items
    """

    OnEvent = 1
    OffEvent = 2

    EveryDay = 0x01
    SpecificDays = 0x02
    Enabled = 0x04
    Weekdays = 0x08
    Weekends = 0x10
    Holidays = 0x20
    OneDay = 0x40

    Monday = 0x01
    Tuesday = 0x02
    Wednesday = 0x04
    Thursday = 0x08
    Friday = 0x10
    Saturday = 0x20
    Sunday = 0x40

def retry(function):
    """
    Attempts to retry a command if there was a protocol error.
    Closes and reopens the port to flush the buffers.
    """
    def _retry(self, *args, **kwargs):
        try:
            # reply = function(*args, **kwargs)
            reply = function(self, *args, **kwargs)
            # print "reply: ", reply
            return reply
        except (PDUnexpectedReplyError, PDNullMessageReplyError, PDTimeoutError) as msg:
            logging.debug('command error "%s" so reopen port and retry', msg)
            time.sleep(1)
            self.reopen()
            try:
                reply = function(self, *args, **kwargs)
                return reply
            except (PDUnexpectedReplyError, PDTimeoutError) as msg:
                logging.error('command retry failed with error "%s"', msg)
                raise
            except PDNullMessageReplyError as msg:
                logging.error('command retry failed with error "%s" so assume unsupported', msg)
                raise PDCommandNotSupportedError('retry failed so assume unsupported')
        except PDCommandNotSupportedError as msg:
            logging.debug('unsupported command error "%s" so do not retry', msg)
            raise
        except:
            logging.debug('an unhandled error type so do not retry')
            raise

    return _retry


class MySerial(serial.Serial):  # subclass, inherits from serial
    """
    Add our own functions for serial support to mimic those in 'socket', so we can use the same
    function names.
    """
    def settimeout(self, length):
        self.timeout = length

    def recv(self, length):
        return self.read(length)

    def sendall(self, data):
        try:
            self.reset_input_buffer()
        except AttributeError:
            self.flushInput()  # function was renamed in some versions of serial
        self.write(data)
        return


class NECPD(object):
    """
    Main class for all communications and commands with NEC large-screen displays.
    """
    reply_message_type = 0
    reply_destination_address = 0

    def __init__(self, f):
        self.f = f
        self.destination_address = 0x41

    @classmethod
    def open(cls, address):
        """
        Build a NECPD from an ip address or port. Try and determine if the address
        is an IP address or com port and open appropriately.

        :param address: IP address or serial port name to open
        """
        try:
            socket.inet_aton(address)
            return cls.from_ip_address(address)
        except socket.error:
            return cls.from_com_port(address)

    @classmethod
    def from_ip_address(cls, address, port=7142):
        """
        Build a NECPD from an ip address and port.

        :param address: IP address to use
        :param port: port to use
        """
        try:
            logging.debug('connecting to %s port %i', address, port)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            logging.debug('setting connection timeout to %i', connect_timeout)
            sock.settimeout(connect_timeout)
            sock.connect((address, port))
            cls.address = address
            cls.port = port
            logging.debug('setting reply timeout to %i', reply_timeout)
            sock.settimeout(reply_timeout)

            f = sock
            return cls(f)
        except socket.timeout:
            # print "Timeout connecting to: ", address
            logging.error('connection timeout %s port %i', address, port)
            raise PDError('Connection timeout to ' + address)

    @classmethod
    def from_com_port(cls, serial_port):
        """
        Build a NECPD from a serial port.

        :param serial_port: name of port to try and open
        """
        try:
            logging.debug('connecting to %s with reply timeout %i', serial_port, reply_timeout)
            f = MySerial(
                serial_port,
                baudrate=9600,
                bytesize=serial.EIGHTBITS,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                timeout=reply_timeout,
                xonxoff=0,
                rtscts=0,
            )
        except serial.serialutil.SerialException:
            logging.error('unable to open RS232 port %s ', serial_port)
            raise PDError('Unable to open RS232 port ' + serial_port)
        return cls(f)

    def set_destination_address(self, address):
        """
        Sets the destination address (Monitor ID) for all messages.

        :param address: the "raw" value of the destination address (Monitor ID) sent with each command
        """
        logging.debug('address=%02xh', address)
        # print("set_destination_address: ", hex(address))
        assert ((0x41 <= address <= 0xA4) or (0x31 <= address <= 0x3A) or address == 0x2A)
        self.destination_address = address

    def reopen(self):
        """
        If the connection is socket based, this closes and reopens the socket to try and flush the buffers.
        """
        if type(self.f) is socket:
            # do this to flush the buffers
            self.f.close()
            logging.debug('reopening connection to %s port %i', self.address, self.port)
            self.f.connect((self.address, self.port))
        return

    def close(self):
        """
        Closes socket.
        """
        logging.debug('closing port')
        if self.f is not None:
            self.f.close()

    @retry
    def command_get_parameter(self, opcode):
        """
        Gets the current value and other parameters of an opcode from the display.

        :param opcode: opcode to query
        :return: namedtuple 'PDOpCodeGetSetTuple'
        """
        logging.debug('opcode=%04xh', opcode)
        assert 0x0000 <= opcode <= 0xffff
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(opcode))
        write_command(self.f,
                               send_data,
                               self.destination_address,
                               0x43)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 16:
            if reply_message_type != 0x44:
                logging.error('unexpected reply received')
                raise unexpectedReply                
            offset = 0
            # result
            parameter_len = 2
            reply_result = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # opcode
            parameter_len = 4
            reply_opcode = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # type
            parameter_len = 2
            reply_type = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # max value
            parameter_len = 4
            reply_max_value = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # current value
            parameter_len = 4
            reply_current_value = ascii_decode_value(reply_data[offset:offset + parameter_len])
            return PDOpCodeGetSetTuple(result=reply_result,
                                       opcode=reply_opcode,
                                       type=reply_type,
                                       max_value=reply_max_value,
                                       current_value=reply_current_value)
        else:
            logging.error('unexpected reply length: %i (expected 16)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_set_parameter(self, opcode, value):
        """
        Sets the value an opcode in the display.

        :param opcode: opcode to be set
        :param value: value to set
        :return: namedtuple 'PDOpCodeGetSetTuple'
        """
        logging.debug('opcode=%04xh value=%i', opcode, value)
        assert 0x0000 <= opcode <= 0xffff
        assert 0x0000 <= value <= 0xffff
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(opcode))
        send_data.extend(ascii_encode_value_4_bytes(value))
        write_command(self.f, send_data, self.destination_address, 0x45)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 16:
            if reply_message_type != 0x46:
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 0
            # result
            parameter_len = 2
            reply_result = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # opcode
            parameter_len = 4
            reply_opcode = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # type
            parameter_len = 2
            reply_type = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # max value
            parameter_len = 4
            reply_max_value = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # current value
            parameter_len = 4
            reply_current_value = ascii_decode_value(reply_data[offset:offset + parameter_len])
            return PDOpCodeGetSetTuple(result=reply_result,
                                       opcode=reply_opcode,
                                       type=reply_type,
                                       max_value=reply_max_value,
                                       current_value=reply_current_value)
        else:
            logging.error('unexpected reply length: %i (expected 16)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_power_status_read(self):
        """
        Reads the current power state of the display.

        :return: state value
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0x01D6))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 16:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # result code and power control reply command
            if reply_data[0:4] != ascii_encode_value_4_bytes(0x0200):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:8] != ascii_encode_value_4_bytes(0xD600):
                logging.error('unexpected reply received')
                raise unexpectedReply
            # value parameter
            state = ascii_decode_value(reply_data[12:12+4])
        else:
            logging.error('unexpected reply length: %i (expected 16)', len(reply_data))
            raise unexpectedReply
        return state

    @retry
    def command_power_status_set(self, state):
        """
        Sets the power state of the display.

        :param state:
        :return: state value (same as input parameter - i.e. not updated if the display changes state)
        """
        assert 1 <= state <= 4
        logging.debug('state=%i', state)
        send_data = []
        send_data.extend(ascii_encode_value_2_bytes(0xC2))
        send_data.extend(ascii_encode_value_4_bytes(0x03D6))
        send_data.extend(ascii_encode_value_4_bytes(state))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 12:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # result code and power control reply command
            if reply_data[0:4] != ascii_encode_value_4_bytes(0x00C2):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:8] != ascii_encode_value_4_bytes(0x03D6):
                logging.error('unexpected reply received')
                raise unexpectedReply
            # value parameter
            state = ascii_decode_value(reply_data[8:8 + 4])
        else:
            logging.error('unexpected reply length: %i (expected 12)', len(reply_data))
            raise unexpectedReply
        return state

    @retry
    def command_serial_number_read(self):
        """
        Reads the serial number of the display.

        :return: serial_number string
        """
        logging.debug('')
        send_data = []
        serial_number = ""
        send_data.extend(ascii_encode_value_4_bytes(0xC216))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 4:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # Serial No. reply command
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC316):
                logging.error('unexpected reply received')
                raise unexpectedReply
            pos = 4
            while pos < len(reply_data):
                x = ascii_decode_value(reply_data[pos:pos + 2])
                if x == 0:
                    break
                pos += 2
                serial_number += chr(x)
        else:
            logging.error('unexpected reply length: %i (expected >=4)', len(reply_data))
            raise unexpectedReply
        return serial_number

    @retry
    def command_model_name_read(self):
        """
        Reads the model name of the display.

        :return: model_name string
        """
        logging.debug('')
        send_data = []
        model_name = ""
        send_data.extend(ascii_encode_value_4_bytes(0xC217))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 4:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # Model Name reply Command
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC317):
                logging.error('unexpected reply received')
                raise unexpectedReply
            pos = 4
            while pos < len(reply_data):
                x = ascii_decode_value(reply_data[pos:pos + 2])
                if x == 0:
                    break
                pos += 2
                model_name += chr(x)
        else:
            logging.error('unexpected reply length: %i (expected >=4)', len(reply_data))
            raise unexpectedReply
        return model_name

    @retry
    def command_self_diagnosis_status_read(self):
        """
        Reads the self diagnostic error codes from the display.

        :return: list of result codes
        """
        send_data = []
        result_codes = []
        logging.debug('')
        send_data.extend(ascii_encode_value_2_bytes(0xB1))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 4:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # Model Name reply Command
            if reply_data[0:2] != ascii_encode_value_2_bytes(0xA1):
                logging.error('unexpected reply received')
                raise unexpectedReply
            pos = 2
            while pos < len(reply_data):
                x = ascii_decode_value(reply_data[pos:pos + 2])
                pos += 2
                result_codes.append(x)
        else:
            logging.error('unexpected reply length: %i (expected >=4)', len(reply_data))
            raise unexpectedReply
        return result_codes

    @retry
    def command_firmware_version_read(self, fw_type):
        """
        Reads the firmware version for a particular component type in the display.
        
        :param fw_type: firmware number to read (0 based)
        :return: version as a string
        """
        send_data = []
        version_string = ""
        assert 0 <= fw_type <= 4
        logging.debug('fw_type=%i', fw_type)
        send_data.extend(ascii_encode_value_4_bytes(0xCA02))
        send_data.extend(ascii_encode_value_2_bytes(fw_type))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # Firmware Version Read command reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(fw_type):
                logging.error('unexpected reply received')
                raise unexpectedReply
            for x in reply_data[8:]:
                if x == 0:
                    break
                version_string += chr(x)
            return version_string                
        else:
            logging.error('unexpected reply length: %i (expected >=8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_save_current_settings(self):
        """
        Saves all changes to the display.

        :return:
        """
        send_data = []
        logging.debug('')
        send_data.extend(_encode_value_2_bytes(0x0C))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 4:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # save current settings Command reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0x000C):
                logging.error('unexpected reply received')
                raise unexpectedReply
        else:
            logging.error('unexpected reply length: %i (expected 4)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_get_timing_report(self):
        """
        Reads the timing report for the currently selected video input.

        :return: status_byte, h_freq, v_freq
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_2_bytes(0x07))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 12:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:2] != ascii_encode_value_2_bytes(0x4E):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 2
            # status_byte
            parameter_len = 2
            status_byte = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # h_freq
            parameter_len = 4
            h_freq = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # v_freq
            parameter_len = 4
            v_freq = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            return status_byte, h_freq, v_freq
        else:
            logging.error('unexpected reply length: %i (expected 12)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_date_and_time_read(self):
        """
        Reads the date and time from the display's real time clock. Note that years are 0-99.

        :return: PDDateTimeTuple
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC211))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 18:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC311):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 4
            # year
            parameter_len = 2
            reply_year = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # month
            parameter_len = 2
            reply_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # day
            parameter_len = 2
            reply_day = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # weekday
            parameter_len = 2
            reply_weekday = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # hour
            parameter_len = 2
            reply_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # minute
            parameter_len = 2
            reply_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # daylight_savings
            parameter_len = 2
            reply_daylight_savings = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
        else:
            logging.error('unexpected reply length: %i (expected 18)', len(reply_data))
            raise unexpectedReply
        return PDDateTimeTuple(year=reply_year,
                               month=reply_month,
                               day=reply_day,
                               weekday=reply_weekday,
                               hour=reply_hour,
                               minute=reply_minute,
                               daylight_savings=reply_daylight_savings,
                               status=0)

    @retry
    def command_date_and_time_write(self, value):
        """
        Writes a date and time to the display's real time clock. Note that years are 0-99.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param value: PDDateTimeTuple
        :return: PDDateTimeTuple
        """
        assert 0 <= value.year <= 99
        assert 1 <= value.month <= 12
        assert 1 <= value.day <= 31
        assert 0 <= value.weekday <= 6  # note: not actually used (display calculates)
        assert 0 <= value.hour <= 23
        assert 0 <= value.minute <= 59
        assert 0 <= value.daylight_savings <= 1
        logging.debug('year=%i month=%i day=%i weekday=%i hour=%i minute=%i daylight_savings=%i',
                      value.year,
                      value.month,
                      value.day,
                      value.weekday,
                      value.hour,
                      value.minute,
                      value.daylight_savings)

        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC212))
        send_data.extend(ascii_encode_value_2_bytes(value.year))
        send_data.extend(ascii_encode_value_2_bytes(value.month))
        send_data.extend(ascii_encode_value_2_bytes(value.day))
        send_data.extend(ascii_encode_value_2_bytes(value.weekday))
        send_data.extend(ascii_encode_value_2_bytes(value.hour))
        send_data.extend(ascii_encode_value_2_bytes(value.minute))
        send_data.extend(ascii_encode_value_2_bytes(value.daylight_savings))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 20:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC312):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 4
            # status
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            if reply_status != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            offset += parameter_len
            # year
            parameter_len = 2
            reply_year = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # month
            parameter_len = 2
            reply_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # day
            parameter_len = 2
            reply_day = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # weekday
            parameter_len = 2
            reply_weekday = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # hour
            parameter_len = 2
            reply_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # minute
            parameter_len = 2
            reply_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # daylight_savings
            parameter_len = 2
            reply_daylight_savings = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
        else:
            logging.error('unexpected reply length: %i (expected 20)', len(reply_data))
            raise unexpectedReply
        return PDDateTimeTuple(year=reply_year,
                               month=reply_month,
                               day=reply_day,
                               weekday=reply_weekday,
                               hour=reply_hour,
                               minute=reply_minute,
                               daylight_savings=reply_daylight_savings,
                               status=reply_status)

    @retry
    def command_advanced_schedule_read(self, program_no):
        """
        Reads a schedule to the display. Note: program_no is 0 based (OSD is 1 based).

        :param program_no: zero based program number (0 - 30)
        :return: PDAdvancedScheduleTuple
        """
        #  Note: program_no is 0 based (OSD is 1 based)
        logging.debug('program_no=%i', program_no)
        send_data = []
        assert 0 <= program_no <= 30 
        send_data.extend(ascii_encode_value_4_bytes(0xC23D))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        return self.get_advanced_schedule_from_message(0xC23D, reply_message_type, reply_data)
        

    @retry
    def command_advanced_schedule_write(self, program_no, schedule_in):
        """
        Writes a schedule to the display. Note: program_no is 0 based (OSD is 1 based).
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param program_no: zero based program number (0 - 6)
        :param schedule_in: PDAdvancedScheduleTuple
        :return: PDAdvancedScheduleTuple
        """
        assert 0 <= program_no <= 30
        assert 0 < schedule_in.event <= 2

        assert 0 <= schedule_in.hour <= 24
        assert 0 <= schedule_in.minute <= 60
        assert 0 <= schedule_in.input <= 255
        assert 0 <= schedule_in.week <= 0x7F
        assert 0 <= schedule_in.picture_mode <= 255
        #assert 0 <= schedule_in.year <= 255
        #assert 0 <= schedule_in.month <= 255
        #assert 0 <= schedule_in.day <= 255
        #assert 0 <= schedule_in.order <= 255
        assert 0 <= schedule_in.extension_1 <= 255
        assert 0 <= schedule_in.extension_2 <= 255
        assert 0 <= schedule_in.extension_3 <= 255
        logging.debug('program_no=%i hour=%i minute=%i turn_off_hour=%i turn_off_minute=%i '
                      'timer_input=%i week_setting=%i option=%i picture_mode=%i extension_1=%i extension_2=%i'
                      ' extension_3=%i extension_4=%i extension_5=%i extension_6=%i extension_7=%i',
                      schedule_in.hour,
                      schedule_in.minute,
                      schedule_in.input,
                      schedule_in.week,
                      schedule_in.type,
                      schedule_in.picture_mode,
                      schedule_in.year,
                      schedule_in.month,
                      schedule_in.day,
                      schedule_in.order,
                      schedule_in.extension_1,
                      schedule_in.extension_2,
                      schedule_in.extension_3)
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC23E))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.event))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.hour))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.minute))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.input))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.week))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.type))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.picture_mode))
        if schedule_in.year > 2000:
            schedule_in.year = schedule_in.year - 2000
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.year))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.month))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.day))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.order))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_1))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_2))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_3))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        return self.get_advanced_schedule_from_message(0xC23E, reply_message_type, reply_data)

    @retry
    def command_advanced_schedule_enable_disable(self, program_no, enable_disable):
        """
        Sends the command to enable or disable the schedule

        :param program_no: zero based program number (0 - 30)
        :param enable_disable: 1 for enable and 0 for disable
        :return: PDScheduleEnableDisableTuple
        """

        send_data = []
        assert 0 <= program_no <= 30 
        send_data.extend(ascii_encode_value_4_bytes(0xC23F))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        send_data.extend(ascii_encode_value_2_bytes(enable_disable))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        if len(reply_data) != 10:
            logging.error('unexpected reply length: %i (expected 10)', len(reply_data))
            raise unexpectedReply
        
        if reply_message_type != 0x42:
            logging.error('unexpected reply received')
            raise unexpectedReply

        if reply_data[0:4] != ascii_encode_value_4_bytes(0xC33F):
            logging.error('unexpected reply received')
            raise unexpectedReply

        offset = 4;
        parameter_len = 2;
        reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len]) 
        offset += parameter_len

        reply_program_no = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        reply_enable_disable = ascii_decode_value(reply_data[offset:offset + parameter_len])

        return PDScheduleEnableDisableTuple(status=reply_status,
                                            program_no=reply_program_no,
                                            enable_disable=reply_enable_disable)
        

    @retry
    def command_schedule_read(self, program_no):
        """
        Reads a schedule to the display. Note: program_no is 0 based (OSD is 1 based).

        :param program_no: zero based program number (0 - 6)
        :return: PDScheduleTuple
        """
        #  Note: program_no is 0 based (OSD is 1 based)
        logging.debug('program_no=%i', program_no)
        send_data = []
        assert 0 <= program_no <= 7 
        send_data.extend(ascii_encode_value_4_bytes(0xC221))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        return self.get_schedule_from_message(0xC221, reply_message_type, reply_data)

    @retry
    def command_schedule_write(self, program_no, schedule_in):
        """
        Writes a schedule to the display. Note: program_no is 0 based (OSD is 1 based).
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param program_no: zero based program number (0 - 6)
        :param schedule_in: PDScheduleTuple
        :return: PDScheduleTuple
        """
        assert 0 <= program_no <= 7
        assert 0 <= schedule_in.turn_on_hour <= 24
        assert 0 <= schedule_in.turn_off_hour <= 24
        assert 0 <= schedule_in.turn_on_minute <= 60
        assert 0 <= schedule_in.turn_off_minute <= 60
        assert 0 <= schedule_in.timer_input <= 255
        assert 0 <= schedule_in.week_setting <= 0x7F
        # assert 0 <= schedule_in.option <= 7
        assert 0 <= schedule_in.picture_mode <= 255
        assert 0 <= schedule_in.extension_1 <= 255
        assert 0 <= schedule_in.extension_2 <= 255
        assert 0 <= schedule_in.extension_3 <= 255
        assert 0 <= schedule_in.extension_4 <= 255
        assert 0 <= schedule_in.extension_5 <= 255
        assert 0 <= schedule_in.extension_6 <= 255
        assert 0 <= schedule_in.extension_7 <= 255
        logging.debug('program_no=%i turn_on_hour=%i turn_on_minute=%i turn_off_hour=%i turn_off_minute=%i '
                      'timer_input=%i week_setting=%i option=%i picture_mode=%i extension_1=%i extension_2=%i'
                      ' extension_3=%i extension_4=%i extension_5=%i extension_6=%i extension_7=%i',
                      schedule_in.program_no,
                      schedule_in.turn_on_hour,
                      schedule_in.turn_on_minute,
                      schedule_in.turn_off_hour,
                      schedule_in.turn_off_minute,
                      schedule_in.timer_input,
                      schedule_in.week_setting,
                      schedule_in.option,
                      schedule_in.picture_mode,
                      schedule_in.extension_1,
                      schedule_in.extension_2,
                      schedule_in.extension_3,
                      schedule_in.extension_4,
                      schedule_in.extension_5,
                      schedule_in.extension_6,
                      schedule_in.extension_7)
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC222))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.turn_on_hour))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.turn_on_minute))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.turn_off_hour))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.turn_off_minute))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.timer_input))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.week_setting))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.option))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.picture_mode))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_1))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_2))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_3))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_4))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_5))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_6))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.extension_7))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        return self.get_schedule_from_message(0xC222, reply_message_type, reply_data)

    @retry
    def command_schedule_enable_disable(self, program_no, enable_disable):
        """
        Sends the command to enable or disable the schedule

        :param program_no: zero based program number (0 - 30)
        :param enable_disable: 1 for enable and 0 for disable
        :return: PDScheduleEnableDisableTuple
        """

        send_data = []
        assert 0 <= program_no <= 30 
        send_data.extend(ascii_encode_value_4_bytes(0xC215))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        send_data.extend(ascii_encode_value_2_bytes(enable_disable))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        if len(reply_data) != 10:
            logging.error('unexpected reply length: %i (expected 10)', len(reply_data))
            raise unexpectedReply
        
        if reply_message_type != 0x42:
            logging.error('unexpected reply received')
            raise unexpectedReply

        if reply_data[0:4] != ascii_encode_value_4_bytes(0xC315):
            logging.error('unexpected reply received')
            raise unexpectedReply

        offset = 4;
        parameter_len = 2;
        reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len]) 
        offset += parameter_len

        reply_program_no = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        reply_enable_disable = ascii_decode_value(reply_data[offset:offset + parameter_len])

        return PDScheduleEnableDisableTuple(status=reply_status,
                                            program_no=reply_program_no,
                                            enable_disable=reply_enable_disable)

    def command_holiday_read(self, program_no):
        """
        Read the holiday from the device

        :param program_no: The holiday to read
        :return: PDHolidayTuple
        """
        send_data = []
        assert 0 <= program_no <= 50 
        send_data.extend(ascii_encode_value_4_bytes(0xCA19))
        send_data.extend(ascii_encode_value_2_bytes(0))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        return self.get_holiday_from_message(program_no, 0x00, reply_message_type, reply_data)

    def command_holiday_write(self, program_no, holiday):
        """
        Write the holiday

        :param program_no: 0 based program number
        :param holiday: PDHolidayTuple
        :return: PDHolidayTuple
        """

        assert 0 <= program_no <= 50 
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA19))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(program_no))
        send_data.extend(ascii_encode_value_2_bytes(holiday.type))
        year = holiday.year
        if holiday.year > 2000:
            year = holiday.year - 2000
        send_data.extend(ascii_encode_value_2_bytes(year))
        send_data.extend(ascii_encode_value_2_bytes(holiday.month))
        if holiday.type & 0x02:
            send_data.extend(ascii_encode_value_2_bytes(holiday.day))
        if holiday.type & 0x04:
            send_data.extend(ascii_encode_value_2_bytes(0))
            send_data.extend(ascii_encode_value_2_bytes(holiday.week_of_month))
            send_data.extend(ascii_encode_value_2_bytes(holiday.day_of_week))
        if holiday.type & 0x01:
            send_data.extend(ascii_encode_value_2_bytes(0))
            send_data.extend(ascii_encode_value_2_bytes(0))
            send_data.extend(ascii_encode_value_2_bytes(holiday.end_month))
            send_data.extend(ascii_encode_value_2_bytes(holiday.end_day))

        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        return self.get_holiday_from_message(program_no, 0x01, reply_message_type, reply_data)

    def command_weekend_read(self):
        """
        Read the weekend bitfield from the device

        :return: PDWeekendTuple
        """

        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA1A))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        if len(reply_data) != 8:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        
        if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB1A):
            logging.error('unexpected reply')
            raise unexpectedReply

        offset = 4
        parameter_len = 2
        if reply_data[offset: offset + parameter_len] != ascii_encode_value_2_bytes(0x00):
            logging.error('unexpected reply')
            raise unexpectedReply

        offset += parameter_len

        weekend_bitfield = ascii_decode_value(reply_data[offset: offset + parameter_len])

        return PDWeekendTuple(status=0,
                              weekend=weekend_bitfield)

    def command_weekend_write(self, weekend):
        """
        Write the weekend bitfield from the device

        :param weekend: Weekend Bitfield to write
        :return: PDWeekendTuple
        """

        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA1A))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(weekend.weekend))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)

        if len(reply_data) != 10:
            logging.error('unexpected reply length: %i (expected 10)', len(reply_data))
            raise unexpectedReply
        
        if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB1A):
            logging.error('unexpedted reply')
            raise unexpectedReply

        offset = 4
        parameter_len = 2

        if reply_data[offset: offset + parameter_len] != ascii_encode_value_2_bytes(0x01):
            logging.error('unexpedted reply')
            raise unexpectedReply

        offset += parameter_len

        status = ascii_decode_value(reply_data[offset: offset + parameter_len])
        offset += parameter_len
        weekend_bitfield = ascii_decode_value(reply_data[offset: offset + parameter_len])

        return PDWeekendTuple(status=status,
                              weekend=weekend_bitfield)


    def get_schedule_from_message(self, command, reply_message_type, reply_data):
        """
        Processes the data from a schedule read or write and returns the schedule

        :param command: Command that was send (read or write)
        :param reply_message_type: Type of reply message received
        :param reply_data: Data received in the reply
        :return: PDScheduleTuple
        """

        # Initial offset is 4
        offset = 4
 
        # Data length default
        data_len = 0

        # Reply status default
        reply_status = 0

        # Read Command
        # Set length and check received command
        if command == 0xC221:
            data_len = 36
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC321):
                logging.error('unexpected reply received')
                raise unexpectedReply
        # Write Commmand
        # Set length, check received command and get status
        elif command == 0xC222:
            data_len = 38
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC322):
                logging.error('unexpected reply received')
                raise unexpectedReply
    
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

        # Check the length
        if len(reply_data) != data_len:
            logging.error('unexpected reply length: %i (expected %i)', len(reply_data), data_len)
            raise unexpectedReply
    
        # Check the replay type
        if reply_message_type != 0x42:
            logging.error('unexpected reply received')
            raise unexpectedReply

        # Set default "null" values
        reply_hour = 24
        reply_minute = 60
        reply_event = 0

        # Parameter length is 2 for all the params.  
        parameter_len = 2

        # program_no
        reply_program_no = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # turn_on_hour
        reply_turn_on_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # turn_on_minute
        reply_turn_on_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # turn_off_hour
        reply_turn_off_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # turn_off_minute
        reply_turn_off_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # timer_input
        reply_timer_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # week_setting
        reply_week_setting = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # option
        reply_option = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # picture_mode
        reply_picture_mode = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_1
        reply_extension_1 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_2
        reply_extension_2 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_3
        reply_extension_3 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_4
        reply_extension_4 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_5
        reply_extension_5 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_6
        reply_extension_6 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_7
        reply_extension_7 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        return PDScheduleTuple(status=0,
                               program_no=reply_program_no,
                               turn_on_hour=reply_turn_on_hour,
                               turn_on_minute=reply_turn_on_minute,
                               turn_off_hour=reply_turn_off_hour,
                               turn_off_minute=reply_turn_off_minute,
                               timer_input=reply_timer_input,
                               week_setting=reply_week_setting,
                               option=reply_option,
                               picture_mode=reply_picture_mode,
                               extension_1=reply_extension_1,
                               extension_2=reply_extension_2,
                               extension_3=reply_extension_3,
                               extension_4=reply_extension_4,
                               extension_5=reply_extension_5,
                               extension_6=reply_extension_6,
                               extension_7=reply_extension_7)

    def get_advanced_schedule_from_message(self, command, reply_message_type, reply_data):
        """
        Processes the data from an advanced schedule read or write and returns the schedule
      
        :param command: Command that was sent (read or write)
        :param reply_message_type: Type of reply message received
        :param reply_data: Data received in the reply
        :return: PDAdvancedScheduleTuple
        """

        # Initial offset is 4 
        offset = 4
   
        # Data length default
        data_len = 0
    
        # Reply status default
        reply_status = 0
    
        # Read Command
        # Set length and check received command
        if command == 0xC23D:
            data_len = 34
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC33D):
                logging.error('unexpected reply received')
                raise unexpectedReply
        # Write Commmand
        # Set length, check received command and get status
        elif command == 0xC23E:
            data_len = 36
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC33E):
                logging.error('unexpected reply received')
                raise unexpectedReply
    
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

        # Check the length
        if len(reply_data) != data_len:
            logging.error('unexpected reply length: %i (expected %i)', len(reply_data), data_len)
            raise unexpectedReply
    
        # Check the replay type
        if reply_message_type != 0x42:
            logging.error('unexpected reply received')
            raise unexpectedReply

        # Set default "null" values
        reply_hour = 24
        reply_minute = 60
        reply_event = 0

        # Parameter length is 2 for all the params.  
        parameter_len = 2

        # program_no
        reply_program_no = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # event
        reply_event = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len
        if reply_event < 1 or reply_event > 2:
            logging.error('unexpected reply event: %i (expected 1 or 2)', reply_event)
            raise unexpectedReply

        # Get the hour and minute
        reply_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
        logging.debug('reply_hour  "%s"', reply_hour)
        offset += parameter_len
        reply_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # input
        reply_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len
 
        # week
        reply_week = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # type
        reply_type = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # picture_mode
        reply_picture_mode = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # year
        reply_year = ascii_decode_value(reply_data[offset:offset + parameter_len])
        if reply_year > 0:
            reply_year += 2000

        offset += parameter_len

        # month
        reply_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # day
        reply_day = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # order
        reply_order = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_1
        reply_extension_1 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_2
        reply_extension_2 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        # extension_3
        reply_extension_3 = ascii_decode_value(reply_data[offset:offset + parameter_len])
        offset += parameter_len

        return PDAdvancedScheduleTuple(status=reply_status,
                                   program_no=reply_program_no,
                                   event=reply_event,
                                   hour=reply_hour,
                                   minute=reply_minute,
                                   input=reply_input,
                                   week=reply_week,
                                   type=reply_type,
                                   picture_mode=reply_picture_mode,
                                   year=reply_year,
                                   month=reply_month,
                                   day=reply_day,
                                   order=reply_order,
                                   extension_1=reply_extension_1,
                                   extension_2=reply_extension_2,
                                   extension_3=reply_extension_3)


    def get_holiday_from_message(this, program_no, command, reply_message_type, reply_data):
        """
        Processes the data from a holiday read or write and returns the holiday
      
        :param program_no: The holiday number
        :param command: Command that was sent (read or write)
        :param reply_message_type: Type of reply message received
        :param reply_data: Data received in the reply
        :return: PDHolidayTuple
        """
        # Initial offset is 6 
        offset = 6
   
        # Data length default
        data_len = 0
    
        # Reply status default
        reply_status = 0
    
        # Read Command
        # Set length and check received command
        if command == 0x00:
            data_len = 24
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB19) and reply_data[5:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('1 unexpected reply received')
                raise unexpectedReply
        # Write Commmand
        # Set length, check received command and get status
        elif command == 0x01:
            data_len = 26
            print("reply_data[5:6]: ", reply_data[5:6])
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB19) and reply_data[4:5] != ascii_encode_value_2_bytes(0x01):
                logging.error('2 unexpected reply received')
                raise unexpectedReply
    
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

        # Check the length
        if len(reply_data) != data_len:
            logging.error('3 unexpected reply length: %i (expected %i)', len(reply_data), data_len)
            raise unexpectedReply
    
        # Check the reply type
        if reply_message_type != 0x42:
            logging.error('4 unexpected reply received')
            raise unexpectedReply

        # Parameter length is 2 for all the params.  
        parameter_len = 2

        reply_id = ascii_decode_value(reply_data[offset: offset + parameter_len])
        offset += parameter_len
   
        if (reply_id != program_no):
            logging.error('5 unexpected reply received')
            raise unexpectedReply
 
        reply_type = ascii_decode_value(reply_data[offset: offset + parameter_len])
        offset += parameter_len

        reply_year = ascii_decode_value(reply_data[offset: offset + parameter_len])
        if reply_year > 0:
            reply_year += 2000

        offset += parameter_len

        reply_month = ascii_decode_value(reply_data[offset: offset + parameter_len])
        offset += parameter_len

        # Initialize Values
        reply_day = 0
        reply_end_month = 0
        reply_end_day = 0
        reply_week_of_month = 0
        reply_day_of_week = 0
        
        # Single Date
        if reply_type & 0x02:
            reply_day = ascii_decode_value(reply_data[offset: offset + parameter_len])
            offset += parameter_len

            # Date Range
            if reply_type & 0x01:
                # Spec is wrong, so need to skip the next 4 
                offset += 4
                reply_end_month = ascii_decode_value(reply_data[offset: offset + parameter_len])
                offset += parameter_len
                reply_end_day = ascii_decode_value(reply_data[offset: offset + parameter_len])
                offset += parameter_len
        elif reply_type & 0x04:
            # Spec is wrong, so need to skip the next 2
            offset += parameter_len
            reply_week_of_month = ascii_decode_value(reply_data[offset: offset + parameter_len])
            offset += parameter_len
            reply_day_of_week = ascii_decode_value(reply_data[offset: offset + parameter_len])
            offset += parameter_len

        return PDHolidayTuple(status=reply_status,
                              id=reply_id,
                              type=reply_type,
                              year=reply_year,
                              month=reply_month,
                              day=reply_day,
                              week_of_month=reply_week_of_month,
                              day_of_week=reply_day_of_week,
                              end_month=reply_end_month,
                              end_day=reply_end_day)  
         

    @retry
    def command_lan_mac_address_read(self):
        """
        Reads the LAN MAC address of the display.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :return: a string of the MAC address using "-" separators
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC22A))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 10:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # LAN read reply command
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC32A):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 4
            # status_byte
            parameter_len = 2
            status_byte = ascii_decode_value(reply_data[offset:offset + parameter_len])
            if status_byte != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            offset += parameter_len
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset += 2
            # IPV
            parameter_len = 2
            ipv = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            mac = ""
            while offset+1 < len(reply_data):
                x = ascii_decode_value(reply_data[offset:offset + 2])
                mac += format(x, "x")
                offset += 2
                if offset < len(reply_data):
                    mac += "-"
            return mac, ipv
        else:
            logging.error('unexpected reply length: %i (expected >=10)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_ip_address_read(self):
        """
        Reads the LAN IP address of the display.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :return: a string of the IP address with decimal numbers and using "." separators
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC22A))
        send_data.extend(ascii_encode_value_2_bytes(0x45))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 10:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # LAN read reply command
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC32A):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 4
            # status_byte
            parameter_len = 2
            status_byte = ascii_decode_value(reply_data[offset:offset + parameter_len])
            if status_byte != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            offset += parameter_len
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x45):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset += 2
            # IPV
            parameter_len = 2
            ipv = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            ip = ""
            while offset+1 < len(reply_data):
                x = ascii_decode_value(reply_data[offset:offset + 2])
                ip += format(x, "d")
                offset += 2
                if offset < len(reply_data):
                    ip += "."
            return ip, ipv
        else:
            logging.error('unexpected reply length: %i (expected >=10)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_power_save_mode_read(self):
        """
        Reads the current Power Save Mode setting from the display

        :return: mode
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0B))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('unexpected reply received')
                raise unexpectedReply
            mode = ascii_decode_value(reply_data[6:8])
            return mode
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_power_save_mode_write(self, in_mode):
        """
        Writes the power save mode to the display. 
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param in_mode:
        :return:
        """
        logging.debug('in_mode=%i', in_mode)
        assert 0 <= in_mode <= 2
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0B))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(in_mode))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_auto_power_save_time_read(self):
        """
        Reads the power save time to the display. Note that the value returned is specified in
        values of 5 seconds. i.e. 1 = 5sec, 2=10 sec.

        :return: value specified in values of 5 seconds
        :return:
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0B))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            reply = ascii_decode_value(reply_data[6:8])
            return reply
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_auto_power_save_time_write(self, in_value):
        """
        Writes the power save time to the display. Note that the value is specified in
        values of 5 seconds. i.e. 1 = 5 sec, 2=10 sec.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'

        :param in_value: specified in values of 5 seconds
        :return:
        """
        logging.debug('in_value=%i', in_value)
        assert 0 <= in_value <= 120
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0B))
        send_data.extend(ascii_encode_value_2_bytes(0x03))
        send_data.extend(ascii_encode_value_2_bytes(in_value))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_auto_standby_time_read(self):
        """
        Reads the standby time to the display. Note that the value returned is specified in
        values of 5 seconds. i.e. 1 = 5sec, 2=10 sec.

        :return: value specified in values of 5 seconds
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0B))
        send_data.extend(ascii_encode_value_2_bytes(0x04))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            reply = ascii_decode_value(reply_data[6:8])
            return reply
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_auto_standby_time_write(self, in_value):
        """
        Writes the standby time to the display. Note that the value is specified in
        values of 5 seconds. i.e. 1 = 5sec, 2=10 sec.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'

        :param in_value: specified in values of 5 seconds
        :return: 
        """
        logging.debug('in_value=%i', in_value)
        assert 0 <= in_value <= 120
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0B))
        send_data.extend(ascii_encode_value_2_bytes(0x05))
        send_data.extend(ascii_encode_value_2_bytes(in_value))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x05):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_direct_tv_channel_read(self):
        """
        Reads the current TV channel from the tuner (if installed).
        Raises "PDCommandNotSupportedError" if the tuner is not installed, selected, or supported.

        :return: major, minor
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC22C))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 16:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC32C):
                logging.error('unexpected reply received')
                raise unexpectedReply
            major = ascii_decode_value(reply_data[4:12])
            minor = ascii_decode_value(reply_data[12:16])
        elif len(reply_data) == 4:
            # display replies with 0xC22C if tuner option not selected
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC22C):
                logging.error('unexpected reply received')
                raise unexpectedReply
            raise PDCommandNotSupportedError('command_direct_tv_channel_read not available')
        else:
            logging.error('unexpected reply length: %i (expected 16 or 4)', len(reply_data))
            raise unexpectedReply
        return major, minor

    @retry
    def command_direct_tv_channel_write(self, channel_in_major, channel_in_minor):
        """
        Selects the TV channel for the tuner (if installed). Note channel values are not verified to be
        valid by the display and are ignored if not programmed / invalid.
        Raises "PDCommandNotSupportedError" if the tuner is not installed, selected, or supported.

        :param channel_in_major:
        :param channel_in_minor:
        :return: major, minor
        """
        logging.debug('channel_in_major=%i channel_in_minor=%i', channel_in_major, channel_in_minor)
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC22D))
        send_data.extend(ascii_encode_value_4_bytes((channel_in_major & 0xffff0000) >> 16))
        send_data.extend(ascii_encode_value_4_bytes(channel_in_major & 0x0000ffff))
        send_data.extend(ascii_encode_value_4_bytes(channel_in_minor))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 16:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC32D):
                logging.error('unexpected reply received')
                raise unexpectedReply
            major = ascii_decode_value(reply_data[4:12])
            if major != channel_in_major:
                logging.error('unexpected reply major does not match received')
                raise unexpectedReply
            minor = ascii_decode_value(reply_data[12:16])
            if minor != channel_in_minor:
                logging.error('unexpected reply minor does not match received')
                raise unexpectedReply
        elif len(reply_data) == 4:
            # display replies with 0xC22D if tuner option not selected
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC22D):
                logging.error('unexpected reply received')
                raise unexpectedReply
            raise PDCommandNotSupportedError('command_direct_tv_channel_write not available')
        else:
            logging.error('unexpected reply length: %i (expected 16 or 4)', len(reply_data))
            raise unexpectedReply
        return major, minor

    @retry
    def command_daylight_savings_read(self):
        """
        Reads the current daylight savings schedule from the display.

        :return: PDDaylightSavingsTuple
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA01))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 30:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('unexpected reply received')
                raise unexpectedReply
            offset = 6
            # status
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # begin_month
            parameter_len = 2
            reply_begin_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # begin_day1
            parameter_len = 2
            reply_begin_day1 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # begin_day2
            parameter_len = 2
            reply_begin_day2 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # begin_time_hour
            parameter_len = 2
            reply_begin_time_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # begin_time_minute
            parameter_len = 2
            reply_begin_time_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # end_month
            parameter_len = 2
            reply_end_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # end_day1
            parameter_len = 2
            reply_end_day1 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # end_day2
            parameter_len = 2
            reply_end_day2 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # end_time_hour
            parameter_len = 2
            reply_end_time_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # end_time_minute
            parameter_len = 2
            reply_end_time_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # time_difference
            parameter_len = 2
            reply_time_difference = ascii_decode_value(reply_data[offset:offset + parameter_len])
            return PDDaylightSavingsTuple(status=reply_status, begin_month=reply_begin_month,
                                          begin_day1=reply_begin_day1,
                                          begin_day2=reply_begin_day2, begin_time_hour=reply_begin_time_hour,
                                          begin_time_minute=reply_begin_time_minute, end_month=reply_end_month,
                                          end_day1=reply_end_day1, end_day2=reply_end_day2,
                                          end_time_hour=reply_end_time_hour, end_time_minute=reply_end_time_minute,
                                          time_difference=reply_time_difference)
        else:
            logging.error('unexpected reply length: %i (expected 30)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_daylight_savings_write(self, schedule_in):
        """
        Writes the daylight savings schedule to the display.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'

        :param schedule_in:
        :return:
        """
        logging.debug('schedule_in=%i', schedule_in)
        assert 1 <= schedule_in.begin_month <= 12
        assert 1 <= schedule_in.begin_day1 <= 5
        assert 1 <= schedule_in.begin_day2 <= 7
        assert 0 <= schedule_in.begin_time_hour <= 23
        assert 0 <= schedule_in.begin_time_minute <= 59
        assert 1 <= schedule_in.end_month <= 12
        assert 1 <= schedule_in.end_day1 <= 5
        assert 1 <= schedule_in.end_day2 <= 7
        assert 0 <= schedule_in.end_time_hour <= 23
        assert 0 <= schedule_in.end_time_minute <= 59
        assert 0 <= schedule_in.time_difference <= 3
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA01))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.begin_month))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.begin_day1))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.begin_day2))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.begin_time_hour))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.begin_time_minute))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.end_month))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.end_day1))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.end_day2))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.end_time_hour))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.end_time_minute))
        send_data.extend(ascii_encode_value_2_bytes(schedule_in.time_difference))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            status = ascii_decode_value(reply_data[6:8])
            if status != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_daylight_savings_on_off_read(self):
        """
        Reads the current daylight savings on/off setting from the display.

        :return: 0=off 1=on
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA01))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 10:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return ascii_decode_value(reply_data[8:10])
        else:
            logging.error('unexpected reply length: %i (expected 10)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_daylight_savings_on_off_write(self, value):
        """
              Writes the daylight savings on/off setting to the display.

        :param value: 0=off 1=on
        :return:
        """
        logging.debug('')
        assert 0 <= value <= 1
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA01))
        send_data.extend(ascii_encode_value_2_bytes(0x03))
        send_data.extend(ascii_encode_value_2_bytes(value))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_auto_id_execute(self):
        """
        Starts the process of assigning consecutive Monitor IDs to daisy-chained displays.

        :return:
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0A))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0A):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    def command_auto_id_complete_notify(self):
        """
        Waits for the display to reply after performing Auto ID using command_auto_id_execute

        :return:
        """
        logging.debug('')
        self.f.settimeout(30)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        self.f.settimeout(reply_timeout)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCA0A):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            return ascii_decode_value(reply_data[6:8])
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            self.f.settimeout(reply_timeout)
            raise unexpectedReply

    @retry
    def command_auto_id_reset(self):
        """
        Resets the Auto ID assignments

        :return:
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0A))
        send_data.extend(ascii_encode_value_2_bytes(0x03))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0A):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_auto_tile_matrix_execute(self, settings):
        """
        Starts the process of Auto Tile Matrix daisy-chained displays.

        :return:
        """
        logging.debug('')
        assert 1 <= settings.h_monitors <= 10
        assert 1 <= settings.v_monitors <= 10
        assert settings.pattern_id == 1
        assert 1 <= settings.current_input_select <= 255
        assert 0 <= settings.tile_matrix_mem <= 1
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA03))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(settings.h_monitors))
        send_data.extend(ascii_encode_value_2_bytes(settings.v_monitors))
        send_data.extend(ascii_encode_value_2_bytes(settings.pattern_id))
        send_data.extend(ascii_encode_value_2_bytes(settings.current_input_select))
        send_data.extend(ascii_encode_value_2_bytes(settings.tile_matrix_mem))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    def command_auto_tile_matrix_complete(self):
        """
        Waits for the display to reply after performing Auto ID using command_auto_id_execute

        :return:
        """
        logging.debug('')
        self.f.settimeout(30)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        self.f.settimeout(reply_timeout)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            return ascii_decode_value(reply_data[6:8])
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            self.f.settimeout(reply_timeout)
            raise unexpectedReply

    @retry
    def command_auto_tile_matrix_read(self):
        """
        Reads the Auto Tile Matrix assignments

        :return: h_monitors, v_monitors
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA03))
        send_data.extend(ascii_encode_value_2_bytes(0x04))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 12:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            h_monitors = ascii_decode_value(reply_data[8:10])
            v_monitors = ascii_decode_value(reply_data[10:12])
            return h_monitors, v_monitors
        else:
            logging.error('unexpected reply length: %i (expected 12)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_auto_tile_matrix_write(self, h_monitors, v_monitors):
        """
        Writes the Auto Tile Matrix assignments
        :param h_monitors:
        :param v_monitors:
        :return:
        """
        logging.debug('')
        assert 1 <= h_monitors <= 10
        assert 1 <= v_monitors <= 10
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA03))
        send_data.extend(ascii_encode_value_2_bytes(0x05))
        send_data.extend(ascii_encode_value_2_bytes(h_monitors))
        send_data.extend(ascii_encode_value_2_bytes(v_monitors))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x05):
                logging.error('unexpected reply received')
                raise unexpectedReply
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_auto_tile_matrix_reset(self):
        """
        Resets the Auto Tile Matrix assignments

        :return:
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA03))
        send_data.extend(ascii_encode_value_2_bytes(0x06))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x06):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            return
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_asset_data_read(self, offset):
        """
        Reads a chunk of the asset data string from the display.

        :param offset: Offset of chunk of the asset data string to read. Either 0 or 32.
        :return: asset_string
        """
        logging.debug('')
        send_data = []
        asset_string = ""
        assert 0 <= offset <= 64
        send_data.extend(ascii_encode_value_4_bytes(0xC00B))
        send_data.extend(ascii_encode_value_2_bytes(offset))
        send_data.extend(ascii_encode_value_2_bytes(32))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 4:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # asset data Read reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC10B):
                logging.error('unexpected reply received')
                raise unexpectedReply
            for x in reply_data[4:]:
                if x == 0:
                    break
                asset_string += chr(x)
            return asset_string
        else:
            logging.error('unexpected reply length: %i (expected >=4)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_asset_data_write(self, offset, in_string):
        """
        Writes a chunk of the asset data string to the display.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param offset: either 0 or 32
        :param in_string: string of up to 32 characters
        :return: asset_string reply
        """
        logging.debug('offset=%i in_string=%s', offset, in_string)
        send_data = []
        asset_string = ""
        assert 0 <= offset <= 64
        assert 0 <= len(in_string) <= 32
        assert offset+len(in_string) <= 64
        send_data.extend(ascii_encode_value_4_bytes(0xC00E))
        send_data.extend(ascii_encode_value_2_bytes(offset))
        for x in in_string:
            send_data.extend([ord(x)])
        # pad with null
        for i in range(len(in_string), 32):
            send_data.extend([0])
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # asset data write reply
            result = ascii_decode_value(reply_data[0:2])
            if result != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            if reply_data[2:6] != ascii_encode_value_4_bytes(0xC00E):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(offset):
                logging.error('unexpected reply received')
                raise unexpectedReply
            for x in reply_data[8:]:
                print("received:", chr(x))
                if x == 0:
                    break
                asset_string += chr(x)
            return asset_string
        else:
            logging.error('unexpected reply length: %i (expected >=6)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_send_ir_remote_control_code(self, code):
        """
        Sends an IR remote control code to the display that mimics using the IR remote.

        :param code: code in range 0 - 0xffff
        :return:
        """
        logging.debug('code=%02xh', code)
        assert 0 <= code <= 0xffff
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC210))
        send_data.extend(ascii_encode_value_4_bytes(code))
        send_data.extend(ascii_encode_value_2_bytes(0x03))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC310):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:8] != ascii_encode_value_4_bytes(code):
                logging.error('unexpected reply received')
                raise unexpectedReply
        elif len(reply_data) == 12:  # older models reply with this format
            if reply_data[2:6] != ascii_encode_value_4_bytes(0xC210):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:10] != ascii_encode_value_4_bytes(code):
                logging.error('unexpected reply received')
                raise unexpectedReply
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_input_name_read(self):
        """
        Reads the OSD text name for the current video input.

        :return: name_string
        """
        logging.debug('')
        send_data = []
        name_string = ""
        send_data.extend(ascii_encode_value_4_bytes(0xCA04))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('unexpected reply received')
                raise unexpectedReply
            pos = 6
            while pos < len(reply_data):
                x = ascii_decode_value(reply_data[pos:pos + 2])
                if x == 0:
                    break
                pos += 2
                name_string += chr(x)
        else:
            logging.error('unexpected reply length: %i (expected >=8)', len(reply_data))
            raise unexpectedReply
        return name_string

    @retry
    def command_input_name_write(self, name_string):
        """
        Writes the OSD text name for the current video input.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param name_string:
        :return:
        """
        logging.debug('name_string=%s', name_string)
        send_data = []
        assert len(name_string) <= 8
        send_data.extend(ascii_encode_value_4_bytes(0xCA04))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        for char in name_string:
            send_data.extend(ascii_encode_value_2_bytes(ord(char)))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x00):
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_input_name_reset(self):
        """
        Resets the OSD text name for the current video input to the default text.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :return:
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA04))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x00):
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_input_name_of_designated_terminal_read(self, video_input):
        """
                Reads the OSD text name for a specific video input.

        :param video_input: video input to read input name of
        :return:
        """
        logging.debug('')
        assert 0x00 <= video_input <= 0xff
        send_data = []
        name_string = ""
        send_data.extend(ascii_encode_value_4_bytes(0xCA04))
        send_data.extend(ascii_encode_value_2_bytes(0x03))
        send_data.extend(ascii_encode_value_2_bytes(video_input))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 10:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x03):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x00):
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            if reply_data[8:10] != ascii_encode_value_2_bytes(video_input):
                logging.error('unexpected reply received')
                raise unexpectedReply
            pos = 10
            while pos < len(reply_data):
                x = ascii_decode_value(reply_data[pos:pos + 2])
                if x == 0:
                    break
                pos += 2
                name_string += chr(x)
        else:
            logging.error('unexpected reply length: %i (expected >=8)', len(reply_data))
            raise unexpectedReply
        return name_string

    @retry
    def command_input_name_of_designated_terminal_write(self, video_input, name_string):
        """
        Writes the OSD text name for a specific video input.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param video_input: video input to write input name of
        :param name_string:
        :return:
        """
        logging.debug('name_string=%s input=%i', name_string, video_input)
        assert 0x00 <= video_input <= 0xff
        send_data = []
        assert len(name_string) <= 8
        send_data.extend(ascii_encode_value_4_bytes(0xCA04))
        send_data.extend(ascii_encode_value_2_bytes(0x04))
        send_data.extend(ascii_encode_value_2_bytes(video_input))
        for char in name_string:
            send_data.extend(ascii_encode_value_2_bytes(ord(char)))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x00):
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_input_name_of_designated_terminal_reset(self, video_input):
        """
        Resets the OSD text name for the current video input to the default text.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param video_input: video input to reset the name of
        :return:
        """
        logging.debug('input=%i', video_input)
        assert 0x00 <= video_input <= 0xff
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA04))
        send_data.extend(ascii_encode_value_2_bytes(0x05))
        send_data.extend(ascii_encode_value_2_bytes(video_input))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            # reply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB04):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x05):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[6:8] != ascii_encode_value_2_bytes(0x00):
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_security_enable_read(self):
        """
        Reads the current Security Enable status.

        :return: secure_mode
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0C))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0C):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            secure_mode = ascii_decode_value(reply_data[6:8])
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return secure_mode

    @retry
    def command_security_enable_write(self, secure_mode, password):
        """
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param secure_mode: 
        :param password: 4 digit string
        :return: secure_mode
        """
        logging.debug('secure_mode=%i password=%s', secure_mode, password)
        assert 0 <= secure_mode <= 3
        assert len(password) == 4
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA0C))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(secure_mode))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        for char in password:
            assert 0x30 <= ord(char) <= 0x39
            send_data.extend([0x33, 0x33, 0x33, ord(char)])
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB0C):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return secure_mode

    @retry
    def command_security_lock_control(self, secure_mode, password):
        """
        Performs the Security Lock Control command.

        :param secure_mode:
        :param password: 4 digit string
        :return: status, mode
        """
        assert 0 <= secure_mode <= 3
        assert len(password) == 4
        logging.debug('secure_mode=%i password=%s', secure_mode, password)
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xC21D))
        send_data.extend(ascii_encode_value_2_bytes(secure_mode))
        for char in password:
            assert 0x30 <= ord(char) <= 0x39
            send_data.extend(ascii_encode_value_2_bytes(ord(char)-0x30))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xC31D):
                logging.error('unexpected reply received')
                raise unexpectedReply
            status = ascii_decode_value(reply_data[4:6])
            mode = ascii_decode_value(reply_data[6:8])
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return status, mode

    @retry
    def command_set_proof_of_play_operation_mode(self, in_mode):
        """
        Sets the Proof Of Play operation mode in the display.

        :param in_mode:
        :return: status
        """
        assert 0 <= in_mode <= 2
        logging.debug('in_mode=%i', in_mode)
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA15))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        send_data.extend(ascii_encode_value_2_bytes(in_mode))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB15):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('unexpected reply received')
                raise unexpectedReply
            status = ascii_decode_value(reply_data[6:8])
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return status

    @retry
    def command_get_proof_of_play_status(self):
        """
        Reads the current proof of play status from the the display.

        :return: PDProofOfPlayStatusTuple
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA15))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 18:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB15):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            reply_error_status = ascii_decode_value(reply_data[6:8])
            reply_total_number = ascii_decode_value(reply_data[8:12])
            reply_maximum_number = ascii_decode_value(reply_data[12:16])
            reply_current_status = ascii_decode_value(reply_data[16:18])
            return PDProofOfPlayStatusTuple(error_status=reply_error_status,
                                            total_number=reply_total_number,
                                            maximum_number=reply_maximum_number,
                                            current_status=reply_current_status)
        else:
            logging.error('unexpected reply length: %i (expected 18)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_get_proof_of_play_current(self):
        """
        Reads the latest proof of play log from the the display.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :return: PDProofOfPlayLogItemTuple
        """
        logging.debug('')
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA15))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 50:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB15):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply

            offset = 6
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            if reply_status != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            parameter_len = 4
            reply_log_number = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 4
            reply_signal_h_resolution = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 4
            reply_signal_v_resolution = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_audio_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_audio_input_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_picture_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_audio_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 4
            reply_year = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_day = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_second = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_reserved_1 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_reserved_2 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_reserved_3 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            
            return PDProofOfPlayLogItemTuple(status=reply_status, 
                                             log_number=reply_log_number,
                                             input=reply_input, 
                                             signal_h_resolution=reply_signal_h_resolution,
                                             signal_v_resolution=reply_signal_v_resolution, 
                                             audio_input=reply_audio_input, 
                                             audio_input_status=reply_audio_input_status,
                                             picture_status=reply_picture_status,
                                             audio_status=reply_audio_status,
                                             year=reply_year,
                                             month=reply_month,
                                             day=reply_day,
                                             hour=reply_hour,
                                             minute=reply_minute,
                                             second=reply_second,
                                             reserved_1=reply_reserved_1,
                                             reserved_2=reply_reserved_2,
                                             reserved_3=reply_reserved_3)
        else:
            logging.error('unexpected reply length: %i (expected 50)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_get_proof_of_play_number_to_number(self, from_number, to_number):
        """
        Reads a specific proof of play log from the the display.
        Note: only support reading 1 log at a time.
        Raises "PDCommandStatusReturnedError" if the returned status is not 'No Error'.

        :param from_number:
        :param to_number:
        :return:
        """
        assert from_number == to_number   # only support reading 1 log at a time
        assert 0 <= from_number <= 0xffff
        logging.debug('from_number=%i to_number=%i', from_number, to_number)
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA15))
        send_data.extend(ascii_encode_value_2_bytes(0x03))
        send_data.extend(ascii_encode_value_4_bytes(from_number))
        send_data.extend(ascii_encode_value_4_bytes(to_number))

        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 50:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB15):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x03):
                logging.error('unexpected reply received')
                raise unexpectedReply

            offset = 6
            parameter_len = 2
            reply_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            if reply_status != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError

            parameter_len = 4
            reply_log_number = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 4
            reply_signal_h_resolution = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 4
            reply_signal_v_resolution = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_audio_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_audio_input_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_picture_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_audio_status = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 4
            reply_year = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_month = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_day = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_hour = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_minute = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_second = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_reserved_1 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_reserved_2 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            parameter_len = 2
            reply_reserved_3 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            return PDProofOfPlayLogItemTuple(status=reply_status, 
                                             log_number=reply_log_number,
                                             input=reply_input, 
                                             signal_h_resolution=reply_signal_h_resolution,
                                             signal_v_resolution=reply_signal_v_resolution, 
                                             audio_input=reply_audio_input, 
                                             audio_input_status=reply_audio_input_status,
                                             picture_status=reply_picture_status,
                                             audio_status=reply_audio_status,
                                             year=reply_year,
                                             month=reply_month,
                                             day=reply_day,
                                             hour=reply_hour,
                                             minute=reply_minute,
                                             second=reply_second,
                                             reserved_1=reply_reserved_1,
                                             reserved_2=reply_reserved_2,
                                             reserved_3=reply_reserved_3)
        else:
            logging.error('unexpected reply length: %i (expected 50)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_capabilities_request(self, offset):
        """
        Reads a chunk of the capability string.

        :param offset: offset to read - increments of 32
        :return:
        """
        assert 0 <= offset <= 0xffff
        logging.debug('offset=%i', offset)
        capability_string = ""
        send_data = []
        send_data.extend(ascii_encode_value_2_bytes(0xF3))
        send_data.extend(ascii_encode_value_2_bytes(offset >> 8))
        send_data.extend(ascii_encode_value_2_bytes(offset & 0xff))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) >= 6:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received (expected reply_message_type 42h')
                raise unexpectedReply
            # capabilities request reply command
            if reply_data[0:2] != ascii_encode_value_2_bytes(0xE3):
                logging.error('unexpected reply received (expected capabilities request reply command E3 (45h 33h)')
                raise unexpectedReply
            reply_offset = (ascii_decode_value(reply_data[2:4]) << 8)
            reply_offset += ascii_decode_value(reply_data[4:6])
            if reply_offset != offset:
                logging.debug('command_capabilities_request offsets do not match: %i vs %i', reply_offset, offset)
                raise unexpectedReply
            pos = 6
            while pos < len(reply_data):
                x = reply_data[pos]
                if x == 0:
                    break
                pos += 1
                capability_string += chr(x)
        else:
            logging.error('unexpected reply length: %i (expected >=6)', len(reply_data))
            raise unexpectedReply
        return capability_string

    @retry
    def command_tile_matrix_profile_contents_write(self, settings):
        """
        Saves Tile Matrix settings into a memory so that they can be recalled instantly.

        :param settings PDTileMatrixProfileTuple
        profile_number: memory location to store profile settings in (0-4)
        h_monitors: number of columns (1-10)
        v_monitors: number of rows (1-10)
        position: position of this display (from top left) (1-100)
        tile_comp: use tile compensation (1=off 2=on)
        :return:
        """
        logging.debug('profile_number=%i h_monitors=%i v_monitors=%i position=%i tile_comp=%i',
                      settings.profile_number,
                      settings.h_monitors,
                      settings.v_monitors,
                      settings.position,
                      settings.tile_comp)
        assert 0 <= settings.profile_number <= 4
        assert 1 <= settings.h_monitors <= 10
        assert 1 <= settings.v_monitors <= 10
        assert 1 <= settings.position <= 100
        assert 1 <= settings.tile_comp <= 2
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA17))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        send_data.extend(ascii_encode_value_2_bytes(settings.profile_number))
        send_data.extend(ascii_encode_value_2_bytes(settings.h_monitors))
        send_data.extend(ascii_encode_value_2_bytes(settings.v_monitors))
        send_data.extend(ascii_encode_value_2_bytes(settings.position))
        send_data.extend(ascii_encode_value_2_bytes(settings.tile_comp))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB17):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_tile_matrix_profile_contents_read(self, profile_number):
        """
        Reads the Tile Matrix settings from a memory location (profile number).

        :param profile_number:
        :return: PDTileMatrixProfileTuple
        profile_number: memory location to store profile settings in (0-4)
        h_monitors: number of columns (1-10)
        v_monitors: number of rows (1-10)
        position: position of this display (from top left) (1-100)
        tile_comp: use tile compensation (1=off 2=on)
        """
        logging.debug('profile_number=%i', profile_number)
        assert 0 <= profile_number <= 4
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA17))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(profile_number))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 18:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB17):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            offset = 8
            # profile_number
            parameter_len = 2
            profile_number = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # h_monitors
            parameter_len = 2
            h_monitors = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # v_monitors
            parameter_len = 2
            v_monitors = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # position
            parameter_len = 2
            position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # tile_comp
            parameter_len = 2
            tile_comp = ascii_decode_value(reply_data[offset:offset + parameter_len])
            return PDTileMatrixProfileTuple(profile_number=profile_number,
                                            h_monitors=h_monitors,
                                            v_monitors=v_monitors,
                                            position=position,
                                            tile_comp=tile_comp)
        else:
            logging.error('unexpected reply length: %i (expected 18)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_tile_matrix_profile_write(self, profile_number):
        """
        Selects the Tile Matrix settings from a memory location (profile number).

        :param profile_number: memory location to select profile settings from (0-4)
        :return:
        """
        logging.debug('profile_number=%i', profile_number)
        assert 0 <= profile_number <= 4
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA17))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        send_data.extend(ascii_encode_value_2_bytes(profile_number))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB17):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_pbp_pip_profile_contents_write(self, settings):
        """
        Saves PIP/PBP settings into a memory so that they can be recalled instantly.

        :param settings PDPIPPBPProfileTuple
        profile_number: memory location to store profile settings in (0-4)

        :return:
        """
        logging.debug('profile_number=%i pip_pbp_mode=%i', settings.profile_number, settings.pip_pbp_mode)
        logging.debug('picture1_input=%i picture2_input=%i picture3_input=%i picture4_input=%i',
                      settings.picture1_input,
                      settings.picture2_input,
                      settings.picture3_input,
                      settings.picture4_input)
        logging.debug('picture1_size=%i picture2_size=%i picture3_size=%i picture4_size=%i',
                      settings.picture1_size,
                      settings.picture2_size,
                      settings.picture3_size,
                      settings.picture4_size)
        logging.debug('picture1_aspect=%i picture2_aspect=%i picture3_aspect=%i picture4_aspect=%i',
                      settings.picture1_aspect,
                      settings.picture2_aspect,
                      settings.picture3_aspect,
                      settings.picture4_aspect)
        logging.debug('picture1_h_position=%i picture2_h_position=%i picture3_h_position=%i picture4_h_position=%i',
                      settings.picture1_h_position,
                      settings.picture2_h_position,
                      settings.picture3_h_position,
                      settings.picture4_h_position)
        logging.debug('picture1_v_position=%i picture2_v_position=%i picture3_v_position=%i picture4_v_position=%i',
                      settings.picture1_v_position,
                      settings.picture2_v_position,
                      settings.picture3_v_position,
                      settings.picture4_v_position)
        logging.debug('reserved_11=%i reserved_12=%i reserved_13=%i reserved_14=%i reserved_15=%i reserved_16=%i',
                      settings.reserved_11,
                      settings.reserved_12,
                      settings.reserved_13,
                      settings.reserved_14,
                      settings.reserved_15,
                      settings.reserved_16)
        logging.debug('reserved_17=%i reserved_18=%i reserved_19=%i reserved_20=%i reserved_21=%i reserved_22=%i',
                      settings.reserved_17,
                      settings.reserved_18,
                      settings.reserved_19,
                      settings.reserved_20,
                      settings.reserved_21,
                      settings.reserved_22)

        assert 0 <= settings.profile_number <= 4

        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA20))
        send_data.extend(ascii_encode_value_2_bytes(0x00))
        send_data.extend(ascii_encode_value_2_bytes(settings.profile_number))
        send_data.extend(ascii_encode_value_2_bytes(settings.pip_pbp_mode))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture1_input))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture2_input))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture3_input))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture4_input))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture1_size))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture2_size))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture3_size))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture4_size))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture1_aspect))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture2_aspect))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture3_aspect))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture4_aspect))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture1_h_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture2_h_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture3_h_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture4_h_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture1_v_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture2_v_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture3_v_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.picture4_v_position))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_11))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_12))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_13))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_14))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_15))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_16))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_17))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_18))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_19))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_20))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_21))
        send_data.extend(ascii_encode_value_2_bytes(settings.reserved_22))

        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB20):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x00):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    @retry
    def command_pbp_pip_profile_contents_read(self, profile_number):
        """
        Reads the PIP/PBP  settings from a memory location (profile number).

        :param profile_number:
        :return: PDPIPPBPProfileTuple
        """
        logging.debug('profile_number=%i', profile_number)
        assert 0 <= profile_number <= 4
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA20))
        send_data.extend(ascii_encode_value_2_bytes(0x01))
        send_data.extend(ascii_encode_value_2_bytes(profile_number))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 52:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB20):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x01):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
            offset = 8
            # profile_number
            parameter_len = 2
            profile_number = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # pip_pbp_mode
            pip_pbp_mode = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len        
            # picture1_input
            picture1_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture2_input
            picture2_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture3_input
            picture3_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture4_input
            picture4_input = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len            
            # picture1_size
            picture1_size = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture2_size
            picture2_size = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture3_size
            picture3_size = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture4_size
            picture4_size = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len            
            # picture1_aspect
            picture1_aspect = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture2_aspect
            picture2_aspect = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture3_aspect
            picture3_aspect = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture4_aspect
            picture4_aspect = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len            
            # picture1_h_position
            picture1_h_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture2_h_position
            picture2_h_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture3_h_position
            picture3_h_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture4_h_position
            picture4_h_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len            
            # picture1_v_position
            picture1_v_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture2_v_position
            picture2_v_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture3_v_position
            picture3_v_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # picture4_v_position
            picture4_v_position = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_11
            reserved_11 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_12
            reserved_12 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_13
            reserved_13 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_14
            reserved_14 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_15
            reserved_15 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_16
            reserved_16 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_17
            reserved_17 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_18
            reserved_18 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_19
            reserved_19 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_20
            reserved_20 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_21
            reserved_21 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len
            # reserved_22
            reserved_22 = ascii_decode_value(reply_data[offset:offset + parameter_len])
            offset += parameter_len

            return PDPIPPBPProfileTuple(profile_number=profile_number,
                                        pip_pbp_mode=pip_pbp_mode,
                                        picture1_input=picture1_input,
                                        picture2_input=picture2_input,
                                        picture3_input=picture3_input,
                                        picture4_input=picture4_input,
                                        picture1_size=picture1_size,
                                        picture2_size=picture2_size,
                                        picture3_size=picture3_size,
                                        picture4_size=picture4_size,
                                        picture1_aspect=picture1_aspect,
                                        picture2_aspect=picture2_aspect,
                                        picture3_aspect=picture3_aspect,
                                        picture4_aspect=picture4_aspect,
                                        picture1_h_position=picture1_h_position,
                                        picture2_h_position=picture2_h_position,
                                        picture3_h_position=picture3_h_position,
                                        picture4_h_position=picture4_h_position,
                                        picture1_v_position=picture1_v_position,
                                        picture2_v_position=picture2_v_position,
                                        picture3_v_position=picture3_v_position,
                                        picture4_v_position=picture4_v_position,
                                        reserved_11=reserved_11,
                                        reserved_12=reserved_12,
                                        reserved_13=reserved_13,
                                        reserved_14=reserved_14,
                                        reserved_15=reserved_15,
                                        reserved_16=reserved_16,
                                        reserved_17=reserved_17,
                                        reserved_18=reserved_18,
                                        reserved_19=reserved_19,
                                        reserved_20=reserved_20,
                                        reserved_21=reserved_21,
                                        reserved_22=reserved_22)
        else:
            logging.error('unexpected reply length: %i (expected 52)', len(reply_data))
            raise unexpectedReply

    @retry
    def command_pbp_pip_profile_write(self, profile_number):
        """
        Selects the PIP/PBP settings from a memory location (profile number).

        :param profile_number: memory location to select profile settings from (0-4)
        :return:
        """
        logging.debug('profile_number=%i', profile_number)
        assert 0 <= profile_number <= 4
        send_data = []
        send_data.extend(ascii_encode_value_4_bytes(0xCA20))
        send_data.extend(ascii_encode_value_2_bytes(0x02))
        send_data.extend(ascii_encode_value_2_bytes(profile_number))
        write_command(self.f, send_data, self.destination_address, 0x41)
        reply_data, reply_message_type, reply_destination_address = read_command_reply(self.f, True)
        if len(reply_data) == 8:
            if reply_message_type != 0x42:
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[0:4] != ascii_encode_value_4_bytes(0xCB20):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if reply_data[4:6] != ascii_encode_value_2_bytes(0x02):
                logging.error('unexpected reply received')
                raise unexpectedReply
            if ascii_decode_value(reply_data[6:8]) != 0:
                logging.error('reply status is not 0')
                raise commandStatusReturnedError
        else:
            logging.error('unexpected reply length: %i (expected 8)', len(reply_data))
            raise unexpectedReply
        return

    def helper_get_long_power_on_hours(self):
        """
        Reads the total power on time in minutes using new 2 x 32 bit opcodes.
        Note: Normally use the function "helper_get_power_on_hours" instead of calling this directly

        :return: power on hours as a value
        """
        logging.debug('')
        reply = self.command_get_parameter(OPCODE_OPERATING_TIME_ON__UPPER___MINUTES___READ_ONLY_)
        if reply.result == 0:
            minutes = reply.current_value << 16
            logging.debug('high word = %04Xh', reply.current_value)
            reply = self.command_get_parameter(OPCODE_OPERATING_TIME_ON__LOWER___MINUTES___READ_ONLY_)
            if reply.result == 0:
                minutes += reply.current_value
                logging.debug('low word = %04Xh', reply.current_value)
                logging.debug('minutes = %i', minutes)
                return minutes / 60.0
        return

    def helper_get_long_total_operating_hours(self):
        """
        Reads the total operating time in minutes using new 2 x 32 bit opcodes.
        Note: Normally use the function "helper_get_total_operating_hours" instead of calling this directly

        :return: total operating hours as a value
        """
        logging.debug('')
        reply = self.command_get_parameter(OPCODE_TOTAL_OPERATING_TIME__UPPER___MINUTES___READ_ONLY_)
        if reply.result == 0:
            minutes = reply.current_value << 16
            logging.debug('high word = %04Xh', reply.current_value)
            reply = self.command_get_parameter(OPCODE_TOTAL_OPERATING_TIME__LOWER___MINUTES___READ_ONLY_)
            if reply.result == 0:
                minutes += reply.current_value
                logging.debug('low word = %04Xh', reply.current_value)
                logging.debug('minutes = %i', minutes)
                return minutes / 60.0
        return

    def helper_get_power_on_hours(self):
        """
        Reads the total power on hours. First tries to read using the new 64 bit minutes values.
        If that fails it reads using the standard 32 bit 0.5 hour value.

        :return: power on hours as a value
        """
        logging.debug('')
        hours = self.helper_get_long_power_on_hours()
        if hours is not None:
            return hours
        return self.command_get_parameter(OPCODE_OPERATING_TIME_ON_30_MIN_READ_ONLY).current_value / 2.0

    def helper_get_total_operating_hours(self):
        """
        Reads the total operating hours. First tries to read using the new 64 bit minutes values.
        If that fails it reads using the standard 32 bit 0.5 hour value.

        :return: total operating hours as a value
        """
        logging.debug('')
        hours = self.helper_get_long_total_operating_hours()
        if hours is not None:
            return hours
        return self.command_get_parameter(OPCODE_TOTAL_OPERATING_TIME_30_MIN_READ_ONLY).current_value / 2.0

    def helper_get_temperature_sensor_values(self):
        """
        Gets the temperature values in 'c for all available temperature sensors.

        :return: a list of values in 'c corresponding to each sensor
        """
        logging.debug('')
        temperatures = []
        reply = self.command_get_parameter(OPCODE_SELECT_TEMPERATURE_SENSOR)
        if reply.result == 0x00:  # supported
            for x in range(0, reply.max_value):
                self.command_set_parameter(OPCODE_SELECT_TEMPERATURE_SENSOR, x+1)
                temperatures.append(
                    self.command_get_parameter(OPCODE_READ_TEMPERATURE_SENSOR_READ_ONLY).current_value / 2.0)
            return temperatures
        return

    def helper_get_fan_statuses(self):
        """
        Gets the fan status for all available fans.

        :return: a list of the text status of each available fan
        """
        logging.debug('')
        status = []
        reply = self.command_get_parameter(OPCODE_FAN__FAN_SELECT)
        if reply.result == 0x00:  # supported
            for x in range(0, reply.max_value):
                self.command_set_parameter(OPCODE_FAN__FAN_SELECT, x+1)
                value = self.command_get_parameter(OPCODE_FAN__FAN_STATUS_READ_ONLY).current_value
                if value in DISPLAY_FAN_STATUS:
                    status.append(DISPLAY_FAN_STATUS[value])
                else:
                    status.append("Unknown")
            return status
        return

    def helper_self_diagnosis_status_text(self):
        """
        Performs "command_self_diagnosis_status_read" and formats the reply into
        a string of the decoded error code(s).

        :return: single string with decoded error codes separated by ';'
        """
        logging.debug('')
        text = ""
        result_codes = self.command_self_diagnosis_status_read()
        for code in result_codes:
            try:
                text += (DISPLAY_DIAGNOSTIC_ERROR_CODES[code]) + "; "
            except KeyError:
                text += ("Unknown error code - " + hex(code)) + "; "
        return text

    def helper_timing_report_text(self):
        """
        Performs "command_get_timing_report" and formats into a readable string.

        :return: string with timing information
        """
        logging.debug('')
        text = ""
        status_byte, h_freq, v_freq = self.command_get_timing_report()
        text += "H Frequency: " + str(h_freq/100.0) + " kHz, "
        text += "V Frequency: " + str(v_freq/100.0) + " Hz, "
        if status_byte & 0x80:
            text += "Out of range, "
        if status_byte & 0x40:
            text += "Unstable, "
        if status_byte & 0x02:
            text += "+H Sync, "
        else:
            text += "-H Sync, "
        if status_byte & 0x01:
            text += "+V Sync"
        else:
            text += "-V Sync"
        return text

    def helper_asset_data_read(self):
        """
        Helper function that reads the entire asset data string by combining chunks using
        "command_asset_data_read".

        :return:
        """
        logging.debug('')
        return self.command_asset_data_read(0) + self.command_asset_data_read(32)

    def helper_asset_data_write(self, in_string):
        """
        Helper function that writes the asset data string as chunks.

        :param in_string:
        :return:
        """
        logging.debug('in_string=%s', in_string)
        self.command_asset_data_write(0, in_string[0:32])
        self.command_asset_data_write(32, in_string[32:64])
        return

    def helper_set_destination_monitor_id(self, monitor_id):
        """
        Helper function to set the Monitor ID.

        :param monitor_id: Can be specified as a number in the range 1-100, or "All", or "A"-"J" for a group
        :return:
        """
        logging.debug('')
        address = 0
        try:
            value = int(monitor_id)
            if 1 <= value <= 100:
                address = 0x41 + value - 1
            else:
                assert 0
        except ValueError:
            if monitor_id.lower() == "all":
                address = 0x2a
            elif len(monitor_id) == 1 & ("a" <= monitor_id.lower() <= "j"):
                address = ord(monitor_id.lower()[0]) - 0x61 + 0x31
            else:
                assert 0
        self.set_destination_address(address)

    def helper_send_ir_remote_control_codes(self, codes):
        """
        Helper function that takes a list of IR codes to send.

        :param codes: list of codes
        :return:
        """
        logging.debug('')
        for code in codes:
            self.command_send_ir_remote_control_code(PD_IR_COMMAND_CODES[code])

    def helper_date_and_time_write(self, in_datetime, in_daylight_savings=0):
        """
        Helper function for helper_date_and_time_write that takes a 'datetime'.

        :param in_datetime: a Python datetime
        :param in_daylight_savings:
        :return: same as command_date_and_time_write
        """
        logging.debug('')
        param = PDDateTimeTuple(year=in_datetime.year-2000,
                                month=in_datetime.month,
                                day=in_datetime.day,
                                weekday=0,
                                hour=in_datetime.hour,
                                minute=in_datetime.minute,
                                daylight_savings=in_daylight_savings,
                                status=0)
        return self.command_date_and_time_write(param)

    def helper_date_and_time_write_keep_daylight_savings_setting(self, in_datetime):
        """
        Helper function for helper_date_and_time_write that takes a 'datetime' but maintains the current
        daylight savings on/off setting currently in the display

        :param in_datetime: a Python datetime
        :return: same as command_date_and_time_write
        """
        logging.debug('')
        value = self.command_date_and_time_read()

        param = PDDateTimeTuple(year=in_datetime.year-2000,
                                month=in_datetime.month,
                                day=in_datetime.day,
                                weekday=0,
                                hour=in_datetime.hour,
                                minute=in_datetime.minute,
                                daylight_savings=value.daylight_savings,
                                status=0)
        return self.command_date_and_time_write(param)

    def helper_date_and_time_read(self):
        """
        Performs "command_date_and_time_read" and converts the reply to a Python datetime.

        :return: a datetime of "command_date_and_time_read", daylight_savings
        """
        logging.debug('')
        value = self.command_date_and_time_read()
        return datetime.datetime(value.year + 2000,
                                 value.month,
                                 value.day,
                                 value.hour,
                                 value.minute), value.daylight_savings

    def helper_set_parameter_as_percentage(self, opcode, percent):
        """
        Sets an opcode based control to a value specified as a percentage value
        by reading the control to find the maximum then calculating the new value.
        Note: This assumes that the control range starts from 0 and is continuous in range.

        :param opcode: opcode to set
        :param percent: value to set as a percentage
        :return:
        """
        assert 0 <= percent <= 100
        logging.debug('opcode=%04xh percent=%i', opcode, percent)
        get_reply = self.command_get_parameter(opcode)
        value = int(percent * get_reply.max_value / 100.0)
        return self.command_set_parameter(opcode, value)

    def helper_capabilities_request(self):
        """
        Reads the entire capability string from the display.

        :return: the capability string
        """
        logging.debug('')
        offset = 0
        capability_string = ""
        while True:
            capability_string_in = self.command_capabilities_request(offset)
            capability_string += capability_string_in
            if len(capability_string_in) != 32:
                break
            offset += 32
        return capability_string

    def helper_firmware_versions_list(self):
        """
        Reads the firmware version(s) from the display. If the display doesn't support
        'command_firmware_version_read' then it reads the capability string and parses
        it to get the version from the 'mpu_ver()'.

        :return: a list of firmware version strings
        """
        logging.debug('')
        reply = []
        for x in range(0, 4):
            try:
                reply.append(self.command_firmware_version_read(x).rstrip())
            except (PDNullMessageReplyError,  PDCommandNotSupportedError):
                # older monitor may not support, so try to read from capability string
                cap_string = self.helper_capabilities_request()
                index_start = string.find(cap_string, "mpu_ver(")
                index_end = string.find(cap_string, ")", index_start)
                if index_start > 0 and index_end > 0:
                    reply.append(cap_string[index_start+len("mpu_ver("):index_end])
                    return reply
                raise PDCommandNotSupportedError
        return reply

    def helper_get_proof_of_play_current(self):
        """
        Reads the latest proof of play log from the the display and returns the date & time as a Python datetime.

        :return: PDHelperProofOfPlayLogItemTuple
        """
        logging.debug('')
        reply = self.command_get_proof_of_play_current()
        return PDHelperProofOfPlayLogItemTuple(status=reply.status,
                                               log_number=reply.log_number,
                                               input=reply.input,
                                               signal_h_resolution=reply.signal_h_resolution,
                                               signal_v_resolution=reply.signal_v_resolution,
                                               audio_input=reply.audio_input,
                                               audio_input_status=reply.audio_input_status,
                                               picture_status=reply.picture_status,
                                               audio_status=reply.audio_status,
                                               date_time=datetime.datetime(reply.year, reply.month, reply.day,
                                                                           reply.hour, reply.minute),
                                               reserved_1=reply.reserved_1,
                                               reserved_2=reply.reserved_2,
                                               reserved_3=reply.reserved_3)

    def helper_get_proof_of_play_number(self, number):
        """
        Reads a specific proof of play log from the the display and returns the date & time as a Python datetime.
        Note: only support reading 1 log at a time.

        :param number: log number to read (1=first)
        :return: PDHelperProofOfPlayLogItemTuple
        """

        logging.debug('number=%i', number)
        reply = self.command_get_proof_of_play_number_to_number(number, number)
        return PDHelperProofOfPlayLogItemTuple(status=reply.status,
                                               log_number=reply.log_number,
                                               input=reply.input,
                                               signal_h_resolution=reply.signal_h_resolution,
                                               signal_v_resolution=reply.signal_v_resolution,
                                               audio_input=reply.audio_input,
                                               audio_input_status=reply.audio_input_status,
                                               picture_status=reply.picture_status,
                                               audio_status=reply.audio_status,
                                               date_time=datetime.datetime(reply.year, reply.month, reply.day,
                                                                           reply.hour, reply.minute),
                                               reserved_1=reply.reserved_1,
                                               reserved_2=reply.reserved_2,
                                               reserved_3=reply.reserved_3)


    def helper_read_schedules(self):
        """
        Helper function to read all the schedules and return them as a list of schedules

        :return: A list of PDScheduleTuple
        """

        reply = []
        for x in range (1, 7):
            reply.append(self.command_schedule_read(x))

        return reply

    def helper_read_advanced_schedules(self):
        """
        Helper function to read all the advanced schedules and return them as a list of schedules

        :return: A list of PDAdvancedScheduleTuple
        """

        reply = []
        for x in range (1, 30):
            reply.append(self.command_advanced_schedule_read(x))

        return reply

    def helper_read_holidays(self):
        """
        Helper function to reall all the holidays and return them as a list of holidays

        :return: A list of PDHolidayTuple
        """

        reply = []
        for x in range (1, 50):
            reply.append(self.command_holiday_read(x))

        return reply

    def helper_advanced_schedule_is_empty(self, schedule):
        """
        Helper function to determin if the schedule is empty

        :param schedule: Schedule
        :return: True if the scheule is empty
        """

        reply = False
        if schedule.hour == 24 and schedule.minute == 60:
            reply = True

        return reply
    
    def helper_advanced_schedule_is_enabled(self, schedule):
        """
        Helper function to determin if the schedule is enabled

        :param schedule: Schedule
        :return: True if the scheule is enabled
        """

        reply = False
        if schedule.type & 0x04:
            reply = True

        return reply

    def helper_advanced_schedule_is_every_day(self, schedule):
        """
        Helper function to determine if the schedule type is Every Day

        :param schedule: Schedule 
        :return: True if the schedule type is every day.
        """
   
        reply = False
        if schedule.type & 0x01:
            reply = True

        return reply

    def helper_advanced_schedule_is_every(self, schedule):
        """
        Helper function to determine if the schedule type is Every 

        :param schedule: Schedule 
        :return: True if the schedule type is every 
        """
   
        reply = False
        if schedule.type & 0x02 and schedule.week != 0:
            reply = True

        return reply

    def helper_advanced_schedule_is_specific_days(self, schedule):
        """
        Helper function to determine if the schedule type is Specific Days 

        :param schedule: Schedule 
        :return: True if the schedule type is specific days 
        """
   
        reply = False
        if schedule.type & 0x02 and schedule.week == 0:
            reply = True

        return reply

    def helper_advanced_schedule_is_weekdays(self, schedule):
        """
        Helper function to determine if the schedule type is Weekdays

        :param schedule: Schedule 
        :return: True if the schedule type is Weekdays
        """
   
        reply = False
        if schedule.type & 0x08: 
            reply = True

        return reply
 
    def helper_advanced_schedule_is_weekends(self, schedule):
        """
        Helper function to determine if the schedule type is Weekends

        :param schedule: Schedule 
        :return: True if the schedule type is Weekends
        """
   
        reply = False
        if schedule.type & 0x10: 
            reply = True

        return reply
 
    def helper_advanced_schedule_is_holidays(self, schedule):
        """
        Helper function to determine if the schedule type is holidays

        :param schedule: Schedule 
        :return: True if the schedule type is holidays
        """
   
        reply = False
        if schedule.type & 0x20: 
            reply = True

        return reply
 
    def helper_advanced_schedule_is_one_day(self, schedule):
        """
        Helper function to determine if the schedule type is one_day

        :param schedule: Schedule 
        :return: True if the schedule type is one_day
        """
   
        reply = False
        if schedule.type & 0x40: 
            reply = True

        return reply
 
    def helper_advanced_schedule_type_string(self, schedule):
        """
        Helper function to return the type string

        :param schedule: Schedule
        :return: Type string
        """

        str = ""
        if schedule.type & 0x01:
            str = "Every Day"
        elif schedule.type & 0x02:
            if schedule.week != 0:
                str = "Every "
            else:
                str = "Specific Days"
        elif schedule.type & 0x08:
            str = "Weekdays"
        elif schedule.type & 0x10:
            str = "Weekends"
        elif schedule.type & 0x20:
            str = "Holidays"
        elif schedule.type & 0x40:
            str = "One Day on "

        return str

    def helper_advanced_schedule_week_string(self, week):
        """
        Helper function to get the week string

        :param week: Schedule week
        :return: Week String such as "Mon, Tues, Fri"
        """

        str = ""
        if week & 0x01:
            str += "Mon"
        if week & 0x02:
            if str != "":
                str += ", "
            str += "Tues" 
        if week & 0x04:
            if str != "":
                str += ", "
            str += "Wed"
        if week & 0x08:
            if str != "":
                str += ", "
            str += "Thurs"
        if week & 0x10:
            if str != "":
                str != ", "
            str += "Fri"
        if week & 0x20:
            if str != "":
                str += ", "
            str += "Sat"
        if week & 0x40:
            if str != "":
                str += ", "
            str += "Sun"

        return str;

    def helper_advanced_schedule_set_type(self, type, enable):
        """
        Set the schedule type.  If enable is True, then also include
        the enable bit in the schedule.

        :param type: Type of schedule.  See the class PDSchedule for types
        :param enable: If True, also enable the schedule
        :return: The Schedule Type
        """

        schedType = type;
        if enable == True:
            schedType += PDSchedule.Enabled

        return schedType

    def helper_advanced_schedule_set_week(self, week):
        """
        Set the week.

        :param week: Array of Days to set
        :return: The week 
        """

        days = 0
        for day in week:
            days += day

        return days
