import unittest
import tasks.task as task


class TestTask(unittest.TestCase):
    def test_init(self):
        t = task.Task()
        self.assertEqual(t.minutes, task.DEFAULT_MINUTES)
        self.assertEqual(t.description, task.DEFAULT_DESCRIPTION)

        mins = 30
        desc = "description"
        t = task.Task(mins, desc)
        self.assertEqual(t.minutes, mins)
        self.assertEqual(t.description, desc)
