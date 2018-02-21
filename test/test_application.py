import unittest
import tempfile
import shutil
from tasks.filesystem import Filesystem
from tasks.application import Application


class TestApplication(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.fs = Filesystem(prefix=self.tempdir)
        self.app = Application(self.fs)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_is_tasks_suite_active(self):
        self.assertFalse(self.app.is_tasks_suite_active())
