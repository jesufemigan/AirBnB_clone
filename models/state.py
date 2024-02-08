#!/usr/bin/python3
"""A module for State class"""

from models.base_model import BaseModel


class State(BaseModel):
    """A class for State"""
    name = ""
    
    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)