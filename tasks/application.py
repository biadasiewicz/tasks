import pickle
import os
from .filesystem import Filesystem


class TasksSuiteAlreadyActive(Exception):
    pass


class TasksSuiteNotActive(Exception):
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

    def stop_tasks_suite(self):
        if not self.is_tasks_suite_active():
            raise TasksSuiteNotActive
        else:
            ts = self.load_tasks_suite()
            os.remove(str(self.fs.tasks_suite_path()))
            return ts

    def load_tasks_suite(self):
        if not self.is_tasks_suite_active():
            raise TasksSuiteNotActive
        else:
            with open(self.fs.tasks_suite_path(), 'rb') as f:
                return pickle.load(f)
