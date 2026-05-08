
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Child classes must override")

    def props_to_html(self):
        if self.props is None: return ""
        return "".join( map(lambda k: f' {k}="{self.props[k]}"', self.props.keys()) )

    def repr_helper(self, indent):
        s = 3*indent*" " + "-" + f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        if self.children is None: return s
        for child in self.children:
            s += "\n" + child.repr_helper(indent + 1)
        return s

    def __repr__(self):
        return self.repr_helper(0)