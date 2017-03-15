"""test_routines.py - Test routines and sample code for communicating via LAN or RS232 with NEC large-screen displays
using the NEC PD SDK.
"""
#
#
# Copyright (C) 2016 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
#

from __future__ import print_function

import logging
import datetime

from nec_pd_sdk import NECPD
from protocol import PDError
from protocol import PDCommandNotSupportedError
from protocol import PDUnexpectedReplyError
from protocol import PDCommandStatusReturnedError
from protocol import PDTimeoutError
from constants import *
from opcode_decoding import *
from nec_pd_sdk import PDTileMatrixProfileTuple
from nec_pd_sdk import PDPIPPBPProfileTuple
from nec_pd_sdk import PDAutoTileMatrixTuple
# import string


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

        print("Testing: command_self_diagnosis_status_read")
        value = pd.command_self_diagnosis_status_read()
        print("command_self_diagnosis_status_read value:", value)

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

        # print("Testing: helper_asset_data_write")
        # pd.helper_asset_data_write("1234567890!@#$%^&*()12345678901298765432109876543210987654321021")

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


def do_auto_tile_matrix_tests(pd):
    try:
        print("Testing: command_auto_tile_matrix_read")
        h_monitors, v_monitors = pd.command_auto_tile_matrix_read()
        print("command_auto_tile_matrix_read:", h_monitors, v_monitors)

        print("Testing: command_auto_tile_matrix_write")
        value = pd.command_auto_tile_matrix_write(h_monitors, v_monitors)
        print("command_auto_tile_matrix_write:", value)

        print("Testing: command_auto_tile_matrix_reset")
        value = pd.command_auto_tile_matrix_reset()
        print("command_auto_tile_matrix_reset:", value)

        print("Testing: command_auto_tile_matrix_read")
        h_monitors, v_monitors = pd.command_auto_tile_matrix_read()
        print("command_auto_tile_matrix_read:", h_monitors, v_monitors)

        print("Testing: command_auto_tile_matrix_execute")
        value = pd.command_auto_tile_matrix_execute(PDAutoTileMatrixTuple(h_monitors=10,
                                                                          v_monitors=10,
                                                                          pattern_id=1,
                                                                          current_input_select=136,
                                                                          tile_matrix_mem=0))
        print("command_auto_tile_matrix_execute:", value)

        # print("Testing: command_auto_tile_matrix_complete")
        # value = pd.command_auto_tile_matrix_complete()
        # print("command_auto_tile_matrix_complete:", value)

    except PDCommandStatusReturnedError as msg:
        print("Error do_auto_tile_matrix_tests returned error status: ", msg)
    except PDCommandNotSupportedError as msg:
        print("Error do_auto_tile_matrix_tests: ", msg)
    return


def do_daylight_savings_tests(pd):
    try:
        print("Testing: command_daylight_savings_on_off_read")
        value = pd.command_daylight_savings_on_off_read()
        print("command_daylight_savings_on_off_read:", value)

        print("Testing: command_daylight_savings_on_off_write")
        value = pd.command_daylight_savings_on_off_write(value)
        print("command_daylight_savings_on_off_write:", value)

        try:
            print("Testing: command_daylight_savings_read")
            value = pd.command_daylight_savings_read()
            print("command_daylight_savings_read status:", value.status,
                  "begin_month:", value.begin_month,
                  "begin_day1:", value.begin_day1,
                  "begin_day2:", value.begin_day2,
                  "begin_time_hour:", value.begin_time_hour,
                  "begin_time_minute:", value.begin_time_minute,
                  "end_month:", value.end_month,
                  "end_day1:", value.end_day1,
                  "end_day2:", value.end_day2,
                  "end_time_hour:", value.end_time_hour,
                  "end_time_minute:", value.end_time_minute,
                  "time_difference:", value.time_difference)

            print("Testing: command_daylight_savings_write")
            pd.command_daylight_savings_write(value)

        except PDCommandNotSupportedError as msg:
            print("Error daylight_savings ", msg)

    except PDCommandNotSupportedError as msg:
        print("Error do_daylight_savings_tests: ", msg)
    return


