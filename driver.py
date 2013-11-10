#!/usr/bin/env 
import RPi.GPIO as GPIO
import socket

class Visual:
    
    bassLED1 = 8 # bass
    bassLED2 = 10
    midLED1  = 16 # alto, tenor
    midLED2  = 18
    trebLED1 = 22 # seprano
    trebLED2 = 24
    frequency = 120

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)
        
        GPIO.setup(self.bassLED1, GPIO.OUT)
        GPIO.setup(self.bassLED2, GPIO.OUT)
        GPIO.setup(self.trebLED1, GPIO.OUT)
        GPIO.setup(self.trebLED2, GPIO.OUT)
        GPIO.setup(self.midLED1, GPIO.OUT)
        GPIO.setup(self.midLED2, GPIO.OUT)

        self.bassDriver1 = GPIO.PWM(self.bassLED1, self.frequency)
        self.bassDriver2 = GPIO.PWM(self.bassLED2, self.frequency)
        self.midDriver1 = GPIO.PWM(self.midLED1, self.frequency)
        self.midDriver2 = GPIO.PWM(self.midLED2, self.frequency)
        self.trebDriver1 = GPIO.PWM(self.trebLED1, self.frequency)
        self.trebDriver2 = GPIO.PWM(self.trebLED2, self.frequency)

        self.bassDriver1.start(0)
        self.bassDriver2.start(0)
        self.midDriver1.start(0)
        self.midDriver2.start(0)
        self.trebDriver1.start(0)
        self.trebDriver2.start(0)

        self.bassVal = 0
        self.midVal  = 0
        self.trebVal = 0

    def setBMT(self, bass, mid, treb):
        if bass < 90:
            if self.bassVal > .5:
                self.bassVal -= 0.5
        else:
            self.bassVal = bass/(bass+15)*100.0
        if mid < 88:
            if self.midVal > .5:
                self.midVal -= 0.5
        else:
            self.midVal = mid/(mid+15)*100.0
        if treb < 88:
            if self.trebVal > .5:
                self.trebVal -= 0.5
        else:
            self.trebVal = treb/(treb+15)*100.0
        self.bassDriver1.ChangeDutyCycle(self.bassVal)
        self.bassDriver2.ChangeDutyCycle(self.bassVal)
        self.midDriver1.ChangeDutyCycle(self.midVal)
        self.midDriver2.ChangeDutyCycle(self.midVal)
        self.trebDriver1.ChangeDutyCycle(self.trebVal)
        self.trebDriver2.ChangeDutyCycle(self.trebVal)
    
def start():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 2345))
    sock.listen(2)

    client, addr = sock.accept()
    
    visuals = Visual()

    def recv():
        ch = client.recv(2)
        n = ord(ch[0]) << 8
        n |= ord(ch[1])
        return n

    while True:
        intensities = (recv(), recv(), recv())

        bmt = (sum(intensities[:2])/1310.0, sum(intensities[1:])/1310.0, sum(intensities)/1966.0)
        #print bmt
        visuals.setBMT(bmt[0], bmt[1], bmt[2])
    
    GPIO.cleanup()
    client.close()

if __name__ == "__main__":
    start()
