#!/bin/python
# -*- coding: utf-8 -*-
"""set_display_to_system_clock.py - Sample script to read the current date and time from the operating system and
 set the NEC large-screen display's internal RTC (real-time clock), via the internal serial link from the Raspberry
 Pi Compute Module.

 This could be used to rely on the Raspberry Pi to automatically read an Internet time server to keep the operating
 system's tme and date correct, and then use that to update the RTC in the host NEC large-screen display. Make sure that
 the correct time has been updated on the operating system before running this.

Revision: 170317
"""

# Copyright (C) 2016-17 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.

import datetime
from nec_pd_sdk.nec_pd_sdk import NECPD
from nec_pd_sdk.protocol import PDError


def main():
    try:
        # change the following to the UART / COM port / IP address of the display
        pd = NECPD.open('/dev/ttyS0')
        pd.helper_set_destination_monitor_id(1)
        try:
            value = pd.helper_date_and_time_write_keep_daylight_savings_setting(datetime.datetime.now())
            print("helper_date_and_time_write status:", value.status,
                  "year:", value.year,
                  "month:", value.month,
                  "day:", value.day,
                  "weekday:", value.weekday,
                  "hour:", value.hour,
                  "minute:", value.minute,
                  "daylight_savings:", value.daylight_savings)
        finally:
            # make sure to always close
            pd.close()

    except PDError as msg:
        print("PDError:", msg)
    return

if __name__ == '__main__':
    main()
exit()
