#!/bin/python
# -*- coding: utf-8 -*-
"""reset_display_wdt.py - Sample script to perform either or both the following operations:

1. Periodically reset the NEC large-screen display's WDT (watchdog timer) for the Raspberry Pi Compute Module.
This is done by sending a command to the display via the internal serial link.
Note: This feature requires at least display firmware R1.005 on the Vxx4 and Pxx4 models.

2. Automatically control the cooling fan in the NEC large-screen display based on the reported system temperature on the
Raspberry Pi Compute Module. This is done by sending a command to the display via the internal serial link.
Note: This feature requires at least display firmware R1.7 on the Vxx4 and Pxx4 models.

Note: This file name remains as "reset_display_wdt.py" for legacy purposes even though it can now perform two functions.


WDT FUNCTION
This feature is enabled by setting: use_reset_wdt = True
Note: This feature requires at least display firmware R1.005 on the Vxx4 and Pxx4 models.

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

There are two time periods that can be configured on the display for the Watchdog Timer:

 • Start Up Time – This sets the time delay for when the display should start receiving WDT reset commands, via the
 internal UART, after power is applied to the Compute Module. This timer’s value should be set high enough to include
 time for the operating system to fully load on the Compute Module, and for the periodic reset commands to begin
 sending to the display.

 • Period Time - This sets the maximum amount of time within which the display must receive WDT reset commands from
 the Compute Module, via the internal UART. If two consecutive reset commands are missed, the display will restart
 the Compute Module. This timer’s value should be set high enough to ensure that any software running on the
 Compute Module will be able to send the periodic reset command to the display, even under heavy load conditions.


FAN CONTROL FUNCTION
This feature is enabled by setting: use_fan_control = True
Note: This feature requires at least display firmware R1.7 on the Vxx4 and Pxx4 models. If the display firmware doesn't
support this feature then polling will be disabled.

This will poll the system temperature using the 'vcgencmd measure_temp' command. If the temperature exceeds the value
specified by 'high_temperature_limit' then the fan is turned on only if it is currently off.
If the temperature drops to the value specified by 'low_temperature_limit_on_to_off' or below, and the fan has been
on for longer than the time specified by 'fan_on_minimum_duration' and the fan is currently on, then the fan is turned
off. Commands to control the fan are only sent when it is necessary to change the fan state in order to reduce possible
conflicts with anything else communicating with the display at the same time.
The 'fan_on_minimum_duration' is used to prevent any annoying rapid cycling of the fan power.
The temperature polling interval (in seconds) is specified using 'temperature_polling_interval'


USAGE
1. Edit the configuration parameters below as needed.
2. Copy this file to a suitable location such as "/usr/share/NEC/".
3. Run this script each time the system starts.

For example it can be added to the "/etc/rc.local" file. Add the following line to the "/etc/rc.local"
file before the line with the text "exit 0":
sudo python /usr/share/NEC/reset_display_wdt.py &


Revision: 180224
"""


# Copyright (C) 2016-18 NEC Display Solutions, Ltd
# written by Will Hollingworth <whollingworth at necdisplay.com>
# See LICENSE.rst for details.

import time
import logging
import os
from nec_pd_sdk.nec_pd_sdk import NECPD
from nec_pd_sdk.protocol import PDError
from nec_pd_sdk.protocol import PDUnexpectedReplyError

# change the following to the UART / COM port / IP address of the display
port = '/dev/ttyS0'
# port = '192.168.1.178'
monitor_id = 1

# set to True to enable resetting of the WDT. Set to False to disable.
use_reset_wdt = True
# set the WDT interval in seconds here. It should be at least the "PERIOD TIME" configured in the display.
wdt_interval = 15

# set to True to enable controlling the cooling fan based on the temperature. Set to False to disable.
use_fan_control = True
# interval in seconds at which to poll the system's temperature sensor.
temperature_polling_interval = 5
# set the temperature in 'C at which the fan is turned on.
high_temperature_limit = 65
# set the temperature in 'C at which the fan is turned off. This is a kind of hysteresis.
low_temperature_limit_on_to_off = high_temperature_limit - 5
# set the minimum length of time in seconds that the fan will remain on (used to prevent rapid cycling)
fan_on_minimum_duration = 30

# set to True to output debug info to the log. Set to False to disable.
enable_debug_logging = False


# fan control modes: OFF=Fan always on. ON=Fan always on. AUTO=Fan turns on and off with CM power.
FAN_MODE_OFF = 0x0001
FAN_MODE_ON = 0x0002
FAN_MODE_AUTO = 0x0003


def get_cpu_temperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return float(res.replace("temp=", "").replace("'C\n", ""))


def reset_wdt(pd):
    try:
        logging.info("Resetting WDT")
        reply = pd.command_set_parameter(0x119e, 1)
        logging.info("command_set_parameter result: %s opcode: %s type: %s max_value: %s current_value: %s" %
                     (reply.result, hex(reply.opcode), reply.type, reply.max_value, reply.current_value))
        if reply.result != 0:
            logging.info("Error: WDT Reset command not supported or is disabled")
        else:
            logging.info("WDT Reset")
    except PDUnexpectedReplyError as msg:
        print("PDUnexpectedReplyError:", msg)
    except PDError as msg:
        print("PDError:", msg)
    return


