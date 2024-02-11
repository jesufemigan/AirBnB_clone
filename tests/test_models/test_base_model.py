#!/usr/bin/python3
"""A python module for testing BaseModel"""


import re
import json
import uuid
import os
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
import unittest


class TestBaseModel(unittest.TestCase):
    """A test for the BaseModel Class"""

    def test_1_instantiation_no_arg(self):
        """Tests if the class is instantiated correctly with no arg"""
        b = BaseModel()
        self.assertEqual(str(type(b)), "<class 'models.base_model.BaseModel'>")
        self.assertIsInstance(b, BaseModel)
        self.assertTrue(issubclass(type(b), BaseModel))

    def test_1_instantiation_with_arg(self):
        """instantiation woth **kwargs"""
        b = BaseModel()
        b.name = "John"
        b.age = 88
        b_json = b.to_dict()
        new_model = BaseModel(**b_json)
        self.assertEqual(new_model.to_dict(), b_json)

    def test_1_instantiation_with_custom_dict(self):
        """Tests instantiation with custom dict **kwargs"""
        custom_dict = {
            "__class__": "BaseModel",
            "id": uuid.uuid4(),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "name": "John",
            "age": 22,
            "gender": "male"
        }
        new_model = BaseModel(**custom_dict)
        self.assertEqual(new_model.to_dict(), custom_dict)

    def test_2_initialization_no_args(self):
        """Test that class is intialized with no args"""
        with self.assertRaises(TypeError) as e:
            BaseModel.__init__()
        msg = "BaseModel.__init__() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_3_id_is_unique(self):
        """Test that id is unique"""
        b = BaseModel()
        c = BaseModel()
        self.assertNotEqual(b.id, c.id)

    def test_4_datetime_created(self):
        """Test if the dates created matched with current time"""
        current_date = datetime.now()
        b = BaseModel()
        diff = b.updated_at - b.created_at
        self.assertTrue(abs(diff.total_seconds()) < 0.01)
        diff = b.created_at - current_date
        self.assertTrue(abs(diff.total_seconds()) < 0.1)

    def test_5_str_method(self):
        """Test if str method is correct"""
        b = BaseModel()
        rex = re.compile(r"^\[(.*)\] \((.*)\) (.*)$")
        res = rex.match(str(b))
        self.assertIsNotNone(res)
        self.assertEqual(res.group(1), "BaseModel")
        self.assertEqual(res.group(2), b.id)
        s = res.group(3)
        s = re.sub(r"(datetime\.datetime\([^)]*\))", "'\\1'", s)
        d = json.loads(s.replace("'", '"'))
        d2 = b.__dict__.copy()
        d2["created_at"] = repr(d2["created_at"])
        d2["updated_at"] = repr(d2["updated_at"])
        self.assertEqual(d, d2)

    def test_6_to_dict_method(self):
        """Tests the to_dict method"""
        b = BaseModel()
        b.name = "Ade"
        b.age = 30
        d = b.to_dict()
        self.assertEqual(d["id"], b.id)
        self.assertEqual(d["__class__"], b.__class__.__name__)
        self.assertEqual(d["created_at"], b.created_at.isoformat())
        self.assertEqual(d["updated_at"], b.updated_at.isoformat())
        self.assertEqual(d["name"], b.name)
        self.assertEqual(d["age"], b.age)

    def test_6_to_dict_no_args(self):
        """Initialize to_dict method with no args"""
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict()
        msg = "BaseModel.to_dict() missing 1 required "\
            "positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_6_to_dict_excess_arg(self):
        """Initialize to_dict method with excess args"""
        with self.assertRaises(TypeError) as e:
            BaseModel.to_dict(self, 12)
        msg = "BaseModel.to_dict() takes 1 positional argument "\
            "but 2 were given"
        self.assertEqual(str(e.exception), msg)

    # def test_7_save_method(self):
    #     """Test the save method"""
    #     b = BaseModel()
    #     b.save()
    #     dict_key = f"{b.__class__.__name__}.{b.id}"
    #     my_dict = {dict_key: b.to_dict()}
    #     self.assertTrue(os.path.isfile(FileStorage._FileStorage__file_path))
    #     with open(FileStorage._FileStorage__file_path, "r",
    #               encoding="utf-8") as f:
    #         self.assertEqual(len(f.read()), len(json.dumps(my_dict)))
    #         f.seek(0)
    #         self.assertEqual(json.load(f), my_dict)

    def test_7_save_method_init_no_args(self):
        """Test the save method with no args"""
        with self.assertRaises(TypeError) as e:
            BaseModel.save()
        msg = "BaseModel.save() missing 1 required positional argument: 'self'"
        self.assertEqual(str(e.exception), msg)

    def test_7_save_method_init_excess_args(self):
        """Test the save method with excess arguments"""
        with self.assertRaises(TypeError) as e:
            BaseModel.save(self, 8)
        msg = "BaseModel.save() takes 1 positional argument "\
            "but 2 were given"
        self.assertEqual(str(e.exception), msg)

    if __name__ == "__main__":
        unittest.main()
