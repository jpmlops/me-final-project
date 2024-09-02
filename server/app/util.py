from pydantic import BaseModel
import shutil
import os

class FilePaths(BaseModel):
    source: str
    destination: str

def copy_image(source_path: str, destination_path: str) -> None:
    """Copy an image from the source path to the destination path."""
    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
    shutil.copy(source_path, destination_path)

