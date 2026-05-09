from htmlnode import *
from leafnode import *
from parentnode import *
from textnode import *
import re
import functools

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


def extract_linked_generic(text_type):      
    pattern = ""
    match text_type:
        case TextType.IMAGE:  pattern = r"!\[(.*?)\]\((.*?)\)"
        case TextType.LINK: pattern = r"(?<!!)\[(.*?)\]\((.*?)\)"
        case _: raise Exception("Error: invalid text_type in extract_linked_generic")

    def inner(text):
        return re.findall(pattern,text)
    return inner


def format_linked_generic(text_type):
    format_func = lambda : None
    match text_type:
        case TextType.IMAGE: format_func = lambda txt,url: f"![{txt}]({url})"
        case TextType.LINK: format_func = lambda txt,url: f"[{txt}]({url})"
        case _: raise Exception("Error: invalid text_type in format_links_generic")
    return format_func


def split_nodes_linked_generic(text_type):
    extract_func = extract_linked_generic(text_type)
    format_func = format_linked_generic(text_type)

    def inner(old_nodes):
        new_nodes = []
        for node in old_nodes:
            if node.text_type != TextType.TEXT:
                new_nodes.append(node)
            else:
                node_txt = node.text
                extract_objs = extract_func(node_txt)
                for (txt,url) in extract_objs:
                    obj_text = format_func(txt,url)
                    j = node_txt.find(obj_text)
                    if j == -1: raise Exception(f"Error scanning string for img/link in {node.text}")
                    if len(obj_text) == 0: raise Exception(f"Error scanning string for img/link in {node.text} - text cannot be empty")
                    if node_txt[:j] != "": new_nodes.append(TextNode(node_txt[:j],TextType.TEXT))
                    new_nodes.append(TextNode(txt,text_type,url))
                    node_txt = node_txt[j+len(obj_text):]
                if node_txt != "": new_nodes.append(TextNode(node_txt,TextType.TEXT))
        return new_nodes
    return inner

#form text_to_textnodes as composition of all conversion functions
split_nodes_arr = [
    lambda old_nodes: split_nodes_delimiter(old_nodes, "**", TextType.BOLD),
    lambda old_nodes: split_nodes_delimiter(old_nodes, "_", TextType.ITALIC),
    lambda old_nodes: split_nodes_delimiter(old_nodes, "`", TextType.CODE),
    split_nodes_linked_generic(TextType.IMAGE),
    split_nodes_linked_generic(TextType.LINK),
]
split_nodes_comb = functools.reduce(lambda f,g: lambda x: f(g(x)), split_nodes_arr)
text_to_textnodes = lambda text: split_nodes_comb([TextNode(text,TextType.TEXT)])

