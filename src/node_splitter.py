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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNodes containing markdown image syntax into separate TextNodes.

    Each text node of type TextType.TEXT is examined for markdown image patterns.
    When found, the node is split into multiple nodes:
    - Text before the image becomes a TEXT node
    - The image becomes an IMAGE node with the alt text as content and the URL as url
    - Text after the image becomes a TEXT node

    Nodes with no images or non-TEXT type nodes are preserved as is.

    Example:
        If a node contains: "Text with ![alt](url) and more text"
        It becomes three nodes:
        1. TextNode("Text with ", TextType.TEXT)
        2. TextNode("alt", TextType.IMAGE, "url")
        3. TextNode(" and more text", TextType.TEXT)
    :param old_nodes: list[TextNode] - List of TextNode objets to process
    :return: list[TextNode] - New list with text nodes split at image markers
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extracted_images = extract_markdown_images(old_node.text)

        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text

        for image_alt, image_link in extracted_images:
            image_markdown = f"![{image_alt}]({image_link})"
            # Split at the image markdown, max 1 split
            parts = current_text.split(image_markdown, 1)

            if len(parts) != 2:
                raise ValueError("invalid markdown, image section not closed")
            # Add text before the image if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the image node
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))

            # Update current_text to be everything after the image
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Splits TextNodes containing markdown link syntax into separate TextNodes.

    Each text node of type TextType.TEXT is examined for markdown link patterns.
    When found, the node is split into multiple nodes:
    - Text before the link becomes a TEXT node
    - The link becomes an LINK node with the alt text as content and the URL as url
    - Text after the link becomes a TEXT node

    Nodes with no link or non-TEXT type nodes are preserved as is.

    Example:
        If a node contains: "Text with [alt](url) and more text"
        It becomes three nodes:
        1. TextNode("Text with ", TextType.TEXT)
        2. TextNode("alt", TextType.LINK, "url")
        3. TextNode(" and more text", TextType.TEXT)
    :param old_nodes: list[TextNode] - List of TextNode objets to process
    :return: list[TextNode] - New list with text nodes split at link markers
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        extracted_links = extract_markdown_links(old_node.text)

        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        current_text = old_node.text

        for link_text, link_url in extracted_links:
            link_markdown = f"[{link_text}]({link_url})"

            # Split at the link markdown, max 1 split
            parts = current_text.split(link_markdown, 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown, link section not closed")

            # Add text before the link if not empty
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))

            # Add the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            # Update current_text to be everything after the link
            if len(parts) > 1:
                current_text = parts[1]
            else:
                current_text = ""

        if current_text:
            new_nodes.append(TextNode(current_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    text_nodes = [TextNode(text, TextType.TEXT)]
    text_nodes = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)

    return text_nodes
