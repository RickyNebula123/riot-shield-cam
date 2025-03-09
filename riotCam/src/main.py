import audio
import camera
import helpers
import RPi.GPIO as GPIO

if __name__ == '__main__':
    # Constants
    REC_BUTTON: int = 23 # GPIO 23 will be record button
    
    # Setup RPi board
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(REC_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Create camera object, initialize sensor
    cam = camera.Camera()
    
    # Generate filename
    filename = helpers.generate_filename()
    
    # Wait for start signal
    input('Press enter to start recording >>')
    
    # Start recording
    cam.record(filename)
    mic.record_audio(filename)
    
    # Wait for stop signal
    input('Press enter to stop recording >>')
    
    # Stop recording, clean up
    cam.stop_recording()
    mic.stop_recording_audio()
    
    
    
    
    