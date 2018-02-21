class Application:
    def __init__(self, fs=None):
        self.fs = fs if fs else Filesystem()

    def is_tasks_suite_active(self):
        return self.fs.tasks_suite_path().exists()
