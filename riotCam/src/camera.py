from libcamera import Transform
from os import path
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
import RPi.GPIO as GPIO

# Constants
REC_BUTTON: int = 20
GPIO.setmode(GPIO.BCM)
GPIO.setup(REC_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
    def __init__(self, res: str ='low'):
        self.REC: bool = False # Track recording state
        self.cam: Picamera2 = Picamera2()
        self.initialize(res)
    
    def initialize(self, res: str) -> None:
        self.set_resolution(res)
        self.encoder = H264Encoder()
        
    def set_resolution(self, res: str) -> None:
        if res not in resolution_modes.keys():
            res = 'low'
        self._set_resolution_(res)
    
    def _set_resolution_(self, video_res: str) -> None:
        res: dict = resolution_modes[video_res]
        conf: dict = self.cam.create_preview_configuration(
            transform = Transform(vflip=True),
            sensor = {
                'output_size': res['size'],
                'bit_depth': res['bit_depth']})
        
        self.update(res, conf)
    
    def update(self, res: dict, conf: dict):
        output: bool = self.cam.started
        
        if output:
            self.cam.stop()
            
        self.cam.configure(conf)
        
        # Sequence to apply controls (bug?)
        self.cam.start(show_preview=True) 
        self.cam.set_controls({'ScalerCrop': res['crop_limits']})
        
        if not output:
            self.cam.stop()
        
        self.resolution = res
        
    def record(self, filename: str):
        self.REC = True
        self.cam.start_recording(self.encoder, filename + '.h264', quality=Quality.MEDIUM)
        
    def stop(self):
        if self.REC:
            self.stop_recording()
            
        if self.cam.started:
            self.cam.stop()
            
    def stop_recording(self):
        if self.REC:
            self.cam.stop_recording()
            self.REC = False
            
if __name__ == '__main__':
    import helpers
    c = Camera('low')
    c.cam.start(show_preview=True)
    c.record(helpers.generate_filename() + '.h264')
    
    input('Enter any key to stop recording: >>')
    c.stop()