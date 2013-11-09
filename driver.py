import RPi.GPIO as GPIO

TxPin = 8
RxPin = 10

class Visual:
    
    bassLED = 3 # bass
    midLED  = 5 # alto, tenor
    trebLED = 7 # seprano
    frequency = 120

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)
        
        GPIO.setup(bassLED, GPIO.OUT)
        GPIO.setup(trebleLED, GPIO.OUT)
        GPIO.setup(midLED, GPIO.OUT)

        self.bassDriver = GPIO.PWM(self.bassLED, self.frequency)
        self.midDriver = GPIO.PWM(self.midLED, self.frequency)
        self.trebDriver = GPIO.PWM(self.trebLED, self.frequency)

        self.bassDriver.start(0)
        self.midDriver.start(0)
        self.trebDriver.start(0)

    def setBMT(self, bass, mid, treb):
        self.bassDriver.ChangeDutyCycle(bass)
        self.midDriver.ChangeDutyCycle(mid)
        self.trebDriver.ChangeDutyCycle(treb)

def start():

    visuals = Visual()

    bmt = (0,0,0) # something that separates the treble, mid, and bass using fft

    visuals.setBMT(bmt[0], bmt[1], bmt[2])
    
    # some running code
    GPIO.cleanup()
