#! /bin/sh
#
### BEGIN INIT INFO
# Provides:		Radio
# Required-Start:	$all
# Required-Stop:
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Disciption:	Radio Service
# Description:		This service starts a Radio on the RPi
## END INIT INFO

HOME=/home/pi
USER=pi

sudo /usr/bin/python3 /home/pi/Desktop/Radio/radio.py

exit 0
