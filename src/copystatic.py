import os.path
import shutil


def copy_static_to_public(source, destination):
    if not os.path.exists(destination):
        os.mkdir(destination)

    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
            print(f"Copied file: {source_path} -> {dest_path}")
        else:
            copy_static_to_public(source_path, dest_path)