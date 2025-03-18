import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_values(self):
        div_node = HTMLNode("div", "This is a div node")
        self.assertEqual(div_node.tag, "div")
        self.assertEqual(div_node.value, "This is a div node")
        self.assertEqual(div_node.children, None)
        self.assertEqual(div_node.props, None)

    def test_text_repr(self):
        html_node = HTMLNode("p", "Text inside a paragraph", props={"class": "bold"})
        expected_repr = "HTMLNode(tag=p, value=Text inside a paragraph, children=None, props={'class': 'bold'})"
        self.assertEqual(repr(html_node), expected_repr)

    def test_prop_to_html(self):
        html_node = HTMLNode("a", "Link", props={"href": "https://www.google.com", "target": "_blank"})
        expected_props_to_html = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(html_node.props_to_html(), expected_props_to_html)

    def test_text_repr_has_children(self):
        li_node_1 = HTMLNode("li", "List 1")
        li_node_2 = HTMLNode("li", "List 2")
        li_node_3 = HTMLNode("li", "List 3")
        ul_node = HTMLNode("ul", None, [li_node_1, li_node_2, li_node_3])
        expected_repr = (
            "HTMLNode(tag=ul, value=None, children=[HTMLNode(tag=li, value=List 1, children=None, "
            "props=None), HTMLNode(tag=li, value=List 2, children=None, props=None), HTMLNode(tag=li, "
            "value=List 3, children=None, props=None)], props=None)")
        self.assertEqual(repr(ul_node), expected_repr)


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


class TestParentNode(unittest.TestCase):
    def test_init_with_all_parameters(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})

        self.assertEqual(parent_node.tag, "div")
        self.assertIsNone(parent_node.value)
        self.assertEqual(parent_node.children, [child_node])
        self.assertEqual(parent_node.props, {"class": "container", "id": "main"})

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(repr(parent_node), "ParentNode(div, [LeafNode(span, child, None)], None)")

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )


if __name__ == '__main__':
    unittest.main()