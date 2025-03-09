import time

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

# Constants
audio_device_name: str = 'alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-mono'

picam2 = Picamera2()
video_config = picam2.create_video_configuration()
picam2.configure(video_config)

encoder = H264Encoder()
output = FfmpegOutput('test.mp4', audio=True, \
                      audio_device=audio_device_name, \
                      audio_filter='[0:a:0]channelmap=channel_layout=stereo')

picam2.start_recording(encoder, output)
input('Enter a value to stop recording...')
picam2.stop_recording()