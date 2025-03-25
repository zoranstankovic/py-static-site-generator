import os.path
import shutil

from copystatic import copy_static_to_public

static_dir_path = "./static"
public_dir_path = "./public"


def main():
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
        print(f"Deleted {public_dir_path} folder")

    copy_static_to_public(static_dir_path, public_dir_path)


main()
