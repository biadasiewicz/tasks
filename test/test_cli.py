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

    def test_start(self):
        self.cli.start()
        output = self.stream.getvalue()
        self.assertEqual(len(output), 0)

    def test_already_started(self):
        self.app.start_tasks_suite(self.tasks_suite)
        self.cli.start()
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["already_started"], output)

    def test_execute_start(self):
        args = ["", "start"]
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertEqual(len(output), 0)
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["already_started"], output)

    def test_stop(self):
        self.app.start_tasks_suite(self.tasks_suite)
        self.cli.stop()
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["stopped"], output)
        self.assertIn(str(self.tasks_suite), output)

    def test_stop_not_started_tasks_suite(self):
        self.cli.stop()
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["no_tasks"], output)

    def test_execute_stop(self):
        args = ["", "stop"]
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["no_tasks"], output)
        self.cli.start()
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["stopped"], output)

    def test_add(self):
        self.app.start_tasks_suite(self.tasks_suite)
        task = Task(1, "task")
        self.cli.add(task)
        self.cli.status()
        output = self.stream.getvalue()
        self.assertIn(str(task), output)

    def test_add_to_not_active_tasks_suite(self):
        task = Task(1, "task")
        self.cli.add(task)
        self.cli.status()
        output = self.stream.getvalue()
        self.assertIn(str(task), output)
        self.assertTrue(self.app.is_tasks_suite_active())

    def test_execute_add(self):
        minutes = 1
        description = "task"
        task = Task(minutes, description)
        args = ["", "add", str(minutes), description]
        self.cli.execute(args)
        self.cli.status()
        output = self.stream.getvalue()
        self.assertIn(str(task), output)

    def test_remove(self):
        self.app.start_tasks_suite(self.tasks_suite)
        self.cli.remove(1)
        self.cli.status()
        output = self.stream.getvalue()
        self.assertNotIn(str(self.task), output)
        self.assertTrue(self.app.is_tasks_suite_active())

    def test_remove_on_not_active_tasks_suite(self):
        self.cli.remove(1)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["no_tasks"], output)
        self.assertFalse(self.app.is_tasks_suite_active())

    def test_remove_invalid_index(self):
        self.app.start_tasks_suite(self.tasks_suite)
        invalid_index = 999
        self.cli.remove(invalid_index)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["index_err"], output)
        self.assertTrue(self.app.is_tasks_suite_active())

        invalid_index = 0
        self.cli.remove(invalid_index)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["index_err"], output)
        self.assertTrue(self.app.is_tasks_suite_active())

    def test_execute_remove(self):
        index = "1"
        ts = self.tasks_suite
        args = ["", "remove", index]
        self.app.start_tasks_suite(ts)
        self.cli.execute(args)
        self.cli.status()
        output = self.stream.getvalue()
        self.assertNotIn(str(ts), output)
        self.assertTrue(self.app.is_tasks_suite_active())

    def test_execute_remove_on_not_active_tasks_suite(self):
        args = ["", "remove", "1"]
        self.assertFalse(self.app.is_tasks_suite_active())
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["no_tasks"], output)
        self.assertFalse(self.app.is_tasks_suite_active())

    def test_execute_remove_invalid_index(self):
        self.app.start_tasks_suite(self.tasks_suite)
        invalid_index = "999"
        args = ["", "remove", invalid_index]
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertIn(CLI.msg["index_err"], output)
        self.assertTrue(self.app.is_tasks_suite_active())

    def test_execute_remove_invalid_index_format(self):
        args = ["", "remove", "xxx"]
        self.app.start_tasks_suite(self.tasks_suite)
        self.cli.execute(args)
        output = self.stream.getvalue()
        self.assertTrue(self.app.is_tasks_suite_active())
