#!/usr/bin/python3
"""The entry point for the model package"""


from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
