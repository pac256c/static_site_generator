import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is NOT a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_texttype(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_neq_urlnone(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "yahoo.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()