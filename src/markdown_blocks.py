import re
from enum import Enum

from htmlnode import HTMLNode, ParentNode
from node_splitter import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    """
    Enumeration of different markdown block types that can be identified.

    Attributes:
        PARAGRAPH: Regular text paragraph
        HEADING: Any level of heading (h1-h6)
        CODE: Code block surrounded by triple backticks
        QUOTE: Blockquote prefixed with '>'
        UNORDERED_LIST: List with bullet points
        ORDERED_LIST: Numbered list
    """
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


ALLOWED_HEADINGS = ("# ", "## ", "### ", "#### ", "##### ", "###### ")


def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Splits a markdown string into individual content blocks.

    This function separates markdown content into discrete blocks by splitting
    on double newlines, which is the standard markdown way to separate blocks.
    It removes empty blocks and leading/trailing whitespace from each block.

    Args:
        markdown (str): The raw Markdown text to be processed

    Returns:
        list[str]: A list of individual markdown blocks with whitespace trimmed

    Example:
        >>> text = "# Header\\n\\nParagraph text\\n\\n```\\ncode block\\n```"
        >>> markdown_to_blocks(text)
        ['# Header', 'Paragraph text', '```\\ncode block\\n```']
    """
    blocks = []
    for block in markdown.split("\n\n"):
        clean_block = block.strip()
        if not clean_block:
            continue
        blocks.append(clean_block)

    return blocks


def block_to_block_type(block: str) -> BlockType:
    """
    Determines the markdown block type of given string block.

    This function analyzes the provided block of text and identifies its
    markdown type by checking for specific patterns. It returns the corresponding
    BlockType enum value.

    Args:
        block (str): A string containing a markdown block

    Returns:
        BlockType: The identified type of the markdown block

    The function checks for block types in this order:
    1. Heading (starts with #)
    2. Code block (surrounded by ```)
    3. Quote (all lines start with >)
    4. Unordered list (all lines start with "- ")
    5. Ordered list (lines start with sequential numbers)
    6. Defaults to paragraph if no other type is matched

    Example:
        >>> block_to_block_type("# Header")
        BlockType.HEADING
        >>> block_to_block_type("Regular paragraph text")
        BlockType.PARAGRAPH
    """
    if block.startswith(ALLOWED_HEADINGS):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if check_all_strings_start_with(block.split("\n"), ">"):
        return BlockType.QUOTE

    if check_all_strings_start_with(block.split("\n"), "- "):
        return BlockType.UNORDERED_LIST

    if is_ordered_list(block.split("\n")):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def check_all_strings_start_with(string_list: list[str], char: str) -> bool:
    """
    Checks if all strings in a list start with a specific character.

    Args:
        string_list: A list of strings.
        char: The character to check.

    Returns:
        True if all strings start with the character, False otherwise.
    """
    return all(s.startswith(char) for s in string_list)


def is_ordered_list(ordered_list: list[str]) -> bool:
    """
    Checks if all strings start with a number followed by . and space
    Numbers must start from 1 and increment by 1 for each item in the list

    Args:
        ordered_list: A list of strings.

    Returns:
        bool: True if all strings start with number in sequential order followed by . and space starting from 1.
    """
    current_number = 1
    for item in ordered_list:
        if not item.startswith(f"{current_number}. "):
            return False
        current_number += 1
    return True


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode('div', children, None)


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return ordered_list_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html_node(block)


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split('\n')
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    pattern = r'```(?:\w*\n|\n)((?:.|\n)*?)```'
    match = re.search(pattern, block)
    code_text = match.group(1)
    raw_text_node = TextNode(code_text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def quote_to_html_node(block: str) -> ParentNode:
    clean_lines = []
    for line in block.split("\n"):
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        clean_lines.append(line.lstrip(">").strip())
    clean_quote = " ".join(clean_lines)
    children = text_to_children(clean_quote)
    return ParentNode("blockquote", children)


def ordered_list_to_html_node(block: str) -> ParentNode:
    pattern = r'^\s*\d+\.\s+(.*?)$'
    ol_items = []
    for item in block.split('\n'):
        match = re.match(pattern, item)
        text = match.group(1)
        children = text_to_children(text)
        ol_items.append(ParentNode("li", children))
    return ParentNode("ol", ol_items)


def unordered_list_to_html_node(block: str) -> ParentNode:
    list_items = []
    for item in block.split("\n"):
        text = item.lstrip("- ")
        children = text_to_children(text)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def get_quote_block_text(md_quote: str) -> str:
    quote_lines = []
    for quote_line in md_quote.split("\n"):
        quote_lines.append(quote_line.lstrip("> "))

    return " ".join(quote_lines)
