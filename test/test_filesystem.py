import unittest
import tempfile
import shutil
from tasks.filesystem import Filesystem

class TestFilesystem(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.fs = Filesystem(self.tempdir)

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_initialization(self):
        p = self.fs.app_dir_path()
        self.assertTrue(p.exists())
