from datetime import datetime
dt_fmt: str = '%d-%m-%y[%H:%M]'
def generate_filename() -> str:
    return datetime.now().strftime(dt_fmt)