def do_auto_id_tests(pd):
    try:
        print("Testing: command_auto_id_reset")
        value = pd.command_auto_id_reset()
        print("command_auto_id_reset value:", value)

        print("Testing: command_auto_id_execute")
        pd.command_auto_id_execute()

        print("Testing: command_auto_id_complete_notify")
        value = pd.command_auto_id_complete_notify()
        print("command_auto_id_complete_notify value:", value)
    except PDTimeoutError as msg:
        print("Error do_auto_id_tests: ", msg)
    except PDCommandNotSupportedError as msg:
        print("Error do_auto_id_tests: ", msg)
    return


def do_input_name_tests(pd):
    try:
        print("Testing: command_input_name_read")
        value = pd.command_input_name_read()
        print("command_input_name_read value:", value)
    except PDCommandNotSupportedError as msg:
        print("Error:", msg)

    try:
        print("Testing: command_input_name_write")
        value = pd.command_input_name_write("87654321")
        print("command_input_name_write value:", value)
    except PDCommandNotSupportedError as msg:
        print("Error:", msg)

    try:
        print("Testing: command_input_name_read")
        value = pd.command_input_name_read()
        print("command_input_name_read value:", value)
    except PDCommandNotSupportedError as msg:
        print("Error:", msg)

    try:
        print("Testing: command_input_name_reset")
        value = pd.command_input_name_reset()
        print("command_input_name_reset value:", value)
    except PDCommandNotSupportedError as msg:
        print("Error:", msg)

    try:
        print("Testing: command_input_name_read")
        value = pd.command_input_name_read()
        print("command_input_name_read value:", value)
    except PDCommandNotSupportedError as msg:
        print("Error:", msg)
    return


def do_direct_tv_channel_tests(pd):
    try:
        print("Testing: command_direct_tv_channel_read")
        major, minor = pd.command_direct_tv_channel_read()
        print("command_direct_tv_channel_read:", major, "-", minor)

        set_major = 13
        set_minor = 1
        print("Testing: command_direct_tv_channel_write")
        major, minor = pd.command_direct_tv_channel_write(set_major, set_minor)
        print("command_direct_tv_channel_write:", major, "-", minor)
    except PDCommandNotSupportedError as msg:
        print("Error direct_tv_channel ", msg)
    return


def do_capability_string_tests(pd):
    try:
        print("Testing: helper_capabilities_request")
        string = pd.helper_capabilities_request()
        print("full capabilities string: ", string)
    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in helper_capabilities_request: ", msg)
    except PDError as msg:
        print("Error helper_capabilities_request:", msg)
    return


def do_lan_mac_address_tests(pd):
    try:
        print("Testing: command_lan_mac_address_read")
        mac, ipv = pd.command_lan_mac_address_read()
        print("command_lan_mac_address_read.IPV:", ipv)
        print("command_lan_mac_address_read.MAC:", mac)
    except PDCommandNotSupportedError as msg:
        print("Error command_lan_mac_address_read: ", msg)
    return


def do_power_save_time_tests(pd):
    try:
        print("Testing: command_power_save_mode_read")
        value = pd.command_power_save_mode_read()
        print("command_power_save_mode_read.value:", value)

        print("Testing: command_power_save_mode_write")
        value = pd.command_power_save_mode_write(value)
        print("command_power_save_mode_write.status:", value)

        print("Testing: command_auto_power_save_time_read")
        value = pd.command_auto_power_save_time_read()
        print("command_auto_power_save_time_read.value:", value)

        print("Testing: command_auto_power_save_time_write")
        value = 5
        value = pd.command_auto_power_save_time_write(value)
        print("command_auto_power_save_time_write:", value)

        print("Testing: command_auto_standby_time_read")
        value = pd.command_auto_standby_time_read()
        print("command_auto_standby_time_read.value:", value)

        value = 5
        print("Testing: command_auto_standby_time_write")
        value = pd.command_auto_standby_time_write(value)
        print("command_auto_standby_time_write.status:", value)
    except PDCommandNotSupportedError as msg:
        print("Error power_save command: ", msg)
    return


