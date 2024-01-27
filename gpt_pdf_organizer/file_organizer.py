import os
import glob
from typing import List

def read_pdf_files_from_path(path: str) -> List[str]:
    if os.path.isdir(path):
    files = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            files.append(os.path.join(folder_path, file))
    return files
