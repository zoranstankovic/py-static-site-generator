import unittest

from node_splitter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, \
    split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual([], split_nodes_delimiter([], "**", TextType.BOLD))
        self.assertEqual([], split_nodes_delimiter([], "_", TextType.ITALIC))
        self.assertEqual([], split_nodes_delimiter([], "`", TextType.CODE), )

    def test_single_text_node_no_delimiter(self):
        nodes = [TextNode("hello world", TextType.TEXT)]
        self.assertEqual([TextNode("hello world", TextType.TEXT)], split_nodes_delimiter(nodes, "**", TextType.BOLD))
        self.assertEqual([TextNode("hello world", TextType.TEXT)], split_nodes_delimiter(nodes, "_", TextType.ITALIC))
        self.assertEqual([TextNode("hello world", TextType.TEXT)], split_nodes_delimiter(nodes, "`", TextType.CODE))

    def test_single_text_node_with_delimiter_bold(self):
        nodes = [TextNode("hello **world**", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.BOLD)]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "**", TextType.BOLD))

    def test_single_text_node_with_delimiter_italic(self):
        nodes = [TextNode("hello _world_", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.ITALIC)]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "_", TextType.ITALIC))

    def test_single_text_node_with_delimiter_code(self):
        nodes = [TextNode("hello `world`", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode("world", TextType.CODE)]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "`", TextType.CODE))

    def test_multiple_delimiters_same_type(self):
        nodes = [TextNode("hello **world** and **test**", TextType.TEXT)]
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("test", TextType.BOLD)
        ]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "**", TextType.BOLD))

    def test_multiple_delimiters_mixed_types(self):
        nodes = [TextNode("hello **world**", TextType.TEXT), TextNode("another", TextType.ITALIC)]
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("another", TextType.ITALIC)
        ]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "**", TextType.BOLD))

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

        self.assertEqual(expected_bold, split_nodes_delimiter(nodes, "**", TextType.BOLD))
        self.assertEqual(expected_italic, split_nodes_delimiter(nodes, "_", TextType.ITALIC))

    def test_delimiter_at_start_and_end(self):
        nodes = [TextNode("**hello**", TextType.TEXT)]
        expected = [TextNode("hello", TextType.BOLD)]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "**", TextType.BOLD))

        nodes = [TextNode("_hello_", TextType.TEXT)]
        expected = [TextNode("hello", TextType.ITALIC)]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "_", TextType.ITALIC))

    def test_non_text_nodes_are_returned_unchanged(self):
        nodes = [TextNode("hello", TextType.ITALIC), TextNode("world", TextType.BOLD)]
        self.assertEqual(nodes, split_nodes_delimiter(nodes, "**", TextType.BOLD))

    def test_space_inside_delimiter(self):
        nodes = [TextNode("hello _ world _", TextType.TEXT)]
        expected = [TextNode("hello ", TextType.TEXT), TextNode(" world ", TextType.ITALIC)]
        self.assertEqual(expected, split_nodes_delimiter(nodes, "_", TextType.ITALIC))

    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]

        self.assertEqual(expected, new_nodes)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual([], extract_markdown_images(""))

    def test_no_images(self):
        self.assertEqual([], extract_markdown_images("This is some text without images."))

    def test_single_image(self):
        text = "This is an image: ![alt text](http://example.com/image.jpg)"
        expected = [("alt text", "http://example.com/image.jpg")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_multiple_images(self):
        text = "![alt1](url1) ![alt2](url2) ![alt3](url3)"
        expected = [("alt1", "url1"), ("alt2", "url2"), ("alt3", "url3")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_at_start(self):
        text = "![alt text](http://example.com) Some text."
        expected = [("alt text", "http://example.com")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_at_end(self):
        text = "Some text. ![alt text](http://example.com)"
        expected = [("alt text", "http://example.com")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_with_special_chars_in_url(self):
        text = "![alt text](http://example.com/image.jpg?param1=value1&param2=value2#fragment)"
        expected = [("alt text", "http://example.com/image.jpg?param1=value1&param2=value2#fragment")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_with_spaces_in_url(self):
        # URLs with spaces are technically invalid, but the regex SHOULD match them
        # because the requirements only specify matching the pattern.  A separate
        # function would be responsible for validating the URLs.
        text = "![alt text](http://example.com/image with spaces.jpg)"
        expected = [("alt text", "http://example.com/image with spaces.jpg")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_with_parentheses_in_alt_text(self):
        text = "![alt text (with parentheses)](http://example.com)"
        expected = [("alt text (with parentheses)", "http://example.com")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_with_no_alt_text_but_valid_syntax(self):
        # Test that the function handles empty alt text
        text = "![](http://example.com)"
        expected = [("", "http://example.com")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_with_no_url_but_valid_syntax(self):
        # Test that the function handles empty URL.
        text = "![alt_text]()"
        expected = [("alt_text", "")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_with_empty_alt_text_and_url(self):
        text = "![]()"
        expected = [("", "")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_almost_image_missing_exclamation(self):
        text = "[alt text](http://example.com)"  # Missing the !
        self.assertEqual([], extract_markdown_images(text))

    def test_almost_image_missing_brackets(self):
        text = "!alt text(http://example.com)"  # Missing the []
        self.assertEqual([], extract_markdown_images(text))

    def test_almost_image_missing_parentheses(self):
        text = "![alt text]http://example.com"  # Missing the ()
        self.assertEqual([], extract_markdown_images(text))

    def test_multiple_lines_with_images(self):
        text = """
            This is line 1.
    ![alt1](url1)
    This is line 2.
    ![alt2](url2)
    """
        expected = [("alt1", "url1"), ("alt2", "url2")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_inside_other_markdown(self):
        text = "This is **bold text with an ![image](url)**."
        expected = [("image", "url")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_url_with_escaped_characters(self):
        text = r"![alt text](http://example.com/image%20with%20spaces.jpg)"  # %20 is a space
        expected = [("alt text", "http://example.com/image%20with%20spaces.jpg")]
        self.assertEqual(expected, extract_markdown_images(text))

    def test_image_url_starting_with_special_character(self):
        text = "![alt](.image.png)"
        expected = [("alt", ".image.png")]
        self.assertEqual(expected, extract_markdown_images(text))

        text = "![alt](?image.png)"
        expected = [("alt", "?image.png")]
        self.assertEqual(expected, extract_markdown_images(text))

        text = "![alt](!image.png)"
        expected = [("alt", "!image.png")]
        self.assertEqual(expected, extract_markdown_images(text))


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual([], extract_markdown_links(""))

    def test_no_links(self):
        self.assertEqual([], extract_markdown_links("This is some text without links."))

    def test_single_link(self):
        text = "This is a link: [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_multiple_links(self):
        text = "[link1](url1) [link2](url2) [link3](url3)"
        expected = [("link1", "url1"), ("link2", "url2"), ("link3", "url3")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_at_start(self):
        text = "[link text](http://example.com) Some text."
        expected = [("link text", "http://example.com")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_at_end(self):
        text = "Some text. [link text](http://example.com)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_with_special_chars_in_url(self):
        text = "[link text](http://example.com/page.html?param1=value1&param2=value2#fragment)"
        expected = [("link text", "http://example.com/page.html?param1=value1&param2=value2#fragment")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_with_spaces_in_url(self):
        # URLs with spaces should be matched.  URL validation is a separate concern.
        text = "[link text](http://example.com/page with spaces.html)"
        expected = [("link text", "http://example.com/page with spaces.html")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_with_empty_link_text(self):
        text = "[](http://example.com)"
        expected = [("", "http://example.com")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_with_empty_url(self):
        text = "[link text]()"
        expected = [("link text", "")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_with_empty_link_text_and_url(self):
        text = "[]()"
        expected = [("", "")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_almost_link_missing_brackets(self):
        text = "link text(http://example.com)"  # Missing the []
        self.assertEqual([], extract_markdown_links(text))

    def test_almost_link_missing_parentheses(self):
        text = "[link text]http://example.com"  # Missing the ()
        self.assertEqual([], extract_markdown_links(text))

    def test_image_is_excluded(self):
        text = "![alt text](http://example.com/image.jpg)"  # This is an image, not a link
        self.assertEqual([], extract_markdown_links(text))

    def test_link_and_image_together(self):
        text = "[link text](http://example.com) and ![alt text](http://example.com/image.jpg)"
        expected = [("link text", "http://example.com")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_multiple_lines_with_links(self):
        text = """
    This is line 1.
    [link1](url1)
    This is line 2.
    [link2](url2)
    """
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_link_inside_other_markdown(self):
        text = "This is **bold text with a [link](url)**."
        expected = [("link", "url")]
        self.assertEqual(expected, extract_markdown_links(text))

    def test_no_space_between_links(self):
        text = "[link1](url1)[link2](url2)"
        expected = [("link1", "url1"), ("link2", "url2")]
        self.assertEqual(expected, extract_markdown_links(text))


class TestSplitNodesImage(unittest.TestCase):

    def test_no_nodes(self):
        """Test with an empty list of nodes"""
        result = split_nodes_image([])
        self.assertEqual([], result)

    def test_non_text_nodes(self):
        """Test with nodes that are not of TEXT type"""
        nodes = [
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode("alt2", TextType.IMAGE, "url2")
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(nodes, result)

    def test_text_node_no_images(self):
        """Test with TEXT nodes that don't contain any images"""
        nodes = [
            TextNode("Just plain text", TextType.TEXT),
            TextNode("More text without images", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(nodes, result)

    def test_single_image(self):
        """Test with a TEXT node containing a single image"""
        nodes = [
            TextNode("Text with ![alt](url) in the middle", TextType.TEXT)
        ]
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" in the middle", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)

    def test_image_at_start(self):
        """Test with a TEXT node that has an image at the start"""
        nodes = [
            TextNode("![alt](url) at the start", TextType.TEXT)
        ]
        expected = [
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode(" at the start", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)

    def test_image_at_end(self):
        """Test with a TEXT node that has an image at the end"""
        nodes = [
            TextNode("Image at the end ![alt](url)", TextType.TEXT)
        ]
        expected = [
            TextNode("Image at the end ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url")
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)

    def test_multiple_images(self):
        """Test with a TEXT node conataining multiple images"""
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertListEqual(expected, result)

    def test_only_image(self):
        """Test with a TEXT node that contains only an image"""
        nodes = [
            TextNode("![alt](url)", TextType.TEXT)
        ]
        expected = [
            TextNode("alt", TextType.IMAGE, "url")
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)

    def test_mixed_node_types(self):
        """Test with a mix of TEXT and non-TEXT nodes"""
        nodes = [
            TextNode("Existing image", TextType.IMAGE, "existing-url"),
            TextNode("Text with ![alt](url)", TextType.TEXT),
            TextNode("Just text", TextType.TEXT)
        ]
        expected = [
            TextNode("Existing image", TextType.IMAGE, "existing-url"),
            TextNode("Text with ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "url"),
            TextNode("Just text", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)

    def test_consecutive_images(self):
        """Test with consecutive images without text between them"""
        nodes = [
            TextNode("![alt1](url1)![alt2](url2)", TextType.TEXT)
        ]
        expected = [
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode("alt2", TextType.IMAGE, "url2")
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)

    def test_complex_mixed_content(self):
        """Test with a complex mix of nodes and images"""
        nodes = [
            TextNode("Pre-existing", TextType.TEXT),
            TextNode("![alt0](url0) Text ![alt1](url1) more text ![alt2](url2)", TextType.TEXT),
            TextNode("No images here", TextType.TEXT),
            TextNode("Post image", TextType.IMAGE, "post-url")
        ]
        expected = [
            TextNode("Pre-existing", TextType.TEXT),
            TextNode("alt0", TextType.IMAGE, "url0"),
            TextNode(" Text ", TextType.TEXT),
            TextNode("alt1", TextType.IMAGE, "url1"),
            TextNode(" more text ", TextType.TEXT),
            TextNode("alt2", TextType.IMAGE, "url2"),
            TextNode("No images here", TextType.TEXT),
            TextNode("Post image", TextType.IMAGE, "post-url")
        ]
        result = split_nodes_image(nodes)
        self.assertEqual(expected, result)


class TestSplitNodesLink(unittest.TestCase):

    def test_empty_list(self):
        """Test with an empty list of nodes"""
        result = split_nodes_link([])
        self.assertEqual([], result)

    def test_non_text_nodes(self):
        """Test with nodes that are not of TEXT type"""
        nodes = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode("image", TextType.IMAGE, "img-url")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(nodes, result)

    def test_text_node_no_links(self):
        """Test with TEXT nodes that don't contain any links"""
        nodes = [
            TextNode("Just plain text", TextType.TEXT),
            TextNode("More text without links", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(nodes, result)

    def test_single_link(self):
        """Test with a TEXT node containing a single link"""
        nodes = [
            TextNode("Text with [link](https://example.com) in the middle", TextType.TEXT)
        ]
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" in the middle", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(expected, result)

    def test_link_at_start(self):
        """Test with a TEXT node that has a link at the start"""
        nodes = [
            TextNode("[link](https://example.com) at the start", TextType.TEXT)
        ]
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" at the start", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        """Test with a TEXT node that has a link at the end"""
        nodes = [
            TextNode("Link at the end [link](https://example.com)", TextType.TEXT)
        ]
        expected = [
            TextNode("Link at the end ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        """Test with a TEXT node containing multiple links"""
        nodes = [
            TextNode("Start [link1](url1) middle [link2](url2) end", TextType.TEXT)
        ]
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_only_link(self):
        """Test with a TEXT node that contains only a link"""
        nodes = [
            TextNode("[link](url)", TextType.TEXT)
        ]
        expected = [
            TextNode("link", TextType.LINK, "url")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_mixed_node_types(self):
        """Test with a mix of TEXT and non-TEXT nodes"""
        nodes = [
            TextNode("Existing link", TextType.LINK, "existing-url"),
            TextNode("Text with [link](url)", TextType.TEXT),
            TextNode("Just text", TextType.TEXT)
        ]
        expected = [
            TextNode("Existing link", TextType.LINK, "existing-url"),
            TextNode("Text with ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
            TextNode("Just text", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_consecutive_links(self):
        """Test with consecutive links without text between them"""
        nodes = [
            TextNode("[link1](url1)[link2](url2)", TextType.TEXT)
        ]
        expected = [
            TextNode("link1", TextType.LINK, "url1"),
            TextNode("link2", TextType.LINK, "url2")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_links_with_special_characters(self):
        """Test links containing special characters in both text and URL"""
        nodes = [
            TextNode("Here's a [complex! link?](https://example.com/path?query=value&more=stuff)", TextType.TEXT)
        ]
        expected = [
            TextNode("Here's a ", TextType.TEXT),
            TextNode("complex! link?", TextType.LINK, "https://example.com/path?query=value&more=stuff")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_complex_mixed_content(self):
        """Test with a complex mix of nodes and links"""
        nodes = [
            TextNode("Pre-existing", TextType.TEXT),
            TextNode("[link0](url0) Text [link1](url1) more text [link2](url2)", TextType.TEXT),
            TextNode("No links here", TextType.TEXT),
            TextNode("Post link", TextType.LINK, "post-url")
        ]
        expected = [
            TextNode("Pre-existing", TextType.TEXT),
            TextNode("link0", TextType.LINK, "url0"),
            TextNode(" Text ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" more text ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode("No links here", TextType.TEXT),
            TextNode("Post link", TextType.LINK, "post-url")
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_empty_link_text(self):
        """Test with empty link text"""
        nodes = [
            TextNode("This has an [](url) empty link text", TextType.TEXT)
        ]
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("", TextType.LINK, "url"),
            TextNode(" empty link text", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)

    def test_empty_link_url(self):
        """Test with empty link URL"""
        nodes = [
            TextNode("This has an [text]() empty link URL", TextType.TEXT)
        ]
        expected = [
            TextNode("This has an ", TextType.TEXT),
            TextNode("text", TextType.LINK, ""),
            TextNode(" empty link URL", TextType.TEXT)
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(result, expected)


class TestTextToTextnodes(unittest.TestCase):

    def test_invalid_markdown(self):
        """Test with invalid Markdown syntax (unclosed formatting)"""
        with self.assertRaises(ValueError) as context:
            text_to_textnodes("This has **unclosed bold formatting.")

        self.assertTrue("invalid markdown syntax: unclosed inline element" in str(context.exception))

    def test_with_multiple_markdown_elements(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]

        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()