import unittest

from markdown_blocks import markdown_to_blocks

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


if __name__ == '__main__':
    unittest.main()