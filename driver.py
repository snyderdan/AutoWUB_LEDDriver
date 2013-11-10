import RPi.GPIO as GPIO
import time, socket

class Visual:

    BASS_THRESH = 65.0
    MID_THRESH  = 52.0
    TREB_THRESH = 65.0
    
    BASSLED1 = 8 # bass
    BASSLED2 = 10
    MIDLED1  = 16 # alto, tenor
    MIDLED2  = 18
    TREBLED1 = 22 # seprano
    TREBLED2 = 24
    FREQUENCY = 120

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)

        GPIO.setwarnings(False)
        
        GPIO.setup(self.BASSLED1, GPIO.OUT)
        GPIO.setup(self.BASSLED2, GPIO.OUT)
        GPIO.setup(self.TREBLED1, GPIO.OUT)
        GPIO.setup(self.TREBLED2, GPIO.OUT)
        GPIO.setup(self.MIDLED1, GPIO.OUT)
        GPIO.setup(self.MIDLED2, GPIO.OUT)

        self.bassDriver1 = GPIO.PWM(self.BASSLED1, self.FREQUENCY)
        self.bassDriver2 = GPIO.PWM(self.BASSLED2, self.FREQUENCY)
        self.midDriver1 = GPIO.PWM(self.MIDLED1, self.FREQUENCY)
        self.midDriver2 = GPIO.PWM(self.MIDLED2, self.FREQUENCY)
        self.trebDriver1 = GPIO.PWM(self.TREBLED1, self.FREQUENCY)
        self.trebDriver2 = GPIO.PWM(self.TREBLED2, self.FREQUENCY)

        self.bassValue = 2
        self.midValue  = 2
        self.trebValue = 2
        
        self.setBMT(0,0,0)

    def setBMT(self, bass, mid, treb):
        if bass < self.BASS_THRESH: #and self.bassValue >= 2:
            self.bassValue -= 0
        elif bass > self.BASS_THRESH:
            self.bassValue = bass
        if mid < self.MID_THRESH:# and self.midValue >= 2:
            self.midValue -= 0
        elif mid > self.MID_THRESH:
            self.midValue  = mid
        if treb < self.TREB_THRESH:# and self.trebValue >= 2:
            self.trebValue -= 0
        elif treb > self.TREB_THRESH:
            self.trebValue = treb
            
        self.bassDriver1.ChangeDutyCycle(self.bassValue)
        self.bassDriver2.ChangeDutyCycle(self.bassValue)
        self.midDriver1.ChangeDutyCycle(self.midValue)
        self.midDriver2.ChangeDutyCycle(self.midValue)
        self.trebDriver1.ChangeDutyCycle(self.trebValue)
        self.trebDriver2.ChangeDutyCycle(self.trebValue)

def getBMT(intensities):
##    mags   = [abs(i) for i in fft.rfft(intensities)]
##    bmtRaw = (math.log((sum(mags[1:3])/10485.76)**2.2+1)*10,
##              math.log((sum(mags[3:6])/10485.76)**2.2+1)*10,
##              math.log((sum(mags[6:9])/10485.76)**2.2+1)*10)
##    bmtRaw = (sum(mags[1:3])/10485.76,
##              sum(mags[3:6])/10485.76,
##              sum(mags[6:9])/10485.76)
    bmtRaw = (sum(intensities[0:16])/10000.0,
              sum(intensities)/20200.0,
              sum(intensities[16:32])/10000.0)
    return (bmtRaw[0], bmtRaw[1], bmtRaw[2])
    
def start():

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #client, addr = sock.accept()
    
    visuals = Visual()

    visuals.bassDriver1.ChangeDutyCycle(100)
    visuals.bassDriver2.ChangeDutyCycle(100)

    while True:
        pass

    def recv():
        ch = client.recv(2)
        n = ord(ch[0]) << 8
        n |= ord(ch[1])
        return n

    intensities = [recv() for i in range(32)]

    while True:
        
        intensities.append(recv())
        intensities.pop(0)
        #intensities = [54442 for i in range(8)]+[0 for i in range(8)]
        bmt = getBMT(intensities)
        print bmt
        visuals.setBMT(bmt[0],bmt[1],bmt[2])
    
    GPIO.cleanup()
    sock.close()

if __name__ == "__main__":
    start()
