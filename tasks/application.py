import pickle
from .filesystem import Filesystem


class TasksSuiteAlreadyActive(Exception):
    pass


class Application:
    def __init__(self, fs=None):
        self.fs = fs if fs else Filesystem()

    def is_tasks_suite_active(self):
        return self.fs.tasks_suite_path().exists()

    def start_tasks_suite(self, ts):
        if self.is_tasks_suite_active():
            raise TasksSuiteAlreadyActive
        else:
            with open(self.fs.tasks_suite_path(), 'wb') as f:
                pickle.dump(ts, f)