def do_main_other_tests(pd):
    try:
        print("Testing: command_security_enable_read")
        value = pd.command_security_enable_read()
        print("command_security_enable_read value:", value)
    except PDCommandNotSupportedError as msg:
        print("Error:", msg)

    print("Testing: command_security_lock_control")
    status, mode = pd.command_security_lock_control(0, "0000")
    print("command_security_lock_control status:", status)
    print("command_security_lock_control mode:", mode)

    print("Testing: helper_send_ir_remote_control_codes")
    pd.helper_send_ir_remote_control_codes(['menu', '+', '+'])

    try:
        print("Testing: helper_date_and_time_write")
        value = pd.helper_date_and_time_write(datetime.datetime.now(), True)
        print("helper_date_and_time_write status:", value.status,
              "year:", value.year,
              "month:", value.month,
              "day:", value.day,
              "weekday:", value.weekday,
              "hour:", value.hour,
              "minute:", value.minute,
              "daylight_savings:", value.daylight_savings)

        print("Testing: helper_date_and_time_read")
        value, daylight_savings = pd.helper_date_and_time_read()
        print("helper_date_and_time_read.datetime:", str(value), "daylight_savings:", daylight_savings)

    except PDCommandNotSupportedError as msg:
        print("Error date time: ", msg)

    print("Testing: command_save_current_settings")
    pd.command_save_current_settings()
    return


def do_schedule_tests(pd):
    try:
        for x in range(0, 31):
            print("Testing: command_schedule_read #", x)
            value = pd.command_schedule_read(x)
            print("command_schedule_read program_no:", value.program_no,
                  "turn_on:", value.turn_on_hour,
                  ":", value.turn_on_minute,
                  "turn_off:", value.turn_off_hour,
                  ":", value.turn_off_minute,
                  "timer_input:", value.timer_input,
                  "week_setting:", value.week_setting,
                  "option:", value.option,
                  "picture_mode:", value.picture_mode,
                  "extension_1:", value.extension_1,
                  "extension_2:", value.extension_2,
                  "extension_3:", value.extension_3,
                  "extension_4:", value.extension_4,
                  "extension_5:", value.extension_5,
                  "extension_6:", value.extension_6,
                  "extension_7:", value.extension_7)

            print("Testing: command_schedule_write")
            value = pd.command_schedule_write(x, value)
            print("command_schedule_write program_no:", value.program_no,
                  "status:", value.status,
                  "turn_on:", value.turn_on_hour,
                  ":", value.turn_on_minute,
                  "turn_off:", value.turn_off_hour,
                  ":", value.turn_off_minute,
                  "timer_input:", value.timer_input,
                  "week_setting:", value.week_setting,
                  "option:", value.option,
                  "picture_mode:", value.picture_mode,
                  "extension_1:", value.extension_1,
                  "extension_2:", value.extension_2,
                  "extension_3:", value.extension_3,
                  "extension_4:", value.extension_4,
                  "extension_5:", value.extension_5,
                  "extension_6:", value.extension_6,
                  "extension_7:", value.extension_7)
    except PDError as msg:
        print("Error do_schedule_tests: ", msg)
    return


