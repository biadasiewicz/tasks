import unittest
from datetime import datetime
from tasks.tasks_suite import TasksSuite

class TestTaskSuite(unittest.TestCase):
    def setUp(self):
        self.start = datetime.now()
        self.t1 = TasksSuite(self.start)
        self.t2 = TasksSuite(self.start)

    def test_equality(self):
        self.assertEqual(self.t1, self.t2)
        self.assertEqual(self.t1.start, self.start)
        self.assertEqual(self.t2.start, self.start)

    def test_adding_and_removing_tasks(self):
        tasks = [0, 1, 2]

        self.t1.extend(tasks)
        self.t2.extend(tasks)
        self.assertEqual(self.t1, self.t2)

        self.t1.append(3)
        self.assertNotEqual(self.t1, self.t2)

        # '3' is index
        self.t1.pop(3)
        self.assertEqual(self.t1, self.t2)
