#!/usr/bin/python3
"""A class User that inherits from BaseModel"""

from models.base_model import BaseModel


class User(BaseModel):
    """A class User"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
    def __init__(self, *args, **kwargs):
        """Costructor"""
        super().__init__(*args, **kwargs)