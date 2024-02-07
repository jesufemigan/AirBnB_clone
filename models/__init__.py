#!/usr/bin/python3
"""The entry point for the model package"""


from models.engines import file_storage


storage = file_storage.FileStorage()
storage.reload()