def set_fan_power_mode(pd, mode):
    assert 0x0001 <= mode <= 0x0003
    try:
        logging.info("Setting fan power mode %s" % mode)
        reply = pd.command_set_parameter(0x11b5, mode)
        logging.info("command_set_parameter result: %s opcode: %s type: %s max_value: %s current_value: %s" %
                     (reply.result, hex(reply.opcode), reply.type, reply.max_value, reply.current_value))
        if reply.result != 0:
            logging.info("Error: Fan power mode opcode not supported (check firmware version)")
            return -1
        else:
            logging.info("Set fan power mode %s" % mode)
            return 0
    except PDUnexpectedReplyError as msg:
        print("PDUnexpectedReplyError:", msg)
    except PDError as msg:
        print("PDError:", msg)
    return -2


def main():
    if enable_debug_logging:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    global use_fan_control
    assert high_temperature_limit > low_temperature_limit_on_to_off
    assert fan_on_minimum_duration > 0
    assert wdt_interval > 0
    assert temperature_polling_interval > 0
    assert use_reset_wdt | use_fan_control
    current_fan_state = FAN_MODE_OFF
    polling_interval = min(temperature_polling_interval, wdt_interval)
    if not use_fan_control:
        polling_interval = wdt_interval
    logging.info("use_reset_wdt %s" % use_reset_wdt)
    logging.info("use_fan_control %s" % use_fan_control)
    logging.info("high_temperature_limit %s" % high_temperature_limit)
    logging.info("low_temperature_limit_on_to_off %s" % low_temperature_limit_on_to_off)
    logging.info("polling_interval %s" % polling_interval)
    time_since_wdt_reset = 0
    time_since_fan_on = 0

    try:
        # first try and open communications. Any errors here should be reported and terminate.
        pd = NECPD.open(port)
        try:
            pd.helper_set_destination_monitor_id(monitor_id)
            if use_reset_wdt:
                # reset the WDT first thing
                reset_wdt(pd)
            if use_fan_control:
                # turn the fan on first thing
                error = set_fan_power_mode(pd, FAN_MODE_AUTO)
                if error == -1:
                    # the display's firmware doesn't support this command so disable trying again
                    logging.info("fan control not supported by the display so disabling")
                    use_fan_control = False
                    polling_interval = wdt_interval
                else:
                    current_fan_state = FAN_MODE_AUTO
            pd.close()

            # next do an infinite loop of resetting the WDT and/or fan control.
            while True:
                try:
                    logging.info("Waiting for %s seconds" % polling_interval)
                    time.sleep(polling_interval)

                    if use_reset_wdt:
                        if polling_interval == wdt_interval:
                            pd = NECPD.open(port)
                            reset_wdt(pd)
                            pd.close()
                        else:
                            time_since_wdt_reset += polling_interval
                            # if polling rapidly (because 'use_fan_control') then only send the WDT reset when
                            # wdt_interval is exceeded
                            if time_since_wdt_reset >= wdt_interval:
                                pd = NECPD.open(port)
                                reset_wdt(pd)
                                pd.close()
                                time_since_wdt_reset = 0
                    if use_fan_control:
                        try:
                            temperature = get_cpu_temperature()
                            logging.info("Current temperature is %s and fan state is %s" % (temperature,
                                                                                            current_fan_state))
                            if current_fan_state == FAN_MODE_AUTO:
                                time_since_fan_on += polling_interval
                            if temperature >= high_temperature_limit:
                                if current_fan_state != FAN_MODE_AUTO:
                                    logging.info("Turning fan on")
                                    pd = NECPD.open(port)
                                    set_fan_power_mode(pd, FAN_MODE_AUTO)
                                    pd.close()
                                    current_fan_state = FAN_MODE_AUTO
                                    time_since_fan_on = 0
                            if temperature <= low_temperature_limit_on_to_off:
                                if current_fan_state != FAN_MODE_OFF:
                                    logging.info("time since turned on = %s" % time_since_fan_on)
                                    if time_since_fan_on >= fan_on_minimum_duration:
                                        logging.info("Turning fan off")
                                        pd = NECPD.open(port)
                                        set_fan_power_mode(pd, FAN_MODE_OFF)
                                        pd.close()
                                        current_fan_state = FAN_MODE_OFF
                                    else:
                                        logging.info("Fan not turned off because fan on for %s and minimum time is %s"
                                                     % (time_since_fan_on,fan_on_minimum_duration))
                            else:
                                logging.info("temperature > low_temperature_limit_on_to_off (%s)"
                                             % low_temperature_limit_on_to_off)
                        except ValueError:
                            print("Unable to read cpu temperature")
                            logging.error('Unable to read cpu temperature')
                except PDError as msg:
                    # catch any connection errors here so it continues regardless.
                    print("PDError:", msg)
                    logging.error('main loop PDError %s ', msg)
                    pd.close()
                except KeyboardInterrupt:
                    logging.info("KeyboardInterrupt")
                    return

        except PDError as msg:
            logging.error('initial check PDError %s ', msg)

        finally:
            # make sure to always close.
            logging.warning('closing port because error during initial check')
            pd.close()
    except PDError as msg:
        print("Connection error PDError:", msg)

    return


if __name__ == '__main__':
    main()
exit()
