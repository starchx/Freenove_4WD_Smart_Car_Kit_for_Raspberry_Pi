import time
from Motor import *
import RPi.GPIO as GPIO
import logging
import datetime

logging.basicConfig(filename=f"/var/log/line-tracking-position-{datetime.datetime.today().strftime('%Y-%m-%d')}.log",
                    filemode='a',
                    format='%(asctime)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

class Line_Tracking_With_Log:
    def __init__(self):
        self.IR01 = 14
        self.IR02 = 15
        self.IR03 = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.IR01,GPIO.IN)
        GPIO.setup(self.IR02,GPIO.IN)
        GPIO.setup(self.IR03,GPIO.IN)
        self.log_time = int(time.time()) # only log to a file every 1s to reduce the size of the log
    def run(self):
        while True:
            self.LMR=0x00
            if GPIO.input(self.IR01)==True:
                self.LMR=(self.LMR | 4)
            if GPIO.input(self.IR02)==True:
                self.LMR=(self.LMR | 2)
            if GPIO.input(self.IR03)==True:
                self.LMR=(self.LMR | 1)
            if self.LMR==2:
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR==4:
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR==6:
                PWM.setMotorModel(-2000,-2000,4000,4000)
            elif self.LMR==1:
                PWM.setMotorModel(2500,2500,-1500,-1500)
            elif self.LMR==3:
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR==7:
                #pass
                PWM.setMotorModel(0,0,0,0)
            
            # write the position to a log file for cloudwatch agent to upload
            if GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)==True and GPIO.input(self.IR03)!=True:
                if int(time.time()) > self.log_time:
                    print ('Middle')
                    logging.info("Middle")
                    self.log_time = int(time.time())
            elif GPIO.input(self.IR01)!=True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)==True:
                if int(time.time()) > self.log_time:
                    print ('Right')
                    logging.info("Right")
                    self.log_time = int(time.time())
            elif GPIO.input(self.IR01)==True and GPIO.input(self.IR02)!=True and GPIO.input(self.IR03)!=True:
                if int(time.time()) > self.log_time:
                    print ('Left')
                    logging.info("Left")
                    self.log_time = int(time.time())
            else:
                if int(time.time()) - self.log_time > 3: # at least 3 seconds to consider it is really invalid
                    print ('Invalid')
                    logging.info("Invalid")
                    self.log_time = int(time.time())

infrared=Line_Tracking_With_Log()
# Main program logic follows:
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        infrared.run()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program  will be  executed.
        PWM.setMotorModel(0,0,0,0)
