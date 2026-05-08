import unittest

from leafnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_proplen2(self):
        node = LeafNode("a", "txt", props={"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">txt</a>')

    def test_proplen1(self):
        node = LeafNode("a", "txt", props={"href":"https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">txt</a>')

    def test_leaf_to_html_head(self):
        node = LeafNode("head", "Hello, world!")
        self.assertEqual(node.to_html(), "<head>Hello, world!</head>")
        

if __name__ == "__main__":
    unittest.main()