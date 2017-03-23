#!/bin/python
# -*- coding: utf-8 -*-
"""set_system_to_display_clock.py - Sample script to read the current date and time from the NEC large-screen display's
 internal RTC (real-time clock), via the internal serial link from the Raspberry Pi Compute Module, and set the
 operating system's date.

 This could be used for example in situations where the Raspberry Pi Compute Module doesn't have network connectivity,
 but still needs to have the correct date and time. In this case it relies on the RTC in the host display to be correct.

 Note that this runs the OS function "date" as sudo in order to set the date.

Revision: 170317
"""

# Copyright (C) 2016-17 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.


from nec_pd_sdk.nec_pd_sdk import NECPD
from nec_pd_sdk.protocol import PDError
import os


def main():
    try:
        # change the following to the UART / COM port / IP address of the display
        pd = NECPD.open('/dev/ttyS0')
        # pd = NECPD.open('192.168.1.140')
        pd.helper_set_destination_monitor_id(1)
        try:
            value, daylight_savings = pd.helper_date_and_time_read()
            date_str = '{}-{}-{} {}:{}'.format(value.year, value.month, value.day, value.hour, value.minute)
            print("date_str:", date_str)
            os.system('sudo date -s "%s"' % date_str)

        finally:
            # make sure to always close
            pd.close()

    except PDError as msg:
        print("PDError:", msg)
    return

if __name__ == '__main__':
    main()
exit()
