import os.path
import shutil
import sys

from copystatic import copy_static_to_public
from gencontent import generate_pages_recursive

static_dir_path = "./static"
public_dir_path = "./docs"
content_dir_path = "./content"
template_path = "./template.html"
default_basepath = "/"


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else default_basepath
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
        print(f"Deleted {public_dir_path} folder")

    copy_static_to_public(static_dir_path, public_dir_path)

    generate_pages_recursive(basepath, content_dir_path, template_path, public_dir_path)


main()
