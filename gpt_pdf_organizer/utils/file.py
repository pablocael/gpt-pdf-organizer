"""
File related functions
"""
import os
import glob

from gpt_pdf_organizer.app.exception import FilepathNotSupportedException
from typing import List

def read_files_from_path(path: str, extension: str) -> List[str]:
    if os.path.isfile(path) and path.endswith(f".{extension}"):
        return [path]
    elif not os.path.isdir(path):
        raise FilepathNotSupportedException(
            "Path does not contains file extension nor is directory")

    # List of all PDF files in the directory
    return list(sorted(glob.glob(f"{path}/*.{extension}")))
