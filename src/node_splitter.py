from src.textnode import TextNode
from textnode import TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("invalid markdown syntax: unclosed inline element")

        for i in range(len(split_text)):
            if not split_text[i]:
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(split_text[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(split_text[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes
