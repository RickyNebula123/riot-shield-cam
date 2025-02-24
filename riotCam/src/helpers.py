from os import path
from datetime import datetime

# Constants
dt_fmt: str = '%d-%m-%y[%H:%M]'
save_path: str = path.join(path.abspath('..'), 'data/')

def generate_filename() -> str:
    return save_path + datetime.now().strftime(dt_fmt)