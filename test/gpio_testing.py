import time
import RPi.GPIO as GPIO

BUTTON = 5
RECORDING = GPIO.HIGH
NOT_RECORDING = GPIO.LOW
STATE = NOT_RECORDING

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, direction=GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('Starting button test')

while True:
    curr_state = GPIO.input(BUTTON)
    if curr_state == GPIO.LOW:
        print('[STATE CHANGE]')
        
        if STATE == NOT_RECORDING:
            STATE = RECORDING
            print('Recording in progress!')
        elif STATE == RECORDING:
            STATE = NOT_RECORDING
            print('Saving recording')
        
        # time.sleep(0.2)
        
        
        
    