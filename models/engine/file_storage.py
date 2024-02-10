#!/usr/bin/python3
"""A python module for FileStorage class"""


from json import dumps, loads, dump, load
from datetime import datetime


class FileStorage():
    """A class that serializes instances to a JSON file and deserializes
    JSON file to instances"""

    def __init__(self):
        """Constructor"""
        self.__file_path = "file.json"
        self.__objects = {}

    def all(self):
        """returns the dictionary objects"""
        return self.__objects

    def new(self, obj):
        """sets unique object in class object"""
        self.__objects[f"{obj.__class__.__name__}.{obj.id}"] = obj.to_dict()

    def save(self):
        """serializes object to the JSON file"""
        with open(self.__file_path, "w", encoding="utf-8") as f:
            dump(self.__objects, f)

    def reload(self):
        """deserializes the JSON file to objects"""
        from os import path
        if path.exists(self.__file_path) \
                and path.getsize(self.__file_path) > 0:
            with open(self.__file_path, "r", encoding="utf-8") as f:
                self.__objects = load(f)
