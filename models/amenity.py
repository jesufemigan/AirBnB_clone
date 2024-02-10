#!/usr/bin/python3
"""A module for Amenity class"""

from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class for Amenity"""
    name = ""

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)
