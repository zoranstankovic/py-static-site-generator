import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_init_with_all_parameters(self):
        node = LeafNode("p", "Hello, World!", {"class": "greeting", "id": "hello"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, World!")
        self.assertEqual(node.props, {"class": "greeting", "id": "hello"})
        self.assertIsNone(node.children)

    def test_init_without_props(self):
        node = LeafNode("span", "Text")
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "Text")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_init_with_none_tag(self):
        node = LeafNode(None, "Just text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Just text")
        self.assertIsNone(node.props)
        self.assertIsNone(node.children)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")

    def test_leaf_to_html_with_none_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_with_empty_tag(self):
        node = LeafNode("", "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(repr(node), "LeafNode(p, Hello, world!, None)")