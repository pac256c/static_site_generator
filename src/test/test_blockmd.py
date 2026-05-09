import sys
import os
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

import unittest
from inlinemd import *
from blockmd import *
from leafnode import *
from textnode import *
from parentnode import *
from htmlnode import *

block_examples = [
"# Heading 1",
"## Heading 2",
"### Heading 3",
"#### Heading 4",
"##### Heading 5",
"###### Heading 6",
"This is a paragraph of text.",
"""- Item 1
- Item 2
- Item 3""",
"""- Item 1
* Item 2
- Item 3""",
"""1. Item 1
2. Item 2
3. Item 3""",
"""1. Item 1
4. Item 2
3. Item 3""",
"""> This is a quote.
> This is a quote.
> This is a quote.""",
"""> This is a quote.
< This is a corrupted quote.
> This is a quote.""",
"""```
This is code
```""",]

block_example_types = [
BlockType.HEADING,
BlockType.HEADING,
BlockType.HEADING,
BlockType.HEADING,
BlockType.HEADING,
BlockType.HEADING,
BlockType.PARAGRAPH,
BlockType.UNORDERED_LIST,
BlockType.PARAGRAPH,
BlockType.ORDERED_LIST,
BlockType.PARAGRAPH,
BlockType.QUOTE,
BlockType.PARAGRAPH,
BlockType.CODE
]

html_examples = [
"<h1>Heading 1</h1>",
"<h2>Heading 2</h2>",
"<h3>Heading 3</h3>",
"<h4>Heading 4</h4>",
"<h5>Heading 5</h5>",
"<h6>Heading 6</h6>",
"<p>This is a paragraph of text.</p>",
"<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>",
"<p>- Item 1 * Item 2 - Item 3</p>",
"<ol><li>Item 1</li><li>Item 2</li><li>Item 3</li></ol>",
"<p>1. Item 1 4. Item 2 3. Item 3</p>",
"<blockquote>This is a quote. This is a quote. This is a quote.</blockquote>",
"<p>> This is a quote. < This is a corrupted quote. > This is a quote.</p>",
"<pre><code>This is code\n</code></pre>"
]


heading = "# This is a heading"
paragraph = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."
unordered_list = """- This is the first list item in a list block
- This is a list item
- This is another list item"""
blocksplit = "\n\n"


class TestBlockMd(unittest.TestCase):
    ###############################################################################################
    # text_node_to_html_node
    ###############################################################################################
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_extrasplits(self):
        md = blocksplit + blocksplit + unordered_list + "\n   " + blocksplit + paragraph + blocksplit + heading
        exp = [unordered_list, paragraph, heading]
        self.assertEqual(markdown_to_blocks(md), exp)

    def test_markdown_none(self):
        md = blocksplit + blocksplit + blocksplit
        exp = []
        self.assertEqual(markdown_to_blocks(md), exp)

    def test_markdown_many(self):
        md = heading + blocksplit + paragraph + paragraph + blocksplit + "     \t" + unordered_list + blocksplit + unordered_list
        exp = [heading, paragraph+paragraph, unordered_list, unordered_list]
        self.assertEqual(markdown_to_blocks(md), exp)

    ###############################################################################################
    # block_to_block_type
    ###############################################################################################
    def test_block_to_block_type(self):
        for i in range(14):
            self.assertEqual(block_to_block_type(block_examples[i]),block_example_types[i])

    ###############################################################################################
    # markdown_to_html
    ###############################################################################################
    def test_markdown_to_html_blocks(self):
        for i in range(14):
            node = markdown_to_html_node(block_examples[i])
            html = node.to_html()
            self.assertEqual(html, "<div>" + html_examples[i] + "</div>")

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


    def test_quotefromsource(self):
        md = """> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>"I am in fact a Hobbit in all but size."  -- J.R.R. Tolkien</blockquote></div>'
        )

    

if __name__ == "__main__":
    unittest.main()