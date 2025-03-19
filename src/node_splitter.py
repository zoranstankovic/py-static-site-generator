import re

from src.textnode import TextNode
from textnode import TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown syntax: unclosed inline element")

        for i in range(len(split_text)):
            if not split_text[i]:
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text: str):
    """
    Match all images inside of Markdown text with alt text
    like ![alt text](http://example.com) and returns list of tuples
    [('alt text', 'http://example.com')]
    :param text: str
    :return: list
    """
    return re.findall(r"!\[([^\[\]]*)]\(([^()]*)\)", text)

def extract_markdown_links(text: str):
    """
    Extract standard Markdown links from text.

    This function identifies and extracts all standard Markdown links formatted as
    [link text](URL) from the input text. It intentionally excludes Markdown image
    syntax ![alt text](URL) through the use of a negative lookbehind in the regex pattern.

    Args:
        text (str): The Markdown text to search for links.

    Returns:
        list: A list of tuples, where each tuple contains two elements:
              - The link text (str): The text between square brackets
              - The URL (str): The URL between parentheses

    Example:
        >>> extract_markdown_links("Check out [Google](https://google.com) and ![image](img.jpg)")
        [('Google', 'https://google.com')]
    :param text: str
    :return: list
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)]\(([^()]*)\)", text)
