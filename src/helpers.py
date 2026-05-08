from htmlnode import *
from leafnode import *
from parentnode import *
from textnode import *


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT: return LeafNode(None, text_node.text)
        case TextType.BOLD: return LeafNode("b", text_node.text)
        case TextType.ITALIC: return LeafNode("i", text_node.text)
        case TextType.CODE: return LeafNode("code", text_node.text)
        case TextType.LINK: return LeafNode("a", text_node.text, props={"href":text_node.url})
        case TextType.IMAGE: return LeafNode("img", None, props={"src":text_node.url, "alt":text_node.text})
        case _: raise Exception("Error in text_node_to_html_node - type not found")
        

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            txt_arr = node.text.split(delimiter)
            if len(txt_arr) % 2 != 1:
                raise Exception(f"Error: unmatched delimiter {delimiter} in text '{node.text}'")
            for i in range(len(txt_arr)):
                if txt_arr[i] != "":
                    if i % 2 == 0: new_nodes.append(TextNode(txt_arr[i],TextType.TEXT))
                    else:          new_nodes.append(TextNode(txt_arr[i],text_type))
    return new_nodes