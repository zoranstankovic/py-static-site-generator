from pathlib import Path

from markdown_blocks import markdown_to_html_node


def generate_page(basepath: str, from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)
    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)
    html_page = html_page.replace("href=/", f"href={basepath}")
    html_page = html_page.replace("src=/", f"src={basepath}")
    save_file_to_directory(html_page, dest_path)


def read_file(file_path: str):
    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except PermissionError:
        print(f"Error: Permission denied when trying to access {file_path}.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def save_file_to_directory(content, file_path):
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"File successfully saved to {file_path}")
        return True

    except PermissionError:
        print(f"Error: Permission denied when trying to create directory or write to {file_path}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False


def extract_title(markdown: str) -> str:
    for line in markdown.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:]

    raise ValueError("there is no h1 title")


def generate_pages_recursive(basepath: str, dir_path_content: str, template_path: str, dest_dir_path: str):
    content_path = Path(dir_path_content)
    dest_path = Path(dest_dir_path)

    if not dest_path.exists():
        dest_path.mkdir(parents=True, exist_ok=True)

    for source_item in content_path.iterdir():
        source_path_parts = source_item.parts
        dest_item_path = dest_path / source_path_parts[-1]

        if source_item.is_file():
            dest_path = dest_item_path.with_suffix(".html")
            generate_page(basepath, str(source_item), template_path, dest_path)
        else:
            generate_pages_recursive(basepath, str(source_item), template_path, str(dest_item_path))
