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
