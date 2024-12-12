"""
@author: Mr.Chip
@title: SaveImageS3
@nickname: SaveImageS3
@description: This extension offers a custom node to save image to S3-compatible oss.
"""
from .nodes.images import SaveImageS3
from .server import *

NODE_CLASS_MAPPINGS = {
    "SaveImageS3": SaveImageS3
}


WEB_DIRECTORY = "./web"