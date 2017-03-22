#!/bin/python
# -*- coding: utf-8 -*-
"""reset_display_wdt.py - Sample script to periodically reset the NEC large-screen display's WDT (watchdog timer) via
the internal serial link from the Raspberry Pi Compute Module.

The WDT can be used to automatically restart the Compute Module if it stops responding; for example, if it hangs for
some reason.

To use this feature, this background application is configured to periodically send reset commands to the display.
The display will expect to receive these reset commands as an indication that the Compute Module is functioning
normally. If, for some reason, the reset commands aren’t received as expected the display will shut down and restart
the Compute Module.

Use of the Watchdog Timer is optional and requires configuring the Operating System to start the background
application at bootup. The Watchdog Timer is enabled and configured via the OSD or communications commands.
The background application must send the reset command at least as often as the Period Time configured via the OSD.
If two consecutive resets commands aren’t received, the display will restart the Compute Module.

There are two time periods that can be configured for the Watchdog Timer:

 • Start Up Time – This sets the time delay for when the display should start receiving WDT reset commands, via the
 internal UART, after power is applied to the Compute Module. This timer’s value should be set high enough to include
 time for the operating system to fully load on the Compute Module, and for the periodic reset commands to begin
 sending to the display.

 • Period Time - This sets the maximum amount of time within which the display must receive WDT reset commands from
 the Compute Module, via the internal UART. If two consecutive reset commands are missed, the display will restart
 the Compute Module. This timer’s value should be set high enough to ensure that any software running on the
 Compute Module will be able to send the periodic reset command to the display, even under heavy load conditions.

Copy this file to a suitable location such as "/usr/share/NEC/".
Run this script each time the system starts.

For example it can be added to the "/etc/rc.local" file. Add the following line to the "/etc/rc.local"
file before the line with the text "exit 0":
sudo python /usr/share/NEC/reset_display_wdt.py &

Note: This feature requires at least display firmware R1.005

Revision: 170322
"""


# Copyright (C) 2016-17 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.

import time
import logging
from nec_pd_sdk import NECPD
from protocol import PDError
from protocol import PDUnexpectedReplyError

# set the WDT interval in seconds here. It should be at least the "PERIOD TIME" configured in the display.
interval = 15
# change the following to the UART / COM port / IP address of the display
port = '/dev/ttyS0'
# port = '192.168.1.140'


def reset_wdt(pd):
    try:
        print("Resetting WDT")
        reply = pd.command_set_parameter(0x119e, 1)
        # print("command_set_parameter result:", reply.result, "opcode:", hex(reply.opcode), "type:", reply.type,
        #       "max_value:", reply.max_value, "current_value:", reply.current_value)
        if reply.result != 0:
            print("Error: WDT Reset command not supported or is disabled")
        else:
            print("WDT Reset")
    except PDUnexpectedReplyError as msg:
        print("PDUnexpectedReplyError:", msg)
    except PDError as msg:
        print("PDError:", msg)
    return


def main():
    # uncomment the following line to enable debug logging
    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    try:
        # first try and open and reset the WDT. Any errors here should be reported and terminate.
        pd = NECPD.open(port)
        try:
            pd.helper_set_destination_monitor_id(1)
            reset_wdt(pd)
            pd.close()

            # next do an infinite loop of resetting the WDT.
            while True:
                try:
                    print("Waiting for ", interval, "seconds")
                    time.sleep(interval)
                    pd = NECPD.open(port)
                    reset_wdt(pd)

                except PDError as msg:
                    # catch any connection errors here so it continues regardless.
                    print("PDError:", msg)
                    logging.error('main loop PDError %s ', msg)
                finally:
                    # make sure to always close.
                    # logging.warning('close in finally in main loop')
                    pd.close()

        except PDError as msg:
            logging.error('initial check PDError %s ', msg)

        finally:
            # make sure to always close.
            logging.warning('closing port because error during initial check')
            # print("closing port because error during initial check ")
            pd.close()
    except PDError as msg:
        print("Connection error PDError:", msg)

    return

if __name__ == '__main__':
    main()
exit()
