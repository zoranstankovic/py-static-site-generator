import unittest

from node_splitter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(extract_markdown_images(""), [])

    def test_no_images(self):
        self.assertEqual(extract_markdown_images("This is some text without images."), [])

    def test_single_image(self):
        text = "This is an image: ![alt text](http://example.com/image.jpg)"
        expected = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_multiple_images(self):
        text = "![alt1](url1) ![alt2](url2) ![alt3](url3)"
        expected = [("alt1", "url1"), ("alt2", "url2"), ("alt3", "url3")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_at_start(self):
        text = "![alt text](http://example.com) Some text."
        expected = [("alt text", "http://example.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_at_end(self):
        text = "Some text. ![alt text](http://example.com)"
        expected = [("alt text", "http://example.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_special_chars_in_url(self):
        text = "![alt text](http://example.com/image.jpg?param1=value1&param2=value2#fragment)"
        expected = [("alt text", "http://example.com/image.jpg?param1=value1&param2=value2#fragment")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_spaces_in_url(self):
        # URLs with spaces are technically invalid, but the regex SHOULD match them
        # because the requirements only specify matching the pattern.  A separate
        # function would be responsible for validating the URLs.
        text = "![alt text](http://example.com/image with spaces.jpg)"
        expected = [("alt text", "http://example.com/image with spaces.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_parentheses_in_alt_text(self):
        text = "![alt text (with parentheses)](http://example.com)"
        expected = [("alt text (with parentheses)", "http://example.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_no_alt_text_but_valid_syntax(self):
        # Test that the function handles empty alt text
        text = "![](http://example.com)"
        expected = [("", "http://example.com")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_no_url_but_valid_syntax(self):
        # Test that the function handles empty URL.
        text = "![alt_text]()"
        expected = [("alt_text", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_with_empty_alt_text_and_url(self):
        text = "![]()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_almost_image_missing_exclamation(self):
        text = "[alt text](http://example.com)"  # Missing the !
        self.assertEqual(extract_markdown_images(text), [])

    def test_almost_image_missing_brackets(self):
        text = "!alt text(http://example.com)"  # Missing the []
        self.assertEqual(extract_markdown_images(text), [])

    def test_almost_image_missing_parentheses(self):
        text = "![alt text]http://example.com"  # Missing the ()
        self.assertEqual(extract_markdown_images(text), [])

    def test_multiple_lines_with_images(self):
        text = """
            This is line 1.
    ![alt1](url1)
    This is line 2.
    ![alt2](url2)
    """
        expected = [("alt1", "url1"), ("alt2", "url2")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_inside_other_markdown(self):
        text = "This is **bold text with an ![image](url)**."
        expected = [("image", "url")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_url_with_escaped_characters(self):
        text = r"![alt text](http://example.com/image%20with%20spaces.jpg)"  # %20 is a space
        expected = [("alt text", "http://example.com/image%20with%20spaces.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_image_url_starting_with_special_character(self):
        text = "![alt](.image.png)"
        expected = [("alt", ".image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

        text = "![alt](?image.png)"
        expected = [("alt", "?image.png")]
        self.assertEqual(extract_markdown_images(text), expected)

        text = "![alt](!image.png)"
        expected = [("alt", "!image.png")]
        self.assertEqual(extract_markdown_images(text), expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(extract_markdown_links(""), [])

    def test_no_links(self):
        self.assertEqual(extract_markdown_links("This is some text without links."), [])

    def test_single_link(self):
        text = "This is a link: [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_links(self):
        text = "[link1](url1) [link2](url2) [link3](url3)"
        expected = [("link1", "url1"), ("link2", "url2"), ("link3", "url3")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_at_start(self):
        text = "[link text](http://example.com) Some text."
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_at_end(self):
        text = "Some text. [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_special_chars_in_url(self):
        text = "[link text](http://example.com/page.html?param1=value1&param2=value2#fragment)"
        expected = [("link text", "http://example.com/page.html?param1=value1&param2=value2#fragment")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_spaces_in_url(self):
        # URLs with spaces should be matched.  URL validation is a separate concern.
        text = "[link text](http://example.com/page with spaces.html)"
        expected = [("link text", "http://example.com/page with spaces.html")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_link_text(self):
        text = "[](http://example.com)"
        expected = [("", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_url(self):
        text = "[link text]()"
        expected = [("link text", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_with_empty_link_text_and_url(self):
        text = "[]()"
        expected = [("", "")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_almost_link_missing_brackets(self):
        text = "link text(http://example.com)"  # Missing the []
        self.assertEqual(extract_markdown_links(text), [])

    def test_almost_link_missing_parentheses(self):
        text = "[link text]http://example.com"  # Missing the ()
        self.assertEqual(extract_markdown_links(text), [])

    def test_image_is_excluded(self):
        text = "![alt text](http://example.com/image.jpg)"  # This is an image, not a link
        self.assertEqual(extract_markdown_links(text), [])

    def test_link_and_image_together(self):
        text = "[link text](http://example.com) and ![alt text](http://example.com/image.jpg)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_multiple_lines_with_links(self):
        text = """
    This is line 1.
    [link1](url1)
    This is line 2.
    [link2](url2)
    """
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_link_inside_other_markdown(self):
        text = "This is **bold text with a [link](url)**."
        expected = [("link", "url")]
        self.assertEqual(extract_markdown_links(text), expected)

    def test_no_space_between_links(self):
        text = "[link1](url1)[link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(extract_markdown_links(text), expected)