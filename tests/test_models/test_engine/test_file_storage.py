#!/usr/bin/python3


"""A module to test filestorge"""


import unittest
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test filestorage"""

    def test_1_instantiation(self):
        """Test instantiate file storage"""
        f = FileStorage()
        self.assertIsInstance(f, FileStorage)

    def test_1_correct_file_name(self):
        """Tests if file path is named file.json"""
        f = FileStorage()
        self.assertTrue(FileStorage._FileStorage__file_path, "file.json")

    if __name__ == "__main__":
        unittest.main()
