from libcamera import Transform
from os import path
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FfmpegOutput

from pprint import pprint

import RPi.GPIO as GPIO

# Constants
REC_BUTTON: int = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(REC_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
audio_device_name: str = 'alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-mono'

# Crop Regions
mid_screen:  tuple[int, int, int, int] = (0, 0, 1920, 1080)
full_screen: tuple[int, int, int, int] = (0, 0, 3280, 2464)

resolution_modes: dict[str, dict] = {
      'low':{'bit_depth': 10,
      'res':'low',
      'crop_limits': (1000, 752, 1280, 960), # Represents how much we can 'zoom'
      'exposure_limits': (37, 5883414, None),
      'fps': 206.65,
      'size': (640, 480),
      'unpacked': 'SRGGB10'},
    'medium': {'bit_depth': 10,
      'res':'medium',
      'crop_limits': (0, 0, 3280, 2464),
      'exposure_limits': (75, 11766829, None),
      'fps': 41.85,
      'size': (1640, 1232),
      'unpacked': 'SRGGB10'},
    'hd': {'bit_depth': 10,
      'res':'hd',
      'crop_limits': (680, 692, 1920, 1080),
      'exposure_limits': (75, 11766829, None),
      'fps': 47.57,
      'size': (1920, 1080),
      'unpacked': 'SRGGB10'},
     '4K': {'bit_depth': 10,
      'res':'4K',
      'crop_limits': (0, 0, 3280, 2464),
      'exposure_limits': (75, 11766829, None),
      'fps': 21.19,
      'size': (3280, 2464),
      'unpacked': 'SRGGB10'},
    }
        
class Camera:
    def __init__(self, res: str ='low', prev: bool = False):
        self.REC: bool = False # Track recording state
        self.prev: bool = prev
        self.cam: Picamera2 = Picamera2()
        self.initialize(res)
        self.encoder = H264Encoder(bitrate=8000000)
    
    def initialize(self, res: str) -> None:
        self.set_resolution(res)
        
    def set_resolution(self, res: str) -> None:
        if res not in resolution_modes.keys():
            res = 'low'
        self._set_resolution_(res)
    
    def _set_resolution_(self, video_res: str) -> None:
        res: dict = resolution_modes[video_res]
        conf: dict = self.cam.create_video_configuration()
        self.update(res, conf)
    
    def update(self, res: dict, conf: dict):
        output: bool = self.cam.started
        
        if output:
            self.cam.stop()
            
        self.cam.configure(conf)
        self.cam.set_controls({'ScalerCrop': res['crop_limits'],
                               'NoiseReductionMode': 0,
                               'Sharpness': 0.0})

    def record(self, filename: str):
        self.REC = True
        output = FfmpegOutput(filename+'.mp4',
                              audio=True,
                              audio_device=audio_device_name)
        
        self.cam.start_recording(encoder=self.encoder, output=output)
    
    def simple_record(self, filename):
        self.REC = True
        self.cam.start_recording(self.encoder, filename + '.h264')
    
    def testcord(self, filename: str):
        self.REC = True
        output = FfmpegOutput(filename+'.mp4',
                              audio=True,
                              audio_device=audio_device_name)
        self.cam.start_encoder(self.encoder, output)
    
    def stopcording(self):
        self.cam.stop_encoder()
    
    def stop_recording(self):
        if self.REC:
            self.cam.stop_recording()
            self.REC = False
            