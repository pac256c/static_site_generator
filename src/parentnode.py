
from htmlnode import *

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None: raise ValueError("Parent node must have a tag!")
        if self.children is None: raise ValueError("Parent node must have children!")
        html_str = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str