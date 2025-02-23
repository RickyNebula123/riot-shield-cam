from libcamera import Transform
from os import path
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder, Quality
import RPi.GPIO as GPIO

# Constants
dt_fmt: str = '%d-%m-%y[%H:%M:%S]'
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

def generate_filename() -> str:
    return datetime.now().strftime(dt_fmt) + '.h264'
        
class Camera:
    def __init__(self, res: str ='low'):
        self.REC: bool = False # Track recording state
        self.cam: Picamera2 = Picamera2()
        self.initialize(res)
    
    def initialize(self, res: str) -> None:
        self.set_resolution(res)
        self.encoder = H264Encoder()
        self.path: str = path.join(path.abspath('..'), 'data/')
        
    def set_resolution(self, res: str) -> None:
        if res == '4K':
            self.set_resolution_4K()
        elif res == 'medium':
            self.set_resolution_medium()
        elif res == 'hd':
            self.set_resolution_hd()
        else:
            self.set_resolution_low()
    
    def set_resolution_low(self) -> None:
        res: dict = resolution_modes['low']
        conf: dict = self.cam.create_preview_configuration(
            transform = Transform(vflip=True),
            sensor = {
                'output_size': res['size'],
                'bit_depth': res['bit_depth']})
        
        self.update(res, conf)
    
    def set_resolution_medium(self) -> None:
        res: dict = resolution_modes['medium']
        conf: dict = self.cam.create_preview_configuration(
            transform = Transform(vflip=True),
            sensor = {
                'output_size': res['size'],
                'bit_depth': res['bit_depth']})
        
        self.update(res, conf)
        
    def set_resolution_hd(self) -> None:
        res: dict = resolution_modes['hd']
        conf: dict = self.cam.create_preview_configuration(
            transform = Transform(vflip=True),
            sensor = {
                'output_size': res['size'],
                'bit_depth': res['bit_depth']})
        
        self.update(res, conf)
        
    def set_resolution_4K(self) -> None:
        res: dict = resolution_modes['4K']
        conf: dict = self.cam.create_preview_configuration(
            transform = Transform(vflip=True),
            sensor = {
                'output_size': res['size'],
                'bit_depth': res['bit_depth']})
        
        self.update(res, conf)
    
    def update(self, res: dict, conf: dict):
        recording: bool = self.cam.started
        
        if recording:
            self.cam.stop()
            
        self.cam.configure(conf)
        
        # Sequence to apply controls (bug?)
        self.cam.start(show_preview=True) 
        self.cam.set_controls({'ScalerCrop': res['crop_limits']})
        
        if not recording:
            self.cam.stop()
        
        self.resolution = res
        
    def record(self, filename: str):
        self.REC = True
        fp: str = path.join(self.path, filename)
        self.cam.start_recording(self.encoder, fp, quality=Quality.MEDIUM)
        
    def stop(self):
        if self.REC:
            self.stop_recording()
            
        if self.cam.started:
            self.cam.stop()
            
    def stop_recording(self):
        if self.REC:
            self.cam.stop_recording()
            self.REC = False
        
    def button_recording(self):
        path_: str = 'recordings/' + datetime.now().strftime(dt_fmt) + '.h264'
        
        while True:
            if GPIO.input(REC_BUTTON) == GPIO.LOW and not self.REC:
                self.record(path_)
                print('Recording in progress...')
                
            _ = input('Press button to stop recording')
            
            if GPIO.input(REC_BUTTON) == GPIO.LOW and self.REC:
                self.stop_recording()
                print('Recording ended')
                print('Breaking out of loop')
                break
        
if __name__ == '__main__':
    riot: Camera = Camera()