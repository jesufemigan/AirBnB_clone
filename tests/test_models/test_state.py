#!/usr/bin/python3
"""A python module for testing State"""

import unittest
from models.state import State
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """A test for State"""

    def test_1_check_subclass(self):
        """Tests if State inherits from BaseModel and instantiates correctly"""
        u = State()
        self.assertIsInstance(u, State)
        self.assertTrue(issubclass(type(u), BaseModel))

    def test_1_instantiation_no_arg(self):
        """Tests if State instantiates correctly with no args"""
        u = State()
        self.assertIsInstance(u, BaseModel)
        self.assertTrue(issubclass(type(u), BaseModel))

    def test_1_instatiation_with_no_args(self):
        "Tests if State instatiate wiht no arg"
        with self.assertRaises(TypeError) as e:
            State.__init__()
        msg = "__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_1_instantiation_with_custom_arg(self):
        """Test State instantiation with custom args"""

        my_dict = {
            "name": "John",
            "age": 12,
            "race": "Asian"
        }
        u = State(**my_dict)

        self.assertEqual(u.name, my_dict["name"])
        self.assertEqual(u.age, my_dict["age"])
        self.assertEqual(u.race, my_dict['race'])

    if __name__ == "__main__":
        unittest.main()
