#!/usr.bin/python3
"""A python module for testing User"""

import unittest
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """A test for User"""

    def test_1_check_subclass(self):
        """Tests if User inherits from BaseModel and instantiates correctly"""
        u = User()
        self.assertIsInstance(u, User)
        self.assertTrue(issubclass(type(u), BaseModel))

    def test_1_instantiation_no_arg(self):
        """Tests if User instantiates correctly with no args"""
        u = User()
        self.assertIsInstance(u, BaseModel)
        self.assertTrue(issubclass(type(u), BaseModel))

    def test_1_instatiation_with_no_args(self):
        "Tests if User instatiate wiht no arg"
        with self.assertRaises(TypeError) as e:
            User.__init__()
        msg = "User.__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_1_instantiation_with_custom_arg(self):
        """Test User instantiation with custom args"""

        my_dict = {
            "name": "John",
            "age": 12,
            "race": "Asian"
        }
        u = User(**my_dict)

        self.assertEqual(u.name, my_dict["name"])
        self.assertEqual(u.age, my_dict["age"])
        self.assertEqual(u.race, my_dict['race'])


if __name__ == "__main__":
    unittest.main()
