# /usr/bin/python3

import vlc
import requests
import RPi.GPIO as GPIO
import time

#Import LCD libraty
import I2C_LCD_driver

# shuting down Raspberry Pi import
from subprocess import call

#video stream from youtube
#import pafy
print ("Import done!")

class radio:
    
    @classmethod
    def init(cls):
        # define pinout
        cls.PIN_SHUTDOWN = 22
        cls.PIN_PREV     = 23
        cls.PIN_NEXT     = 24
                
        # set class variables
        cls.nos         = 0       # total number of stations
        cls.stationName = ""
        cls.stationMRL  = ""
        cls.stationNumberCurrent = 0
        cls.updated     = 0       # flag to notify the station change

        # define inputs and outputs
        GPIO.setmode(GPIO.BOARD)     #use BCM numbering
        GPIO.setup(cls.PIN_NEXT, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(cls.PIN_PREV, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # GPIO.setup(cls.PIN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
        
        
        #Init player
        cls.player = vlc.MediaPlayer()
        cls.player.audio_set_volume(70)
        
        #Set up station list file and current
        cls.stationList = "/home/pi/Desktop/Radio/URLs.txt"
        cls.stationListLast = "/home/pi/Desktop/Radio/LastStation.txt"
        
        #Get the number of stations in the station list
        cls.__station_NumberTotal()
        
        #Read the last station and set it up
        cls.__station_NumberCurrent()
        cls.__station_SetNew(cls.stationNumberCurrent)
        cls.setMRL(cls.stationMRL) 
        
        #Initialize the LCD and display the current station
        cls.lcd_init()
        cls.lcd_clear()
        cls.lcd_write_name()
        cls.lcd_write_station_number()
        cls.lcd_write_time()
        
        # define events on button press
        GPIO.add_event_detect(cls.PIN_PREV, GPIO.FALLING, callback=cls.__station_Prev, bouncetime=500)
        GPIO.add_event_detect(cls.PIN_NEXT, GPIO.FALLING, callback=cls.__station_Next, bouncetime=500)
        # GPIO.add_event_detect(cls.PIN_SHUTDOWN, GPIO.FALLING, callback=cls.__shutdown, bouncetime=500)
        
        
        #copy the GitHub URLs
        try:
            url_git = "https://raw.githubusercontent.com/hadato/Internet_Radio_v2/master/URL"
            r = requests.get(url_git, allow_redirects=True)
            with open("/home/pi/Desktop/Radio/Git_URLs.txt", 'bw') as f:
                f.write(r.content)
        except:
            print("Error getting the GitHub file")
           
    
    
    @classmethod
    def setMRL(cls, MRL):
        cls.player.set_mrl(MRL)
    
    @classmethod
    def play(cls):
        cls.player.play()
    
    @classmethod
    def stop(cls):
        cls.player.stop
        
    # Function to find the total number of station on the list
    @classmethod
    def __station_NumberTotal(cls):
        try:
            with open(cls.stationList, 'r') as f:
                for i,l in enumerate(f,1):
                    pass
                cls.nos = i
            return 0
        except:
            pritn("Problem reading the station file")
            return 1
        
    @classmethod
    def __station_NumberCurrent(cls):
        try:
            with open(cls.stationListLast, 'r') as f:                
                lines = f.readlines()
            cls.stationNumberCurrent = lines[2]
        except:
            cls.__station_new(1)
            print("Unable to read the last station, reset to 1")
        
    @classmethod
    def __station_NumberNew(cls, newStationNumber):
        with open(cls.stationListLast, 'w') as f:
            f.write("# This is the file to store the last station number" + '\n')
            f.write("Last station number:" + '\n')
            f.write(str(newStationNumber))
    
    @classmethod
    def __station_Read(cls, stationNumber):
        try:
            with open(cls.stationList, 'r') as f:
                lines = f.readlines()
                name, mrl = lines[int(stationNumber)].split(';')
                mrl = mrl.split('\n')
                mrl = mrl[0]
                cls.stationName = name
                cls.stationMRL  = mrl
                return 0
        except:
            print("Error while opening URLs.txt")
            return 1
                
    @classmethod
    def __station_SetNew(cls, newStationNumber):
        try:
            cls.__station_Read(newStationNumber)
            cls.__station_NumberNew(newStationNumber)
            print(cls.stationName)
            print(cls.stationMRL)
            return 0
        except:
            print("Error setting a new station")
            return 1
        
    @classmethod
    def __station_Next(cls, trash = 0):
        try:
            cls.updated = 1
            cls.stop()
            cls.__station_NumberCurrent()
            cls.__station_SetNew((int(cls.stationNumberCurrent) + 1) % cls.nos)
            cls.setMRL(cls.stationMRL)
            cls.play()
            return 0
        except:
            print("Error while setting next station")
            return 1

    @classmethod
    def __station_Prev(cls, trash = 0):
        try:
            cls.updated = 1
            cls.stop()
            cls.__station_NumberCurrent()
            cls.__station_SetNew((int(cls.stationNumberCurrent) - 1) % cls.nos)
            cls.setMRL(cls.stationMRL)
            cls.play()
            return 0
        except:
            print("Error while setting previous station")
            return 1

    @classmethod
    def __shutdown(cls, trash):
        cls.updated = 2
        time.sleep(0.1)
        if GPIO.input(cls.PIN_SHUTDOWN)==0:
            cls.lcd_clear()
            time.sleep(0.1)
            cls.lcd.lcd_display_string("Mej krasny den", 2, 0)
            time.sleep(0.2)
            call("sudo shutdown -h now", shell=True)
        return 0

    @classmethod
    def lcd_init(cls):
        try:
            cls.lcd = mylcd = I2C_LCD_driver.lcd()
            return 0
        except:
            print("Error while initializing LCD")
            return 1

    @classmethod
    def lcd_write_name(cls):
        try:
            cls.lcd.lcd_display_string(cls.stationName[0:19], 1, 0)
            cls.lcd.lcd_display_string(cls.stationName[20:39], 2, 0)
            return 0
        except:
            print("Error writing name")
            return 1

    @classmethod
    def lcd_write_time(cls):
        try:
            cls.lcd.lcd_display_string(time.strftime("%d.%m.%Y     %H:%M"), 4, 0)
            time.sleep(0.001)
            return 0
        except:
            print("Error writing time")
            return 1

    @classmethod
    def lcd_write_station_number(cls):
        try:
            cls.lcd.lcd_display_string("Cislo stanice: "+str(int(cls.stationNumberCurrent) + 1), 3, 0)
            return 0
        except:
            print("Error writing station number")
            return 1

    @classmethod
    def lcd_clear(cls):
        try:
           cls.lcd.lcd_clear()
           return 0
        except:
           print("Error cleaning diplay")
           return 1

    @classmethod
    def lcd_clear_time(cls):
        try:
            cls.lcd.lcd_display_string("                    ", 4, 0)
            return 0
        except:
            print("Error cleaning time line")
            return 1

    @classmethod
    def display_update(cls):
        try:
            if (cls.updated == 2):
                time.sleep(3)
            elif (radio.updated == 1):
                cls.update = 0
                cls.lcd_clear()
                cls.lcd_write_name()
                cls.lcd_write_station_number()
                cls.lcd_write_time()
            else:
                cls.lcd_write_time()
            return 0
        except:
            pritn("Error updating display")
            return 1


    @classmethod
    def __error(cls):
        pass

    @classmethod
    def __del__(cls):
        GPIO.cleanup()
        cls.player.stop()
        cls.player.release()
        print("Player cleaned")


# Main initialization
radio.init()
radio.play()

# Main loop
try:
    while True:
       if (radio.updated == 2):
           time.sleep(3)
       elif (radio.updated == 1):
           radio.updated = 0
           radio.lcd_clear()
           radio.lcd_write_name()
           radio.lcd_write_station_number()
           radio.lcd_write_time()
       else:
           radio.lcd_write_time()
       radio.display_update()
       time.sleep(0.2)

# End of the program
except KeyboardInterrupt:
    pass

