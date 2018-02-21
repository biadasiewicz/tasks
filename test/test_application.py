import unittest
import tempfile
import shutil
from tasks.filesystem import Filesystem
from tasks.application import Application, TasksSuiteAlreadyActive
from tasks.tasks_suite import TasksSuite
from tasks.task import Task


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.fs = Filesystem(prefix=self.tempdir)
        self.app = Application(self.fs)
        self.tasks_suite = TasksSuite()
        self.tasks = [Task("1"), Task("2"), Task("3")]

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_is_tasks_suite_active(self):
        self.assertFalse(self.app.is_tasks_suite_active())
        self.app.start_tasks_suite(self.tasks_suite)
        self.assertTrue(self.app.is_tasks_suite_active())

    def test_starting_already_active_tasks_suite(self):
        self.app.start_tasks_suite(self.tasks_suite)
        with self.assertRaises(TasksSuiteAlreadyActive):
            self.app.start_tasks_suite(self.tasks_suite)
