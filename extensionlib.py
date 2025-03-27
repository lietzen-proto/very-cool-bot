import os
import json
from logger import logger

def find_extensions():
    folders_with_index = []
    for root, dirs, files in os.walk("extensions"):
        if "index.json" in files:  # Check if 'index.json' exists in the current folder
            folders_with_index.append(root)  # Add the folder path to the list
    return folders_with_index

def find_extension_info(arg1, arg2):
    with open(arg1) as v1:
        extension = json.load(v1)
        location = extension['script']
        dependencies = extension['dependencies']
        name = extension['name']
        logger('debug', f"location: {location}, dependencies: {dependencies}, selected info: {arg2}")
    if arg2.lower() == "location":
        return location
    if arg2.lower() == "name":
        return name