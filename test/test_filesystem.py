import unittest
import tempfile
import shutil
from tasks.filesystem import Filesystem, TASKS_SUITE_FILENAME


class TestFilesystem(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.app_name = 'tasks_app'
        self.fs = Filesystem(self.tempdir, self.app_name)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_initialization(self):
        self.assertTrue(self.fs.app_dir_path().exists())

        self.assertIn(self.tempdir, self.fs.prefix)
        self.assertIn(self.app_name, self.fs.app_name)

    def test_tasks_suite_path(self):
        self.assertIn(TASKS_SUITE_FILENAME, str(self.fs.tasks_suite_path()))
