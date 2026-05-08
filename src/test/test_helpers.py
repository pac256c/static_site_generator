import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from helpers import *
from leafnode import *
from textnode import *
from parentnode import *
from htmlnode import *

class TestHelpers(unittest.TestCase):
    ###############################################################################################
    # text_node_to_html_node
    ###############################################################################################
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "https://www.google.com")

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props["src"], "https://www.google.com")
        self.assertEqual(html_node.props["alt"], "This is an image node")

    ###############################################################################################
    # split_nodes_delimiter
    ###############################################################################################
    def test_codebasic(self):
        inparr = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "`", TextType.CODE)
        self.assertEqual(resarr, exparr)

    def test_boldbasic(self):
        inparr = [
            TextNode("This is text with a **bold** word", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "**", TextType.BOLD)
        self.assertEqual(resarr, exparr)

    def test_italicbasic(self):
        inparr = [
            TextNode("This is text with a _italic_ word", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "_", TextType.ITALIC)
        self.assertEqual(resarr, exparr)

    def test_boldmulti(self):
        inparr = [
            TextNode("This is text with **multiple** **bold** words", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("multiple", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "**", TextType.BOLD)
        self.assertEqual(resarr, exparr)

    def test_boldnone(self):
        inparr = [
            TextNode("This is text with no bold words", TextType.TEXT)
        ]
        resarr = split_nodes_delimiter(inparr, "**", TextType.BOLD)
        self.assertEqual(resarr, inparr)

if __name__ == "__main__":
    unittest.main()