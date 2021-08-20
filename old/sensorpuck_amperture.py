# Code based on the implementation from http://amperture.com/?p=23
# With additions by Andreas Tobola, October 2015, http://tnotes.de/SensorPuck

import subprocess
import os

proc = subprocess.Popen(['hcidump --raw'], stdout=subprocess.PIPE, shell=True)

hrmStateStr = ['Idle', 'No Signal', 'Acquiring', 'Active', 'Invalid', 'Error']

while True:
    line = proc.stdout.readline()    
    if ">" not in line:        
        hexarray = line.split()
        N = len(hexarray)
       
        os.system('clear')
       
        if N==14:            
            print "== Enviromental Mode ==\n"
           
            # Humidity uint16 deciprecent
            humidity = (int(hexarray[6], 16) << 8) + int(hexarray[5], 16)
            humidity = float(humidity)/10
           
            # Temperature int16 decidegrees (can be negative -> twos complement)
            temp = (int(hexarray[8], 16) << 8) + int(hexarray[7], 16)
            temp = float(temp)/10

            # Ambient Light uint16 lux/2
            amblight = (int(hexarray[10], 16) << 8) + int(hexarray[9], 16)
            amblight = float(amblight)/2
           
            # UV Index uint8 index
            uvidx = int(hexarray[11], 16)
           
            # Battery Voltage uint8 decivolts
            vbat = int(hexarray[12], 16)
            vbat = float(vbat)/10
           
            print u"Humidity: %.1f " %humidity + '%'
            print u"Temperature: %.1f \xb0C" %temp
            print "Ambient light: %.1f Lux" %amblight
            print "UV index: %.1f" %uvidx
            print "Battery voltage: %.1f V" %vbat
        elif N==18:
            print "== Biometric Mode ==\n"      
           
            # HRM State uint8 none
            hrmState = int(hexarray[5], 16)
            print "HRM state: " + hrmStateStr[hrmState]
           
            # HRM Rate uint8 bpm
            pulseRate = int(hexarray[6], 16)
            print "Pulse rate: " + str(pulseRate) + " bpm"
           
            # HRM Sample Array uint16[5] none
            # ...
        print " "

