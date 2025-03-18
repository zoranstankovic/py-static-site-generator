import unittest

from htmlnode import HTMLNode


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
