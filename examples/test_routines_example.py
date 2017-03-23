"""test_raspberry_pi.py - Test routines and sample code for communicating via LAN or RS232 with NEC large-screen displays
using the NEC PD SDK.
Revision: 170317
"""
#
#
# Copyright (C) 2016-17 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.
#

from __future__ import print_function
import logging

from nec_pd_sdk.nec_pd_sdk import NECPD
from nec_pd_sdk.protocol import PDError
from nec_pd_sdk.protocol import PDUnexpectedReplyError
from nec_pd_sdk.constants import *
from nec_pd_sdk.opcode_decoding import *


def reverse_dict(d):
    return dict(zip(d.values(), d.keys()))


def do_main_tests(pd):
    try:
        print("Testing: command_model_name_read")
        value = pd.command_model_name_read()
        print("command_model_name_read value:", value)

        print("Testing: command_serial_number_read")
        value = pd.command_serial_number_read()
        print("command_serial_number_read value:", value)

        print("Testing: helper_get_power_on_hours")
        print("power on hours: ", pd.helper_get_power_on_hours())

        print("Testing: helper_get_total_operating_hours")
        print("total operating hours: ", pd.helper_get_total_operating_hours())

        print("Testing: helper_get_temperature_sensor_values")
        print("helper_get_temperature_sensor_values: ", pd.helper_get_temperature_sensor_values())

        print("Testing: helper_get_fan_statuses")
        print("helper_get_fan_statuses: ", pd.helper_get_fan_statuses())

        print("Testing: command_power_status_read")
        state = pd.command_power_status_read()
        pd_power_states_rev = reverse_dict(PD_POWER_STATES)
        if state in pd_power_states_rev:
            print("power state: ", pd_power_states_rev[state])
        else:
            print("power state: Unknown state")

        print("Testing: helper_firmware_versions_list")
        text_list = pd.helper_firmware_versions_list()
        ver_num = 0
        for text in text_list:
            ver_num += 1
            print("helper_firmware_versions_list: FW#", ver_num, "=", text)

        print("Testing: helper_set_parameter_as_percentage")
        reply = pd.helper_set_parameter_as_percentage(OPCODE_PICTURE__BRIGHTNESS, 50)
        print("helper_set_parameter_as_percentage result:", reply.result, "opcode:", hex(reply.opcode), "type:",
              reply.type, "max_value:", reply.max_value, "current_value:", reply.current_value)

        print("Testing: command_get_parameter")
        reply = pd.command_get_parameter(OPCODE_PICTURE__BRIGHTNESS)
        print("command_get_parameter result:", reply.result, "opcode:", hex(reply.opcode), "type:", reply.type,
              "max_value:", reply.max_value, "current_value:", reply.current_value)

        print("Testing: command_set_parameter")
        reply = pd.command_set_parameter(OPCODE_PICTURE__BRIGHTNESS, reply.current_value)
        print("command_set_parameter result:", reply.result, "opcode:", hex(reply.opcode), "type:", reply.type,
              "max_value:", reply.max_value, "current_value:", reply.current_value)

        print("Testing: helper_self_diagnosis_status_text")
        text_list = pd.helper_self_diagnosis_status_text()
        print("Diagnostics:", text_list)

        print("Testing: helper_timing_report_text")
        text_list = pd.helper_timing_report_text()
        print("helper_timing_report_text:", text_list)

        print("Testing: helper_asset_data_read")
        text_list = pd.helper_asset_data_read()
        print("helper_asset_data_read:", text_list)

        print("Testing: helper_date_and_time_read")
        value, daylight_savings = pd.helper_date_and_time_read()
        print("helper_date_and_time_read.datetime:", str(value), "daylight_savings:", daylight_savings)

        # try reading all of the opcodes that we know about
        for x in get_opcode_list():
            reply = pd.command_get_parameter(x)
            print("command_get_parameter Opcode 0x", '%04x' % reply.opcode, sep='', end="")
            name = opcode_to_nice_name(reply.opcode)

            if name is not None:
                print(" ('", name, "') ", sep='', end="")
            else:
                print(" (not in opcode_values_to_name_dict!)")

            print("Result:", reply.result, end="")
            if reply.result == 0:  # opcode is supported
                print(" (Supported) ", end="")
                # print(" result:", reply.result, end="")
                print("Type:", reply.type, end="")
                if reply.type == 0:
                    print(" (Set Parameter) ", end="")
                else:
                    print(" (Momentary) ", end="")

                print("Max:", reply.max_value, "Current:", reply.current_value, end="")

                name = opcode_value_to_nice_value_name(reply.opcode, reply.current_value)
                if name is not None:
                    print(" ('", name, "')", sep='', end="")
            else:
                print(" (Unsupported) ", end="")
            print("")

    except PDUnexpectedReplyError as msg:
        print("PDUnexpectedReplyError:", msg)
    except PDError as msg:
        print("PDError:", msg)
    return


# change the following to the UART / COM port / IP address of the display
# port = "/dev/ttyS0" # Raspberry Pi 3 (since /ttyAMA0 used for Bluetooth)
# port = "/dev/ttyAMA0" # Raspberry Pi 1&2
# port = '192.168.1.140' # for an IP address
# port = "/dev/ttyS0"
port = '10.0.0.18'

# set the Monitor ID to communicate with
# can also use Groups such as "A", and "All"
monitor_id = 1



def main():
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    # load the opcode dictionary from file
    load_opcode_dict()

    print("Using port:", port)

    try:
        pd = NECPD.open(port)
        pd.helper_set_destination_monitor_id(monitor_id)

        try:
            do_main_tests(pd)
            print("Testing: Finished!")

        finally:
            # make sure to always close
            pd.close()

    except PDError as msg:
        print("PDError:", msg)
    return


if __name__ == '__main__':
    main()
exit()
