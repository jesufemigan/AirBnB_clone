#!/usr/bin/python3
"""A module for City class"""

from models.base_model import BaseModel


class City(BaseModel):
    """A class for City"""
    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Constructor"""
        super().__init__(*args, **kwargs)
