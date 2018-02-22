import unittest
import tempfile
import shutil
from tasks.filesystem import Filesystem
from tasks.application import Application,\
                              TasksSuiteAlreadyActive,\
                              TasksSuiteNotActive
from tasks.tasks_suite import TasksSuite
from tasks.task import Task


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.fs = Filesystem(prefix=self.tempdir)
        self.app = Application(self.fs)
        self.tasks_suite = TasksSuite()
        self.tasks = [Task(1, "1"), Task(2, "2"), Task(3, "3")]
        self.tasks_suite.extend(self.tasks)

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

    def test_stop_tasks_suite(self):
        self.app.start_tasks_suite(self.tasks_suite)
        self.assertTrue(self.app.is_tasks_suite_active())
        stopped_tasks_suite = self.app.stop_tasks_suite()
        self.assertFalse(self.app.is_tasks_suite_active())
        self.assertEqual(self.tasks_suite, stopped_tasks_suite)

    def test_stopping_not_active_tasks_suite(self):
        self.assertFalse(self.app.is_tasks_suite_active())
        with self.assertRaises(TasksSuiteNotActive):
            self.app.stop_tasks_suite()

    def test_show_status(self):
        self.app.start_tasks_suite(self.tasks_suite)
        output = self.app.show_status()
        for t in self.tasks:
            self.assertIn(t.description, output)

    def test_show_status_not_active_tests_suite(self):
        self.assertFalse(self.app.is_tasks_suite_active())
        output = self.app.show_status()
        self.assertIs(output, None)

    def shift_tasks_suite(self, minutes):
        self.app.start_tasks_suite(self.tasks_suite)
        self.app.shift_tasks_suite_in_time(minutes)
        self.shifted_tasks_suite = self.app.load_tasks_suite()

    def test_shift_tasks_suite_in_time_forward(self):
        minutes = 1
        self.shift_tasks_suite(minutes)
        self.assertLess(self.tasks_suite.start,
                        self.shifted_tasks_suite.start)

    def test_shift_tasks_suite_in_time_backward(self):
        minutes = -1
        self.shift_tasks_suite(minutes)
        self.assertGreater(self.tasks_suite.start,
                           self.shifted_tasks_suite.start)
