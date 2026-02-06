import ctypes
import ok
from src.config import config

if __name__ == '__main__':
    ctypes.windll.user32.SetProcessDPIAware()
    config = config
    ok = ok.OK(config)
    ok.start()
