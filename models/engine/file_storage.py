#!/usr/bin/python3
"""A python module for FileStorage class"""


from json import dump, load
import os, inspect, importlib


class FileStorage():
    """A class that serializes instances to a JSON file and deserializes
    JSON file to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary objects"""
        return FileStorage.__objects

    def new(self, obj):
        """sets unique object in class object"""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def save(self):
        """serializes object to the JSON file"""
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            d = {k: v.to_dict() for k, v in FileStorage.__objects.items()}
            dump(d, f)

    def reload(self):
        """deserializes the JSON file to objects"""
        # import_classes = __import__('console').import_classes
        def import_classes():
            """Import all classes"""
            # models_path = os.path.join(os.path.dirname(__file__), 'models')
            models_path = os.chdir('../')
            class_objects = {}
            for file_name in os.listdir(models_path):
                if file_name.endswith('.py') and file_name != '__init__.py':
                    module_name = file_name[:-3]
                    module = importlib.import_module(f"models.{module_name}")
                    members = inspect.getmembers(module, inspect.isclass)
                    class_objects.update({name: obj for name, obj in members})
            return class_objects
        all_objects = import_classes()
        from os import path
        if path.exists(FileStorage.__file_path) \
                and path.getsize(FileStorage.__file_path) > 0:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                loaded_objects = load(f)
                loaded_objects = {k: all_objects[v["__class__"]](**v)
                                  for k, v in loaded_objects.items()}
                FileStorage.__objects = loaded_objects
