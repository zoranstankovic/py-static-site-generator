from markdown_blocks import markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)
    title = extract_title(markdown)
    html_content = markdown_to_html_node(markdown).to_html()
    html_page = template.replace("{{ Title }}", title)
    html_page = html_page.replace("{{ Content }}", html_content)
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
