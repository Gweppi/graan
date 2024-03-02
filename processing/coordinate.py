from PIL import Image
from PIL.TiffTags import TAGS

with Image.open('output/openEO.tif') as img:
    meta_dict = {TAGS[key] : img.tag[key] for key in img.tag.keys()}