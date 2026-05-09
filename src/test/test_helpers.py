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

extract_markdown_images = extract_linked_generic(TextType.IMAGE)
extract_markdown_links  = extract_linked_generic(TextType.LINK)
split_nodes_image = split_nodes_linked_generic(TextType.IMAGE)
split_nodes_link  = split_nodes_linked_generic(TextType.LINK)

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
    def test_split_nodes_delimiter_codebasic(self):
        inparr = [
            TextNode("This is text with a `code block` word", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "`", TextType.CODE)
        self.assertListEqual(resarr, exparr)

    def test_split_nodes_delimiter_boldbasic(self):
        inparr = [
            TextNode("This is text with a **bold** word", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "**", TextType.BOLD)
        self.assertListEqual(resarr, exparr)

    def test_split_nodes_delimiter_italicbasic(self):
        inparr = [
            TextNode("This is text with a _italic_ word", TextType.TEXT)
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "_", TextType.ITALIC)
        self.assertListEqual(resarr, exparr)

    def test_split_nodes_delimiter_boldmulti(self):
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
        self.assertListEqual(resarr, exparr)

    def test_split_nodes_delimiter_boldnone(self):
        inparr = [
            TextNode("This is text with no bold words", TextType.TEXT)
        ]
        resarr = split_nodes_delimiter(inparr, "**", TextType.BOLD)
        self.assertListEqual(resarr, inparr)

    def test_split_nodes_delimiter_manycomb(self):
        inparr = [
            TextNode("This is text with a `code block` word", TextType.TEXT),
            TextNode("This is text with a **bold** word", TextType.TEXT),
            TextNode("This is text with a _italic_ word", TextType.TEXT),
        ]
        exparr = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        resarr = split_nodes_delimiter(inparr, "**", TextType.BOLD)
        resarr = split_nodes_delimiter(resarr, "_", TextType.ITALIC)
        resarr = split_nodes_delimiter(resarr, "`", TextType.CODE)
        self.assertListEqual(resarr, exparr)


    ###############################################################################################
    # extract_markdown_images
    ###############################################################################################
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_onlylink(self):
        matches = extract_markdown_images(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

    ###############################################################################################
    # extract_markdown_images
    ###############################################################################################
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_onlyimg(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)

    ###############################################################################################
    # split_nodes_image
    ###############################################################################################
    def test_split_image_multiple(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_multiple_list(self):
        length = 5
        inptext = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        inplist = [TextNode(inptext,TextType.TEXT) for i in range(length)]
        exp_nodes = [None for i in range(4*length)]
        exp_nodes[0::4] = [TextNode("This is text with an ", TextType.TEXT)                                      for i in range(length)]
        exp_nodes[1::4] = [TextNode("image",                 TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")  for i in range(length)]
        exp_nodes[2::4] = [TextNode(" and another ",         TextType.TEXT)                                      for i in range(length)]
        exp_nodes[3::4] = [TextNode("second image",          TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")  for i in range(length)]
        new_nodes = split_nodes_image(inplist)
        self.assertListEqual(exp_nodes, new_nodes)

    def test_split_image_none(self):
        node = TextNode(
            "This is text with no image",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("This is text with no image", TextType.TEXT)])

    def test_split_image_linkonly(self):
        node = TextNode(
            "This is text with only a link [to boot dev](https://www.boot.dev) and thats it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("This is text with only a link [to boot dev](https://www.boot.dev) and thats it", TextType.TEXT)])

    def test_split_image_only(self):
        node = TextNode(
            "![image only](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("image only", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")])

    def test_split_image_firstandlast(self):
        node = TextNode(
            "![image1](https://i.imgur.com/zjjcJKZ.png)![image2](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("image2", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    ###############################################################################################
    # split_nodes_link
    ###############################################################################################
    def test_split_link_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_split_link_multiple_list(self):
        length = 5
        inptext = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        inplist = [TextNode(inptext,TextType.TEXT) for i in range(length)]
        exp_nodes = [None for i in range(4*length)]
        exp_nodes[0::4] = [TextNode("This is text with a link ", TextType.TEXT)                          for i in range(length)]
        exp_nodes[1::4] = [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")                for i in range(length)]
        exp_nodes[2::4] = [TextNode(" and ", TextType.TEXT)                                              for i in range(length)]
        exp_nodes[3::4] = [TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")  for i in range(length)]
        new_nodes = split_nodes_link(inplist)
        self.assertListEqual(exp_nodes, new_nodes)

    def test_split_link_none(self):
        node = TextNode(
            "This is text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("This is text with no link", TextType.TEXT)])

    def test_split_link_imageonly(self):
        node = TextNode(
            "This is text with only an image ![image only](https://i.imgur.com/zjjcJKZ.png) and thats it",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("This is text with only an image ![image only](https://i.imgur.com/zjjcJKZ.png) and thats it", TextType.TEXT)])

    def test_split_link_only(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")])

    def test_split_link_firstandlast(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    ###############################################################################################
    # text_to_textnodes
    ###############################################################################################
    def test_text_to_textnodes_main(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expt = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        rest = text_to_textnodes(text)
        self.assertListEqual(rest, expt)

if __name__ == "__main__":
    unittest.main()