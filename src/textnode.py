from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text="", text_type=None, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        equiv  = self.text == other.text
        equiv &= self.text_type == other.text_type
        equiv &= self.url  == other.url
        return equiv

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
