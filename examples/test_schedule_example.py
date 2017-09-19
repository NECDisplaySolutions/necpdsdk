"""test_schedule_example.py - Test routines and sample code for communicating via LAN or RS232 with NEC large-screen displays
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
from builtins import input
import logging
import datetime
from nec_pd_sdk.nec_pd_sdk import NECPD
from nec_pd_sdk.protocol import PDError
from nec_pd_sdk.protocol import PDUnexpectedReplyError
from nec_pd_sdk.constants import *
from nec_pd_sdk.opcode_decoding import *
from nec_pd_sdk.nec_pd_sdk import PDAdvancedScheduleTuple
from nec_pd_sdk.nec_pd_sdk import PDScheduleTuple
from nec_pd_sdk.nec_pd_sdk import PDHolidayTuple
from nec_pd_sdk.nec_pd_sdk import PDWeekendTuple


def reverse_dict(d):
    return dict(list(zip(list(d.values()), list(d.keys()))))


def do_main_tests(pd, advanced):
    try:
        if advanced == 1:
            print("Testing: command_advanced_schedule_read")
            for x in range(1, 30):
                value = pd.command_advanced_schedule_read(x)
                if value.hour == 24 and value.minute == 60:
                    print("Schedule ", x, " Is empty")
                else:
                    print("command_advanced_schedule_read value: ", value) 
                # print off time
                if value.event == 2 and value.hour != 24 and value.minute != 60:
                    mytime=datetime.time(value.hour, value.minute);
                    print("Turn off time: ", mytime.isoformat())
                # print on time
                if value.event == 1 and value.hour != 24 and value.minute != 24:
                    mytime=datetime.time(value.hour, value.minute);
                    print("Turn on time: ", mytime.isoformat())
                # print schedule type
                enabled = 0;
                if value.type & 0x01:
                    print("Every Day");
                elif value.type & 0x02:
                    str = ""
                    if value.week & 0x01:
                        str += "Mon"
                    if value.week & 0x02:
                        if str != "":
                            str += ", Tues"
                        else:
                            str += "Tues"
                    if value.week & 0x04:
                        if str != "":
                            str += ", Wed"
                        else:
                            str += "Wed"
                    if value.week & 0x08:
                        if str != "":
                            str += ", Thurs"
                        else:
                            str += "Thurs"
                    if value.week & 0x10:
                        if str != "":
                            str += ", Fri"
                        else:
                            str += "Fri"
                    if value.week & 0x20:
                        if str != "":
                            str += ", Sat"
                        else:
                            str += "Sat"
                    if value.week & 0x40:
                        if str != "":
                            str += ", Sun"
                        else:
                            str += "Sun" 

                    if not str:
                        print("Specific Days")
                    else:
                        print("Every ", str)
                elif value.type & 0x08:
                    print("Weekdays")
                elif value.type & 0x10:
                    print("Weekends")
                elif value.type & 0x20:
                    print("Holidays")
                elif value.type & 0x40:
                    mydate = datetime.date(value.year, value.month, value.day);
                    print("One Day on ", mydate.isoformat())

                if value.type & 0x04:
                    enabled = 1;
                    print ("Schedule is enabled")
                else:
                    print ("Schedule is disabled")

            print("\n\n")
            print("Testing: command_advanced_schedule_write")
            schedule = PDAdvancedScheduleTuple(status=0,
                                               program_no = 7,
                                               event = 1,
                                               hour = 8,
                                               minute = 0,
                                               input = 0,
                                               week = 96,
                                               type = 0x06,
                                               picture_mode = 0,
                                               year = 0,
                                               month = 0,
                                               day = 0,
                                               order = 0,
                                               extension_1 = 0,
                                               extension_2 = 0,
                                               extension_3 = 0)
            create_schedule = pd.command_advanced_schedule_write(7, schedule)
            print("Sent Schedule: ", schedule)
            print("Created Schedule: ", schedule)
    
            print("\n\n")
            print("Testing: command_advanced_schedule_enable_disable")
            schedule = pd.command_advanced_schedule_enable_disable(7, 0)
            print("Disable Sched: ", schedule)

            print("\n\n")
            print("Testing: helper_read_advanced_schedules")
            schedules = pd.helper_read_advanced_schedules()
            print("Schedules: ", schedules)

            #print("Testing program number out of range")
            #value = pd.command_advanced_schedule_read(34)

            print("Testing command_holiday_read")
            for x in range(1, 50):
                holiday = pd.command_holiday_read(x)
                print("Read Holiday: ", holiday)

            print("\n\n")
            print("Testing command_holiday_write")
            holiday=PDHolidayTuple(status=0,
                                   id=30,
                                   type=2,
                                   year=18,
                                   month=12,
                                   day=25,
                                   week_of_month=0,
                                   day_of_week=0,
                                   end_month=0,
                                   end_day=0)
            create_holiday = pd.command_holiday_write(30, holiday)
            print("Sent Holiday: ", holiday)
            print("Created Holiday: ", create_holiday)

            print("\n\n")
            print("Testing helper_read_holidays")
            holidays = pd.helper_read_holidays()
            print("Holidays: ", holidays)

            print("\n\n")
            print("Testing command_weekend_read")
            weekend = pd.command_weekend_read()
            w = ''
            if weekend.weekend & 0x01:
                w += 'M '
            if weekend.weekend & 0x02:
                w += 'T '
            if weekend.weekend & 0x04:
                w += 'W '
            if weekend.weekend & 0x08:
                w += 'Th '
            if weekend.weekend & 0x10:
                w += 'F '
            if weekend.weekend & 0x20:
                w += 'S '
            if weekend.weekend & 0x40:
                w += 'Sn '
            print("Weekend: ", w)

            print("\n\n")
            print("Testing command_weekend_write")
            weekend = PDWeekendTuple(status=0,
                                     weekend = 0x70)
            create_weekend = pd.command_weekend_write(weekend)
            w = ''
            cw = ''
            if weekend.weekend & 0x01:
                w += 'M '
            if create_weekend.weekend & 0x01:
                cw += 'M '
            if weekend.weekend & 0x02:
                w += 'T '
            if create_weekend.weekend & 0x02:
                cw += 'T '
            if weekend.weekend & 0x04:
                w += 'W '
            if create_weekend.weekend & 0x04:
                cw += 'W '
            if weekend.weekend & 0x08:
                w += 'Th '
            if create_weekend.weekend & 0x08:
               cw += 'Th '
            if weekend.weekend & 0x10:
                w += 'F '
            if create_weekend.weekend & 0x10:
                cw += 'F '
            if weekend.weekend & 0x20:
                w += 'S '
            if create_weekend.weekend & 0x20:
                cw += 'S '
            if weekend.weekend & 0x40:
                w += 'Sn '
            if create_weekend.weekend & 0x40:
                cw += 'Sn '
            print("Sent Weekend: ", w)
            print("Created Weekend: ", cw) 


        else:
            print("Testing: command_schedule_read")
            for x in range(1, 7):
                value = pd.command_schedule_read(x)
                print("command_schedule_read value: ", value) 

            print("\n\n")
            print("Testing: command_schedule_write")
            schedule = PDScheduleTuple(status=0,
                                       program_no=2,
                                       turn_on_hour=8,
                                       turn_on_minute=0,
                                       turn_off_hour=20,
                                       turn_off_minute=30,
                                       timer_input=0,
                                       week_setting=96,
                                       option=4,
                                       picture_mode=0,
                                       extension_1=0,
                                       extension_2=0,
                                       extension_3=0,
                                       extension_4=0,
                                       extension_5=0,
                                       extension_6=0,
                                       extension_7=0)
            create_schedule = pd.command_schedule_write(2, schedule)
            print("Sent Schedule: ", schedule)
            print("Created Schedule: ", create_schedule)

            print("\n\n")
            print("Testing: command_advanced_schedule_enable_disable")
            schedule = pd.command_schedule_enable_disable(2, 0)
            print("Disable Sched: ", schedule)

            print("\n\n")
            print("Testing: helper_read_schedules")
            schedules = pd.helper_read_schedules()
            print("Schedules: ", schedules)

            #print("Testing program number out of range")
            #value = pd.command_schedule_read(9)

    except PDUnexpectedReplyError as msg:
        print("PDUnexpetedReplyError: ", msg)
    except PDError as msg:
        print("PDError: ", msg)
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
    port = input("or Enter an IP address or COM port name: ")

    if len(port) == 0:
        port = '192.168.1.140'
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
        else:
            print("Unknown option.")
            return

    print("Using port:", port)

    try:
        pd = NECPD.open(port)

        monitor_id = input("Enter the Monitor ID (1-100, A-J or ALL (Enter for 1): ")
        if len(monitor_id) == 0:
            monitor_id = 1

        pd.helper_set_destination_monitor_id(monitor_id)

        advanced = input("Test Advanced? (N=No, Enter for YES): ")
        if len(advanced) == 0:
          advanced = 1;

        try:
            do_main_tests(pd, advanced)
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