def do_proof_of_play_tests(pd):
    try:
        print("Testing: command_set_proof_of_play_operation_mode")
        value = pd.command_set_proof_of_play_operation_mode(1)
        print("command_set_proof_of_play_operation_mode: ", value)

        print("Testing: command_get_proof_of_play_status")
        value = pd.command_get_proof_of_play_status()
        print("command_get_proof_of_play_status error_status:", value.error_status,
              "total_number:", value.total_number,
              "maximum_number:", value.maximum_number,
              "current_status:", value.current_status)
        total_number = value.total_number

        print("Testing: command_get_proof_of_play_current")
        value = pd.command_get_proof_of_play_current()
        print("command_get_proof_of_play_current status=", value.status,
              "log_number:", value.log_number,
              "input:", value.input,
              "signal_h_resolution:", value.signal_h_resolution,
              "signal_v_resolution:", value.signal_v_resolution,
              "audio_input:", value.audio_input,
              "audio_input_status:", value.audio_input_status,
              "picture_status:", value.picture_status,
              "audio_status:", value.audio_status,
              "year", value.year,
              "month:", value.month,
              "day:", value.day,
              "hour:", value.hour,
              "minute:", value.minute,
              "second:", value.second,
              "reserved_1:", value.reserved_1,
              "reserved_2:", value.reserved_2,
              "reserved_3:", value.reserved_3)

        print("Testing: helper_get_proof_of_play_current")
        value = pd.helper_get_proof_of_play_current()
        print("helper_get_proof_of_play_current status=", value.status, "log_number:", value.log_number,
              "input:", value.input,
              "signal_h_resolution:", value.signal_h_resolution,
              "signal_v_resolution:", value.signal_v_resolution,
              "audio_input:", value.audio_input,
              "audio_input_status:", value.audio_input_status,
              "picture_status:", value.picture_status,
              "audio_status:", value.audio_status,
              "datetime:", str(value.date_time),
              "reserved_1:", value.reserved_1,
              "reserved_2:", value.reserved_2,
              "reserved_3:", value.reserved_3)

        print("Testing: command_get_proof_of_play_number_to_number")
        for x in range(1, total_number + 1):
            value = pd.command_get_proof_of_play_number_to_number(x, x)
            print("command_get_proof_of_play_number_to_number status=", value.status,
                  "log_number:", value.log_number,
                  "input:", value.input,
                  "signal_h_resolution:", value.signal_h_resolution,
                  "signal_v_resolution:", value.signal_v_resolution,
                  "audio_input:", value.audio_input,
                  "audio_input_status:", value.audio_input_status,
                  "picture_status:", value.picture_status,
                  "audio_status:", value.audio_status,
                  "year", value.year,
                  "month:", value.month,
                  "day:", value.day,
                  "hour:", value.hour,
                  "minute:", value.minute,
                  "second:", value.second,
                  "reserved_1:", value.reserved_1,
                  "reserved_2:", value.reserved_2,
                  "reserved_3:", value.reserved_3)

        print("Testing: helper_get_proof_of_play_number")
        for x in range(1, total_number + 1):
            value = pd.helper_get_proof_of_play_number(x)
            print("helper_get_proof_of_play_number status=", value.status,
                  "log_number:", value.log_number,
                  "input:", value.input,
                  "signal_h_resolution:", value.signal_h_resolution,
                  "signal_v_resolution:", value.signal_v_resolution,
                  "audio_input:", value.audio_input,
                  "audio_input_status:", value.audio_input_status,
                  "picture_status:", value.picture_status,
                  "audio_status:", value.audio_status,
                  "datetime:", str(value.date_time),
                  "reserved_1:", value.reserved_1,
                  "reserved_2:", value.reserved_2,
                  "reserved_3:", value.reserved_3)

    except PDCommandNotSupportedError as msg:
        print("Error proof_of_play: ", msg)

    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in proof_of_play: ", msg)
    return


