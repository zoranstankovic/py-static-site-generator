import unittest

from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node


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


class TestMarkdownToHtmlNode(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            html
        )

    def test_headings(self):
        md = """
# Heading with emphasis and `code`

## Level 2 with **stronger** emphasis

### Level 3 with `inline` code

#### Level 4 with a [simple link](/)

##### Level 5 with an image ![string](http://localhost:8000)

###### Level 6 with a _mix_ of **everything** `and more` [here](https://example.net)
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><h1>Heading with emphasis and <code>code</code></h1><h2>Level 2 with <b>stronger</b> emphasis</h2><h3>Level 3 with <code>inline</code> code</h3><h4>Level 4 with a <a href="/">simple link</a></h4><h5>Level 5 with an image <img src="http://localhost:8000" alt="string"></img></h5><h6>Level 6 with a <i>mix</i> of <b>everything</b> <code>and more</code> <a href="https://example.net">here</a></h6></div>'
        self.assertEqual(expected, html)

    def test_quote_markdown_text(self):
        md = """
> This is a simple, single-line blockquote.

> This is a blockquote that spans multiple lines.
> Notice that the `>` symbol only needs to be at the beginning of the first line of the paragraph,
> but it's common practice to include it at the beginning of each line for better readability.

> This is another multi-line blockquote.
> It demonstrates how you can continue a thought across several lines
> while still maintaining the quote formatting.

> This is a blockquote with **bold** text inside.

> This blockquote also contains _italicized_ text.

> Here's a blockquote with `inline code` within it.

> This blockquote has a [link](https://www.example.com) embedded.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><blockquote>This is a simple, single-line blockquote.</blockquote><blockquote>This is a blockquote that spans multiple lines. Notice that the <code>></code> symbol only needs to be at the beginning of the first line of the paragraph, but it\'s common practice to include it at the beginning of each line for better readability.</blockquote><blockquote>This is another multi-line blockquote. It demonstrates how you can continue a thought across several lines while still maintaining the quote formatting.</blockquote><blockquote>This is a blockquote with <b>bold</b> text inside.</blockquote><blockquote>This blockquote also contains <i>italicized</i> text.</blockquote><blockquote>Here\'s a blockquote with <code>inline code</code> within it.</blockquote><blockquote>This blockquote has a <a href="https://www.example.com">link</a> embedded.</blockquote></div>'
        self.assertEqual(expected, html)

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            html
        )

    def test_unordered_list(self):
        md = """
- This is a simple list item.
- Here is another item in the list.
- And yet one more list item.

- List item with **bold** text.
- List item with _italicized_ text.
- List item with `inline code`.
- List item with a [link](https://www.example.com).
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><ul><li>This is a simple list item.</li><li>Here is another item in the list.</li><li>And yet one more list item.</li></ul><ul><li>List item with <b>bold</b> text.</li><li>List item with <i>italicized</i> text.</li><li>List item with <code>inline code</code>.</li><li>List item with a <a href="https://www.example.com">link</a>.</li></ul></div>'
        self.assertEqual(expected, html)

    def test_ordered_list(self):
        md = """
1. First item in the ordered list.
2. Second item in the ordered list.
3. Third item in the ordered list.

1. Item with **bold** text.
2. Item with _italicized_ text.
3. Item with `inline code`.
4. Item with a [link](https://www.example.com).
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        expected = '<div><ol><li>First item in the ordered list.</li><li>Second item in the ordered list.</li><li>Third item in the ordered list.</li></ol><ol><li>Item with <b>bold</b> text.</li><li>Item with <i>italicized</i> text.</li><li>Item with <code>inline code</code>.</li><li>Item with a <a href="https://www.example.com">link</a>.</li></ol></div>'
        self.assertEqual(expected, html)


if __name__ == '__main__':
    unittest.main()
