import RPi.GPIO as GPIO
import time, socket

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

    def setBMT(self, bass, mid, treb):
        self.bassDriver1.ChangeDutyCycle(bass)
        self.bassDriver2.ChangeDutyCycle(bass)
        self.midDriver1.ChangeDutyCycle(mid)
        self.midDriver2.ChangeDutyCycle(mid)
        self.trebDriver1.ChangeDutyCycle(treb)
        self.trebDriver2.ChangeDutyCycle(treb)

def start():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    visuals = Visual()

    bmts = ((0,0,0),(100,100,100),(66,0,66),(30,30,30),(66,66,30),(30,30,30),(0,100,66))

    index = 0

    # bmt = bmts[0] # something that separates the treble, mid, and bass using fft

    while True:
        bmt = bmts[index]
        index = (index + 1) % len(bmts)
        visuals.setBMT(bmt[0], bmt[1], bmt[2])
        time.sleep(0.15)
        bmt = bmts[0]
        visuals.setBMT(bmt[0], bmt[1], bmt[2])
        #time.sleep(0.02)
    # some running code
    
    GPIO.cleanup()
    sock.close()

if __name__ == "__main__":
    start()
