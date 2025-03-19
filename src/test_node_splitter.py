import unittest

from node_splitter import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(split_nodes_delimiter([], "**", TextType.BOLD), [])
        self.assertEqual(split_nodes_delimiter([], "_", TextType.ITALIC), [])
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])

    def test_single_text_node_no_delimiter(self):
        nodes = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), [TextNode("hello world", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), [TextNode("hello world", TextType.TEXT)])
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), [TextNode("hello world", TextType.TEXT)])

    def test_single_text_node_with_delimiter_bold(self):
        nodes = [TextNode("hello **world**", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected)

    def test_single_text_node_with_delimiter_italic(self):
        nodes = [TextNode("hello _world_", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.ITALIC)]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), expected)

    def test_single_text_node_with_delimiter_code(self):
        nodes = [TextNode("hello `world`", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.CODE)]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expected)

    def test_multiple_delimiters_same_type(self):
        nodes = [TextNode("hello **world** and **test**", TextType.TEXT)]
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("test", TextType.BOLD)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected)

    def test_multiple_delimiters_mixed_types(self):
        nodes = [TextNode("hello **world**", TextType.TEXT), TextNode("another", TextType.ITALIC)]
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("another", TextType.ITALIC)
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected)

    def test_multiple_text_nodes_with_delimiters(self):
        nodes = [TextNode("hello **world**", TextType.TEXT), TextNode("another _test_", TextType.TEXT)]
        expected_bold = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("another _test_", TextType.TEXT)
        ]
        expected_italic = [
            TextNode("hello **world**", TextType.TEXT),
            TextNode("another ", TextType.TEXT),
            TextNode("test", TextType.ITALIC)
        ]

        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected_bold)
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), expected_italic)

    def test_delimiter_at_start_and_end(self):
        nodes = [TextNode("**hello**", TextType.TEXT)]
        expected = [TextNode("hello", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expected)

        nodes = [TextNode("_hello_", TextType.TEXT)]
        expected = [TextNode("hello", TextType.ITALIC)]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), expected)

    def test_non_text_nodes_are_returned_unchanged(self):
        nodes = [TextNode("hello", TextType.ITALIC), TextNode("world", TextType.BOLD)]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), nodes)

    def test_space_inside_delimiter(self):
        nodes = [TextNode("hello _ world _", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode(" world ", TextType.ITALIC)]
        self.assertEqual(split_nodes_delimiter(nodes, "_", TextType.ITALIC), expected)

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)
