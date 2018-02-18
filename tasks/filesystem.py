import os
from pathlib import Path


APP_NAME = "tasks"


class Filesystem:
    def __init__(self, prefix=None):
        self.prefix = prefix if prefix else Path.home()
        p = self.app_dir_path()
        p.mkdir(exist_ok=True)

    def app_dir_path(self):
        dir_name = '.' + APP_NAME
        return self.prefix / Path("." + APP_NAME)
