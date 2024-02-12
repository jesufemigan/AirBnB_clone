#!/usr/bin/python3
"""Tests for the console"""


import unittest
from console import HBNBCommand
from unittest.mock import patch
from io import StringIO


class TestConsole(unittest.TestCase):
    """Tests for the console"""

    def test_1_prompt(self):
        """Test the prompt"""
        self.assertTrue("(hbnb) ", HBNBCommand.prompt)

    def test_2_empty_line(self):
        """Test empty line"""
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

    if __name__ == "__main__":
        unittest.main()
