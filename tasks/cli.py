import sys
from tasks.application import Application


class CLI:

    msg = {
        "too_few_args": "Too few args",
        "no_tasks": "There is no active tasks suite",
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

    def status(self):
        output = self.app.show_status()
        if output is None:
            output = self.msg["no_tasks"]
        print(output, file=self.stream)
