#!/usr/bin/python3
"""A module for Review class"""

from models.base_model import BaseModel


class Review(BaseModel):
    """A class for Review"""
    place_id = ""
    user_id = ""
    text = ""
    
    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)