import audio
import camera
import helpers

if __name__ == '__main__':
    # Create camera object
    cam = camera.Camera()
    
    # Create microphone object
    mic = audio.Microphone()
    
    # Generate filename
    filename = helpers.generate_filename()
    
    # Wait for start signal
    input('Press enter to start recording >>')
    
    # Start recording
    cam.cam.start(show_preview=True)
    cam.record(filename)
    mic.record_audio(filename)
    
    # Wait for stop signal
    input('Press enter to stop recording >>')
    
    # Stop recording, clean up
    cam.stop_recording()
    mic.stop_recording_audio()
    
    
    
    
    