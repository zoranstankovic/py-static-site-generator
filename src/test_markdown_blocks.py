import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


class TestMarkdownToBlocks(unittest.TestCase):

    def test_empty_string(self):
        md = ""
        result = markdown_to_blocks(md)
        expected = []
        self.assertEqual(expected, result)

    def test_single_paragraph(self):
        md = "This is a single paragraph."
        result = markdown_to_blocks(md)
        expected = ["This is a single paragraph."]
        self.assertEqual(expected, result)

    def test_multiple_empty_lines(self):
        md = """


First paragraph


Second paragraph


        """
        result = markdown_to_blocks(md)
        expected = ["First paragraph", "Second paragraph"]
        self.assertEqual(expected, result)

    def test_with_multiple_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        result = markdown_to_blocks(md)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
        self.assertEqual(expected, result)


class TestBlockToBlockType(unittest.TestCase):

    def test_heading(self):
        heading_one = "# This is heading one"
        heading_two = "## This is heading two"
        heading_three = "### This is heading three"
        heading_four = "#### This is heading four"
        heading_five = "##### This is heading five"
        heading_six = "###### This is heading six"

        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_one))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_two))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_three))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_four))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_five))
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_six))

    def test_invalid_heading_returns_paragraph(self):
        """Test invalid heading returns paragraph"""
        heading_seven = "####### This is heading seven"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(heading_seven))

    def test_code_block(self):
        code_block = "```python\nThis is code block in Python\n```"

        self.assertEqual(BlockType.CODE, block_to_block_type(code_block))

    def test_invalid_code_block(self):
        """Test invalid code block returns paragraph"""
        invalid_code_block = "``python\nThis is code block in Python\n```"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(invalid_code_block))

    def test_quote_block(self):
        quote_block = "> This is a blockquote\n> that continues here\n> and here"

        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block))

    def test_invalid_quote_block(self):
        """Test invalid quote block returns paragraph"""
        invalid_quote_block = "> This is a blockquote\n that continues here\n> and here"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(invalid_quote_block))

    def test_unordered_list(self):
        unordered_list = "- this is one list item\n- this is another list item"

        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered_list))

    def test_invalid_unordered_list(self):
        """Test invalid unordered list block returns paragraph"""
        unordered_list = "-this is one list item\n- this is another list item"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(unordered_list))

        unordered_list = "- this is one list item\nthis is another list item"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(unordered_list))

    def test_ordered_list(self):
        ordered_list = "1. one\n2. two\n3. three"

        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(ordered_list))

    def test_invalid_ordered_list(self):
        """Test invalid ordered list block returns paragraph"""
        ordered_list = "1. one\n3. three\n3. three"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(ordered_list))

        ordered_list = "1. one\nthree\n3. three"

        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(ordered_list))


if __name__ == '__main__':
    unittest.main()
