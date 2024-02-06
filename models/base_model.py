#!/usr/bin/python3
"""A module that define the base class"""
import uuid
from datetime import datetime

class BaseModel():
    """A class that defines all common attributes/methods for other classes"""

    def __init__(self):
        """Constructor"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    def __setattr__(self, name, value):
        """set attribute magic method"""
        if name != "updated_at":
            self.updated_at = datetime.now()
        super().__setattr__(name, value)


    def __str__(self):
        """returns the string representation of BaseModel"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """updates the public instance attribute <updated_at>
        with the current datetime"""
        self.updated_at = datetime.now()

    def to_dict(self):
        """returns a dictionary containing all key/value of __dict__
        instance"""
        new_dict = self.__dict__
        new_dict['__class__'] = self.__class__.__name__
        for key, value in new_dict.items():
            if key == "created_at" or key == "updated_at":
                new_dict[key] = datetime.isoformat(value)
        return new_dict



