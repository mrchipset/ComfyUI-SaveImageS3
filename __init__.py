from .nodes.images import SaveImageS3
from .server import *

NODE_CLASS_MAPPINGS = {
    "SaveImageS3": SaveImageS3
}


WEB_DIRECTORY = "./web"