def do_pbp_pip_tests(pd):
    try:

        profile_number = 2
        new_profile = PDPIPPBPProfileTuple(profile_number=profile_number,
                                           pip_pbp_mode=2,
                                           picture1_input=0x1,
                                           picture2_input=0x88,
                                           picture3_input=0,
                                           picture4_input=0,
                                           picture1_size=80,
                                           picture2_size=80,
                                           picture3_size=0,
                                           picture4_size=0,
                                           picture1_aspect=1,
                                           picture2_aspect=1,
                                           picture3_aspect=0,
                                           picture4_aspect=0,
                                           picture1_h_position=0,
                                           picture2_h_position=0,
                                           picture3_h_position=0,
                                           picture4_h_position=0,
                                           picture1_v_position=0,
                                           picture2_v_position=0,
                                           picture3_v_position=0,
                                           picture4_v_position=0,
                                           reserved_11=0,
                                           reserved_12=0,
                                           reserved_13=0,
                                           reserved_14=0,
                                           reserved_15=0,
                                           reserved_16=0,
                                           reserved_17=0,
                                           reserved_18=0,
                                           reserved_19=0,
                                           reserved_20=0,
                                           reserved_21=0,
                                           reserved_22=0)

        print("Testing: command_pbp_pip_profile_contents_write")
        value = pd.command_pbp_pip_profile_contents_write(new_profile)
        print("command_pbp_pip_profile_contents_write:", value)

        print("Testing: command_pbp_pip_profile_contents_read")
        value = pd.command_pbp_pip_profile_contents_read(profile_number)
        print("command_pbp_pip_profile_contents_read:", value)
        print("command_pbp_pip_profile_contents_read profile_number=", value.profile_number,
              "pip_pbp_mode:", value.pip_pbp_mode,
              "picture1_input:", value.picture1_input,
              "picture2_input:", value.picture2_input,
              "picture3_input:", value.picture3_input,
              "picture4_input:", value.picture4_input,
              "picture1_size:", value.picture1_size,
              "picture2_size:", value.picture2_size,
              "picture3_size:", value.picture3_size,
              "picture4_size:", value.picture4_size,
              "picture1_aspect:", value.picture1_aspect,
              "picture2_aspect:", value.picture2_aspect,
              "picture3_aspect:", value.picture3_aspect,
              "picture4_aspect:", value.picture4_aspect,
              "picture1_h_position:", value.picture1_h_position,
              "picture2_h_position:", value.picture2_h_position,
              "picture3_h_position:", value.picture3_h_position,
              "picture4_h_position:", value.picture4_h_position,
              "picture1_v_position:", value.picture1_v_position,
              "picture2_v_position:", value.picture2_v_position,
              "picture3_v_position:", value.picture3_v_position,
              "picture4_v_position:", value.picture4_v_position,
              "reserved_11:", value.reserved_11,
              "reserved_12:", value.reserved_12,
              "reserved_13:", value.reserved_13,
              "reserved_14:", value.reserved_14,
              "reserved_15:", value.reserved_15,
              "reserved_16:", value.reserved_16,
              "reserved_17:", value.reserved_17,
              "reserved_18:", value.reserved_18,
              "reserved_19:", value.reserved_19,
              "reserved_20:", value.reserved_20,
              "reserved_21:", value.reserved_21,
              "reserved_22:", value.reserved_22)

    except PDCommandNotSupportedError as msg:
        print("Error pbp_pip_profile: ", msg)

    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in pbp_pip_profile: ", msg)
    return


def do_tile_matrix_profile_tests(pd):
    try:
        profile = 1

        new_profile = PDTileMatrixProfileTuple(profile_number=profile,
                                             h_monitors=2,
                                             v_monitors=2,
                                             position=2,
                                             tile_comp=1)
        print("Testing: command_tile_matrix_profile_contents_write")
        value = pd.command_tile_matrix_profile_contents_write(new_profile)
        print("command_tile_matrix_profile_contents_write:", value)

        print("Testing: command_tile_matrix_profile_write")
        value = pd.command_tile_matrix_profile_write(profile)
        print("command_tile_matrix_profile_write:", value)

        for x in range(1, 5):
            try:
                print("Testing: command_tile_matrix_profile_contents_read")
                value = pd.command_tile_matrix_profile_contents_read(x)
                print("command_tile_matrix_profile_contents_read profile #", x, ":", value)
            except PDCommandNotSupportedError as msg:
                print("Error command_tile_matrix_profile_contents_read: ", msg)
                continue
        return

    except PDCommandNotSupportedError as msg:
        print("Error tile_matrix_profile: ", msg)

    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in tile_matrix_profile: ", msg)
    return


def do_input_name_of_designated_terminal_tests(pd):
    try:

        for video_input in get_opcode_value_list(OPCODE_INPUT):
            try:
                print("Testing: command_input_name_of_designated_terminal_read input=", hex(video_input), "(",
                      opcode_value_to_nice_value_name(OPCODE_INPUT, video_input), ")")
                value = pd.command_input_name_of_designated_terminal_read(video_input)
                print("command_input_name_of_designated_terminal_read:", value)
            except PDCommandStatusReturnedError as msg:
                print ("input not supported: ", msg)

        video_input = 0x11
        print("Testing: command_input_name_of_designated_terminal_write")
        value = pd.command_input_name_of_designated_terminal_write(video_input, "test987")
        print("command_input_name_of_designated_terminal_write:", value)

        print("Testing: command_input_name_of_designated_terminal_read")
        value = pd.command_input_name_of_designated_terminal_read(video_input)
        print("command_input_name_of_designated_terminal_read:", value)

        print("Testing: command_input_name_of_designated_terminal_reset")
        value = pd.command_input_name_of_designated_terminal_reset(video_input)
        print("command_input_name_of_designated_terminal_reset:", value)
        return
    except PDCommandNotSupportedError as msg:
        print("Error input_name_of_designated_terminal: ", msg)

    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in input_name_of_designated_terminal: ", msg)
    return


