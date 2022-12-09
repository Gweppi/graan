import os
import zipfile
from pathlib import Path
from search import searchImages

def unzip():
    files = os.listdir('./')

    zippedfile = ''

    for file in files:
        if file.endswith('.zip'):
            zippedfile = file

    print(zippedfile)

    with zipfile.ZipFile(Path(__file__).with_name(zippedfile), 'r') as zip_ref:
        zip_ref.extractall(os.getcwd())

    searchImages()