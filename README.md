# Internet Radio v2
This is a second generation of a simple internet radio for a person who is not a big fan of the modern technology. This time the radio is build around a vintage casing.

![Radio 1](https://github.com/hadato/Internet_Radio_v2/blob/master/_DSC3178.JPG)

## Motivation
After a long search for an internet radio which would be suitable for a person who does not enjoy modern technology, the idea was very clear. I wanted to build a radio with just few buttons to control it (volume, next/previous station, ON/OFF), and a simple information display. Due to the fact that the person inclines to vintage design, I wanted to utilize an old radio and keep the look as close to the original as possible.

## Construction and Operation
The radio is based on Raspberry Pi Zero W which is the cheapest model of a small linux computer including Wi-Fi. The radio further utilises an external USB sound card to provide a reasonable sound quality. For sound amplification, a single integrated A-B class amplifier based on TDA7297 is used. The sound amplifier is fed from a 15V switching power source (not ideal) with additional filtering. For the Raspberry a second 5V source is used. 

The main casing comes from an old Tesla 411U (1952/53). All the internal parts were taken out and a new front speaker board and compartment ware created. The internal construction is made out of thick paper board in several layers stiffened by several ribs.  The closed speaker box of approximately 6 l is equipped with a single 3.5" speaker (Vifa TC9FD18-08) which provides a reasonable sound for such a simple design. In order to keep the vintage look, a thin fabric is placed over the front board. 

In the lower part of the radio, all electronic components except of the display are placed. The display is hidden behind the fabric on the right side of the speaker, but it is still perfectly readable. It communicates with the Raspberry through I2C. The front glass tuning panel was mounted directly to the casing with a light background to make the writing more visible. 

Original buttons are left on the right side of the radio. The front one is directly connected to the potentiometer and controls the volume. The back one operates as a lever and presses two toggle-buttons to change the station. The right side button was lost during the life of the radio and is replaced by the power switch.

 

## Software
The Raspberry Pi runs Raspbian with a SSH possibility. During the start-up, a simple service radio.py based on libVLC is started as a service.  The service then checks for the interrupts from the buttons and behave accordingly. In addition, station name, current station number and time are sent to the display through I2C. If the NEXT/PREVIOUS button is pressed, the service reads next/previous station from a station list saved in an external text file (the name and the station address are hardcoded). If the power switch is toggled to position OFF, the service send a command to turn the raspberry system off. After ca. 20 s, the power is switched off by switching off a relay (delay circuit). 

## To Be Done
So far the station name and the address are hardcoded in a file and no meta data are read from the internet stations itself. Hence, no more information is  available (song name, song duration, author, ...). The logical step is to implement the meta data read-out. Moreover, the file is included in the radio and can be just changed through I2C. The idea is to implement a function to read the station file from GitHub on a startup (started, but not yet finished). The last obvious update could be a more complicated sound box design to boost the lower frequencies. Even though the dimensions are "quite big", my favourite scaled Karlsonator design cannot fit in the box.  A well sounded alternative, which I want to try to implement, is dual chamber reflex (DCR).

## Conclusion
Giving this radio as a gift was a success, similarly to the previous version. Even though there is a of room for improvement, the radio as it is does the job and pleases the eye. 

## All Pictures
![Radio 2]( https://github.com/hadato/Internet_Radio_v2/blob/master/_DSC3178.JPG)
![Radio 3]( https://github.com/hadato/Internet_Radio_v2/blob/master/_DSC3179.JPG)
![Radio 4]( https://github.com/hadato/Internet_Radio_v2/blob/master/_DSC3183.JPG)

