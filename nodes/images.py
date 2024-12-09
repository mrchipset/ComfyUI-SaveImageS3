from nodes import SaveImage
import importlib
import numpy as np
from comfy.cli_args import args
import os
from io import BytesIO

from PIL import Image, ImageOps
from PIL.ExifTags import TAGS, GPSTAGS, IFD
from PIL.PngImagePlugin import PngImageFile, PngInfo
from PIL.JpegImagePlugin import JpegImageFile

import json

import folder_paths

from ..common import get_s3_client, S3Client
class SaveImageS3(SaveImage):
    def __init__(self):
        super().__init__()

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"tooltip": "The images to save."}),
                "filename_prefix": ("STRING", {"default": "ComfyUI", "tooltip": "The prefix for the file to save. This may include formatting information such as %date:yyyy-MM-dd% or %Empty Latent Image.width% to include values from nodes."})
            },
            "hidden": {
                "prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "save_images"

    OUTPUT_NODE = True

    CATEGORY = "image"
    DESCRIPTION = "Saves the input images to your S3 storage."

    def save_images(self, images, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        s3_client = get_s3_client()
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, images[0].shape[1], images[0].shape[0])
        results = list()
        for (batch_number, image) in enumerate(images):
            i = 255. * image.cpu().numpy()
            img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))
            metadata = None
            if not args.disable_metadata:
                metadata = PngInfo()
                if prompt is not None:
                    metadata.add_text("prompt", json.dumps(prompt))
                if extra_pnginfo is not None:
                    for x in extra_pnginfo:
                        metadata.add_text(x, json.dumps(extra_pnginfo[x]))

            filename_with_batch_num = filename.replace("%batch_num%", str(batch_number))
            file = f"{filename_with_batch_num}_{counter:05}_.png"
            # save meta info in json file
            meta_file = f"{filename_with_batch_num}_{counter:05}_.json"
            oss_meta = {}
            oss_meta["prompt"] = prompt
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    oss_meta[x] = extra_pnginfo[x]
            data = BytesIO()
            img.save(data, format="PNG", pnginfo=metadata, compress_level=self.compress_level)
            data.seek(0)
            oss_meta_json = json.dumps(oss_meta, indent=4).encode('utf-8')
            s3_client.upload_image(file, data)
            s3_client.upload_meta(meta_file, BytesIO(oss_meta_json))
            img.save(os.path.join(full_output_folder, file), pnginfo=metadata, compress_level=self.compress_level)
            results.append({
                "filename": file,
                "subfolder": subfolder,
                "type": self.type
            })
            counter += 1

        return { "ui": { "images": results } }
    