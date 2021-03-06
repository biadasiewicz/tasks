from pathlib import Path


DEFUALT_APP_NAME = "tasks"
TASKS_SUITE_FILENAME = "current"


class Filesystem:
    """Create directories and files for application."""

    def __init__(self, prefix=None, app_name=None):
        self.prefix = prefix if prefix else Path.home()
        self.app_name = app_name if app_name else DEFUALT_APP_NAME
        self.app_dir_path().mkdir(exist_ok=True)

    def app_dir_path(self):
        return self.prefix / Path("." + self.app_name)

    def tasks_suite_path(self):
        return self.app_dir_path() / Path(TASKS_SUITE_FILENAME)
