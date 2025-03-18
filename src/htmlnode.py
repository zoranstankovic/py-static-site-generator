class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list[object] = None,
                 props: dict[str, str] = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        html_props = ""
        if self.props is None:
            return ""
        for key, value in self.props.items():
            html_props += f" {key}=\"{value}\""
        return html_props

    def __repr__(self):
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={self.children}, props={self.props})"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None or self.tag == "":
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("invalid HTML: no children")

        parent_node = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            parent_node += child.to_html()

        parent_node += f"</{self.tag}>"
        return parent_node

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"