def do_athlon5_tests(pd):
    try:
        print("Testing: command_firmware_revision_read")
        value = pd.command_firmware_revision_read()
        print("command_firmware_revision_read:", value)

    except PDCommandNotSupportedError as msg:
        print("Error command_firmware_revision_read: ", msg)

    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in command_firmware_revision_read: ", msg)

    try:
        print("Testing: helper_get_long_power_on_hours")
        value = pd.helper_get_long_power_on_hours()
        print("helper_get_long_power_on_hours:", value)

        print("Testing: helper_get_long_total_operating_hours")
        value = pd.helper_get_long_total_operating_hours()
        print("helper_get_long_total_operating_hours:", value)
    except PDCommandNotSupportedError as msg:
        print("Error helper_get_long_power_on_hours: ", msg)

    except PDUnexpectedReplyError as msg:
        print("Error unexpected reply in helper_get_long_total_operating_hours: ", msg)
    return


def do_other_tests(pd):
    try:
        # test main functions that are covered by "helper_xxx" functions
        print("Testing: command_date_and_time_read")
        value = pd.command_date_and_time_read()
        print("command_date_and_time_read year:", value.year,
              "month:", value.month,
              "day:", value.day,
              "weekday:", value.weekday,
              "hour:", value.hour,
              "minute:", value.minute,
              "daylight_savings:", value.daylight_savings)

        print("Testing: command_date_and_time_write")
        value = pd.command_date_and_time_write(value)
        print("command_date_and_time_read status:", value.status,
              "year:", value.year,
              "month:", value.month,
              "day:", value.day,
              "weekday:", value.weekday,
              "hour:", value.hour,
              "minute:", value.minute,
              "daylight_savings:", value.daylight_savings)

        pd.command_send_ir_remote_control_code(PD_IR_COMMAND_CODES['display'])

        value = pd.command_asset_data_read(0)
        print("command_asset_data_read.value:", value)

        value = pd.command_asset_data_read(32)
        print("command_asset_data_read.value:", value)

        value = pd.command_asset_data_write(0, "1234567890!@#$%^&*()123456789012")
        print("command_asset_data_write.value:", value)

        value = pd.command_asset_data_write(32, "98765432109876543210987654321021")
        print("command_asset_data_write.value:", value)

        try:
            for val in range(0,4):
                value = pd.command_firmware_version_read(val)
                print("command_firmware_version_read #", val, "value:", value)
        except PDCommandNotSupportedError as msg:
            print("Error command_firmware_version_read ", msg)
        except PDUnexpectedReplyError as msg:
            print("PDUnexpectedReplyError:", msg)
        except PDCommandStatusReturnedError as msg:
            print("firmware not supported: ", msg)

    except PDError as msg:
        print("PDError:", msg)
    return


def do_hack_lock_code(pd):
    try:
        # hack the lock code
        for val in range(0, 10000):
            code = str(val).zfill(4)
            # print("code:", code)
            try:
                value = pd.command_security_enable_write(0, code)
                print("correct code is:", code)
                break
            except PDCommandStatusReturnedError:
                # print("msg:", msg)
                print("incorrect code: ", code)
            except PDCommandNotSupportedError as msg:
                print(msg)
                break

    except PDError as msg:
        print("PDError:", msg)
    return


def do_opcode_dict_tests():
    # tests for the opcode dictionary from file
    print("opcode_values_to_name_dict keys:", opcode_values_to_name_dict.keys())
    print("opcode_values_to_name_dict values:", opcode_values_to_name_dict.values())

    print("input = ", opcode_to_nice_name(0x60))
    print("input = ", hex(nice_name_to_opcode("Input")))
    print("input val 1 = ", opcode_value_to_nice_value_name(0x60, 1))
    print("input val 1 = ", opcode_nice_value_name_to_value(0x60, "VGA"))
    print("get_opcode_list=", get_opcode_list())
    print("get_opcode_nice_value_name_list=", get_opcode_nice_value_name_list(0x60))
    print("get_opcode_value_list=", get_opcode_value_list(0x60))
    print("get_opcode_value_dict=", get_opcode_value_dict(0x60))

    for opcode in get_opcode_list():
        print("Opcode", hex(opcode), "is called", opcode_to_nice_name(opcode))
        values = get_opcode_nice_value_name_list(opcode)
        if values is not None:
            print("and supports values:", values)

    '''
    for opcode in get_opcode_list():
        name = string.upper(opcode_to_nice_name(opcode))
        name = string.replace(name, " ", "_")
        name = string.replace(name, "|", "_")
        name = string.replace(name, "(", "_")
        name = string.replace(name, ")", "_")
        print("OPCODE_", name, " = ", hex(opcode), sep='')
    '''
    return


def main():
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    # load the opcode dictionary from file
    load_opcode_dict()

    print("Presets: ")
    print("'1' = COM1")
    print("'2' = COM2")
    print("'3' = COM3")
    print("'4' = COM4")
    print("'5' = /dev/ttyS0 (Raspberry Pi 3)")
    print("'6' = /dev/ttyAMA0 (Raspberry Pi 1&2)")
    print("'7' = 192.168.0.10 (Default IP)")
    port = raw_input("or Enter an IP address or COM port name: ")

    if len(port) == 0:
        port = '192.168.1.234'
    elif len(port) == 1:
        if port[0] == '1':
            port = "COM1"
        elif port[0] == '2':
            port = "COM2"
        elif port[0] == '3':
            port = "COM3"
        elif port[0] == '4':
            port = "COM4"
        elif port[0] == '5':
            port = "/dev/ttyS0"
        elif port[0] == '6':
            port = "/dev/ttyAMA0"
        elif port[0] == '7':
            port = "192.168.0.10"
        elif port[0] == '8':
            port = "192.168.1.25"
        elif port[0] == '9':
            port = "192.168.1.160"
        else:
            print("Unknown option.")
            return

    print("Using port:", port)

    try:
        # Notes: For Raspberry Pi:
        # Enable Serial using "sudo raspi-config" (Advanced options)
        # Edit "sudo nano /boot/cmdline.txt" and remove section "console=ttyAMA0,115200"
        # pd = NECPD.open('/dev/ttyS0')  # Raspberry Pi 3 (since /ttyAMA0 used for Bluetooth)
        # pd = NECPD.open('/dev/ttyAMA0')  # Raspberry Pi 1&2

        pd = NECPD.open(port)
        # pd = NECPD.open("COM3")
        # pd = NECPD.open('192.168.1.25')
        # pd = NECPD.open('192.168.1.26')
        # pd = NECPD.open('192.168.1.234')

        monitor_id = raw_input("Enter the Monitor ID (1-100, A-J or ALL (Enter for 1): ")
        if len(monitor_id) == 0:
            monitor_id = 1

        pd.helper_set_destination_monitor_id(monitor_id)
        # pd.helper_set_destination_monitor_id("All")
        # pd.helper_set_destination_monitor_id("A")

        loops = int(raw_input("Enter number of times to repeat tests: "))
        assert 1 <= loops <= 10000

        try:
            for x in range(0, loops):
                print("---------  Testing loop ", x+1, "---------")
                do_main_tests(pd)
                do_auto_tile_matrix_tests(pd)
                do_daylight_savings_tests(pd)
                do_auto_id_tests(pd)
                do_input_name_tests(pd)
                do_direct_tv_channel_tests(pd)
                do_capability_string_tests(pd)
                do_lan_mac_address_tests(pd)
                do_power_save_time_tests(pd)
                do_main_other_tests(pd)
                do_schedule_tests(pd)
                do_proof_of_play_tests(pd)
                do_pbp_pip_tests(pd)
                do_tile_matrix_profile_tests(pd)
                do_input_name_of_designated_terminal_tests(pd)
                do_athlon5_tests(pd)
                do_other_tests(pd)
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
