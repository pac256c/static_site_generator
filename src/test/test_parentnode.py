import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from parentnode import *
from leafnode import *

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_tohtml_with_manyleaves(self):
        node = ParentNode("p", [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),  
        ])
        self.assertEqual(node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def tests_tohtml_with_spread(self):
        node = ParentNode("p", [
            ParentNode("span", [
                ParentNode("div", [
                    LeafNode(None, "one")
                ]),
                ParentNode("div", [
                    LeafNode(None, "two")
                ]),
            ]),
            ParentNode("span", [
                ParentNode("div", [
                    LeafNode(None, "three")
                ]),
                ParentNode("div", [
                    LeafNode(None, "four")
                ]),
            ]),
        ])
        self.assertEqual(node.to_html(),
            "<p><span><div>one</div><div>two</div></span><span><div>three</div><div>four</div></span></p>"
        )
        

if __name__ == "__main__":
    unittest.main()