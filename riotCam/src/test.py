import audio
import camera
import cv2
import helpers
import time

from picamera2 import MappedArray

color = (0, 255, 0)
origin = (0, 30)
font = cv2.FONT_HERSHEY_SIMPLEX
scale = 1
thickness = 2

audio_opts = ''

def apply_timestamp(request):
    timestamp = time.strftime('%Y-%m-%d %X')
    with MappedArray(request, 'main') as m:
        cv2.putText(m.array, timestamp, origin, font, scale, color, thickness)

# c = camera.Camera('low')
# c.cam.pre_callback = apply_timestamp

def test_ffmpeg():
    c = camera.Camera()
    c.cam.pre_callback = apply_timestamp
    while True:
        input('Press enter to start recording...')
        fn = helpers.generate_filename()
        c.record(audio_opts + fn)
        input('Press enter to stop recording')
        c.stop_recording()

def simple_record():
    c = camera.Camera()
    c.cam.pre_callback = apply_timestamp
    while True:
        input('Press enter to start recording...')
        fn = helpers.generate_filename()
        c.simple_record(audio_opts + fn)
        input('Press enter to stop recording')
        c.stop_recording()

def test_audio_camera():
    m = audio.Microphone()
    c = camera.Camera()
    c.cam.pre_callback = apply_timestamp
    while True:
        input('Press enter to start recording...')
        fn = helpers.generate_filename()
        c.simple_record(audio_opts + fn)
        m.record_audio(fn)
        input('Press enter to stop recording')
        c.stop_recording()
        m.stop_recording_audio()
    
test_ffmpeg()