#!/usr/bin/python3
"""A python module for FileStorage class"""


from json import dump, load


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

    def classes(self):
        """Returns all classes"""
        from models.base_model import BaseModel
        from models.amenity import Amenity
        from models.user import User
        from models.state import State
        from models.city import City
        from models.place import Place
        from models.review import Review

        classes = {"BaseModel": BaseModel,
                   "User": User,
                   "State": State,
                   "City": City,
                   "Amenity": Amenity,
                   "Place": Place,
                   "Review": Review}
        return classes

    def reload(self):
        """deserializes the JSON file to objects"""

        # import_classes = __import__('console').import_classes
        # all_objects = import_classes()
        from os import path
        if path.exists(FileStorage.__file_path) \
                and path.getsize(FileStorage.__file_path) > 0:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                loaded_objects = load(f)
                loaded_objects = {k: self.classes()[v["__class__"]](**v)
                                  for k, v in loaded_objects.items()}
                FileStorage.__objects = loaded_objects
