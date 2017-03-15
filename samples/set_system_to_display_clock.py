from nec_pd_sdk import NECPD
from protocol import PDError
import os


def main():
    try:
		# change the following to the UART  / COM port / IP address of the display
        pd = NECPD.open('/dev/ttyS0')
        #pd = NECPD.open('192.168.1.140')
        pd.helper_set_destination_monitor_id(1)
        try:
            value, daylight_savings = pd.helper_date_and_time_read()
            #print("helper_date_and_time_read.datetime:", str(value), "daylight_savings:", daylight_savings)
            date_str = '{}-{}-{} {}:{}'.format(value.year, value.month, value.day, value.hour, value.minute)
            print("date_str:", date_str)
            #os.system("sudo timedatectl set-time '%s'" % date_str)
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
