import os.path
import shutil

from copystatic import copy_static_to_public
from gencontent import generate_page

static_dir_path = "./static"
public_dir_path = "./public"
content_dir_path = "./content"
template_path = "./template.html"

def main():
    if os.path.exists(public_dir_path):
        shutil.rmtree(public_dir_path)
        print(f"Deleted {public_dir_path} folder")

    copy_static_to_public(static_dir_path, public_dir_path)

    index_md_path = os.path.join(content_dir_path, "index.md")
    index_html_path = os.path.join(public_dir_path, "index.html")

    generate_page(index_md_path, template_path, index_html_path)


main()
