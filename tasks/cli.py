import sys
from .application import Application,\
                         TasksSuiteAlreadyActive,\
                         TasksSuiteNotActive
from .tasks_suite import TasksSuite
from .task import Task


class CLI:

    msg = {
        "too_few_args": "Too few options given",
        "no_tasks": "There is no active tasks suite",
        "already_started": "Tasks suite already started",
        "stopped": "Tasks suite stopped",
        "index_err": "Index is invalid",
        "index_format_err": "Index format is invalid",
        }

    def __init__(self, app=None, stream=None):
        self.app = app if app else Application()
        self.stream = stream if stream else sys.__stdout__

    def execute(self, args):
        try:
            command = args[1]
            if command == "status":
                self.status()
            elif command == "start":
                self.start()
            elif command == "stop":
                self.stop()
            elif command == "add":
                self.add(Task(args[2], args[3]))
            elif command == "remove":
                self.remove(args[2])
        except IndexError as e:
            print(self.msg["too_few_args"], file=self.stream)

    def status(self):
        output = self.app.show_status()
        if output is None:
            output = self.msg["no_tasks"]
        print(output, file=self.stream)

    def start(self):
        ts = TasksSuite()
        try:
            self.app.start_tasks_suite(ts)
        except TasksSuiteAlreadyActive:
            print(self.msg["already_started"], file=self.stream)

    def stop(self):
        try:
            ts = self.app.stop_tasks_suite()
            print(self.msg["stopped"], file=self.stream)
            print(ts, file=self.stream)
        except TasksSuiteNotActive:
            print(self.msg["no_tasks"], file=self.stream)

    def add(self, task):
        if self.app.is_tasks_suite_active():
            ts = self.app.stop_tasks_suite()
        else:
            ts = TasksSuite()
        ts.append(task)
        self.app.start_tasks_suite(ts)

    def remove(self, index):
        try:
            index = int(index)
            index = index - 1
        except ValueError:
            print(self.msg["index_format_err"], file=self.stream)
            return
        try:
            ts = self.app.stop_tasks_suite()
        except TasksSuiteNotActive:
            print(self.msg["no_tasks"], file=self.stream)
            return
        try:
            ts.pop(index)
        except IndexError:
            print(self.msg["index_err"], file=self.stream)
        finally:
            self.app.start_tasks_suite(ts)
