import unittest
import tempfile
import shutil
from io import StringIO
from tasks.cli import CLI
from tasks.filesystem import Filesystem
from tasks.application import Application
from tasks.task import Task
from tasks.tasks_suite import TasksSuite


class TestCLI(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.fs = Filesystem(prefix=self.tempdir)
        self.app = Application(self.fs)
        self.stream = StringIO()
        self.cli = CLI(self.app, self.stream)
        self.task = Task(30, "desc")
        self.tasks_suite = TasksSuite()
        self.tasks_suite.append(self.task)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        self.stream.close()

    def test_execute_too_few_args(self):
        args = [""]
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["too_few_args"], output)

    def test_status(self):
        self.cli.status()
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["no_tasks"], output)
        self.app.start_tasks_suite(self.tasks_suite)
        self.cli.status()
        output = self.stream.getvalue()
        self.assertIn(str(self.task), output)

    def test_execute_status(self):
        args = ["", "status"]
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["no_tasks"], output)
        self.app.start_tasks_suite(self.tasks_suite)
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(str(self.task), output)
