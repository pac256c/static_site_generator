import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_proplen2(self):
        node = HTMLNode(tag="a", value="txt", children=None, props={"href":"https://www.google.com", "target":"_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_proplen1(self):
        node = HTMLNode(tag="a", value="txt", children=None, props={"href":"https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_proplen0(self):
        node = HTMLNode(tag="a", value="txt", children=None, props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_printchildren(self):
        nodec = HTMLNode(tag="c", value="txt_c", children=None, props={"href":"gCgle.com"})
        nodeb = HTMLNode(tag="b", value="txt_b", children=[nodec], props={"href":"gBgle.com"})
        nodea = HTMLNode(tag="a", value="txt_a", children=[nodeb, nodec], props={"href":"gAgle.com"})
        repr = """-<a href="gAgle.com">txt_a</a>\n   -<b href="gBgle.com">txt_b</b>\n      -<c href="gCgle.com">txt_c</c>\n   -<c href="gCgle.com">txt_c</c>"""
        self.assertEqual(nodea.__repr__(), repr)
        

if __name__ == "__main__":
    unittest.main()