from htmlnode import *
from leafnode import *
from parentnode import *
from textnode import *
from inlinemd import * 
import re
import functools
from enum import Enum

class BlockType(Enum):
    PARAGRAPH      = "paragraph"
    HEADING        = "heading"
    CODE           = "code"
    QUOTE          = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST   = "ordered_list"

def markdown_to_blocks(markdown):
    split_markdown = markdown.split("\n\n")
    split_markdown = map(str.strip, split_markdown)
    split_markdown = filter(lambda x: x!="", split_markdown)
    return list(split_markdown)

def is_blocktype(block, block_type):
    if len(block) == 0: raise Exception("Error: a markdown block must not be empty")
    lines = block.split("\n")
    andred = lambda x,y: x and y

    match block_type:
        case BlockType.HEADING:
            start = block.split(" ")
            if len(start) == 0: return False
            return block[0] == "#"*len(block[0])
        case BlockType.CODE:
            if len(block) < 7: return False
            return block[:4] == "```\n" and block[-3:] == "```"
        case BlockType.QUOTE:
            start = lambda line: len(line) > 0 and line[0] == ">"
            return functools.reduce(andred,map(start,lines),True)
        case BlockType.UNORDERED_LIST:
            start = lambda line: len(line) > 0 and line[0] == "-"
            return functools.reduce(andred,map(start,lines),True)
        case BlockType.ORDERED_LIST:
            start = lambda line: -1 if not line.split(".")[0].isdigit() else int(line.split(".")[0])
            return list(range(1,len(lines)+1)) == list(map(start,lines))
        case BlockType.PARAGRAPH: 
            return True
        case _: raise Exception("Error: unrecognized markdown block type")

def block_to_block_type(block):
    blocktype_check = [BlockType.HEADING, BlockType.CODE, BlockType.QUOTE, BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST, BlockType.PARAGRAPH]
    for blocktype in blocktype_check:
        if is_blocktype(block,blocktype): return blocktype

def inline_to_leaves(text):
    textnodes = text_to_textnodes(text)
    leafnodes = list(map(text_node_to_html_node, textnodes))
    return leafnodes

def block_to_html_node(block, block_type):
    lines = block.split("\n")

    match block_type:
        case BlockType.HEADING:
            i = block.find(" ")
            children = inline_to_leaves(block[i+1:])
            return ParentNode(f"h{i}",children)
        case BlockType.CODE:
            #note: keep everything unchanged inside of block, including newlines
            tmpblock = block[4:-3]
            children = [text_node_to_html_node(TextNode(tmpblock, TextType.TEXT))]
            parent = ParentNode("code",children)
            return ParentNode("pre", [parent])
        case BlockType.QUOTE:
            tmpblock = " ".join(map(lambda line: line.replace(">","").strip(), lines))
            children = inline_to_leaves(tmpblock)
            return ParentNode("blockquote", children)
        case BlockType.UNORDERED_LIST:
            tmpblock = map(lambda line: line[1:].strip(), lines)
            children = list(map(lambda line: ParentNode("li", inline_to_leaves(line)), tmpblock)) 
            return ParentNode("ul", children)
        case BlockType.ORDERED_LIST:
            parents = []
            for line in lines:
                linesplit = line.split(".")
                linesplit[1] = linesplit[1].lstrip()
                children = inline_to_leaves(".".join(linesplit[1:]))
                parents.append(ParentNode("li", children))
            return ParentNode("ol", parents)
        case BlockType.PARAGRAPH: 
            children = inline_to_leaves(" ".join(lines))
            return ParentNode("p", children)
        case _: raise Exception("Error: unrecognized markdown block type")

def markdown_to_html_node(markdown):
    block_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        #need to determine parents / children are inline markdown
        block_type = block_to_block_type(block)
        block_node = block_to_html_node(block,block_type)
        block_nodes.append(block_node)
    return ParentNode("div", block_nodes)