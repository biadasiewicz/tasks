import sys
from .application import Application, TasksSuiteAlreadyActive
from .tasks_suite import TasksSuite


class CLI:

    msg = {
        "too_few_args": "Too few args",
        "no_tasks": "There is no active tasks suite",
        "already_started": "Tasks suite already started",
        }

    def __init__(self, app=None, stream=None):
        self.app = app if app else Application()
        self.stream = stream if stream else sys.__stdout__

    def execute(self, args):
        if len(args) < 2:
            print(self.msg["too_few_args"], file=self.stream)
            return
        self.run(args)

    def run(self, args):
        command = args[1]
        if command == "status":
            self.status()
        elif command == "start":
            self.start()

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
