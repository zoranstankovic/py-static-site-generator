from enum import Enum


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
    Determines the markdown block type of a given string block.

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

