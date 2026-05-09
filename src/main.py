from textnode import *
import shutil
import os
from blockmd import *
from htmlnode import *
from inlinemd import *
from leafnode import *
from parentnode import *
from textnode import *

#source & dest are both os.path's
def copy_content_and_apply_func(func, remove_dest):
    def inner(source, dest):
        if remove_dest and os.path.exists(dest):
            shutil.rmtree(dest)
        if not os.path.exists(dest): os.mkdir(dest)
        for item in os.listdir(source):
            source_path = os.path.join(source,item)
            dest_path = os.path.join(dest,item)
            if os.path.isfile(source_path):
                func(source_path,dest_path)
            else:
                inner(source_path, dest_path)
    return inner

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        linesplit = line.strip().split(" ")
        if linesplit[0] == "#": return " ".join(linesplit[1:]).strip()
    raise Exception("No title found in input markdown")

def read_file_as_str(file_path):
    with open(file_path, "r") as file:
        content = file.read()
        return content
    raise Exception("Error reading file")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file_as_str(from_path)
    template = read_file_as_str(template_path)
    htmlnode = markdown_to_html_node(markdown)
    html = htmlnode.to_html()
    title = extract_title(markdown)
    fullhtml = template.replace("{{ Title }}", title)
    fullhtml = fullhtml.replace("{{ Content }}", html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.mkdir(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(fullhtml)

copy_content = copy_content_and_apply_func(lambda src, dest: shutil.copy(src,dest), True)
convert_content = copy_content_and_apply_func(lambda src, dest: generate_page(src, "template.html", dest[:-2]+"html"), False)

def main():
    copy_content("static", "public")
    convert_content("content", "public")

if __name__ == "__main__":
    main()