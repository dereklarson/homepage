import copy
import dateutil.parser
import glob
import os
import re
import yaml
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


def md2yaml(text):
    """Converts the Gatsby markdown syntax to a yaml parseable string.
    It ends up being just a matter of converting the second --- of the frontmatter
    into the name of a key that describes the remaining content, and checking a bit
    the nature of the content (bullets or plaintext)
    """
    # First convert hrefs to latex versions
    text = href_html2tex(text)
    # We'll place the frontmatter directly into our output variable
    output, markdown, mode = split_frontmatter(text)
    if mode == "text":
        replacement = "\\%"  # Can't include backslash in f-string
        output.extend([f"    {line.replace('%', replacement)}" for line in markdown])
        return "\n".join(output)
    elif mode != "bullets":
        print("Unsupported markdown processing mode")
        return output

    listbuffer = None
    for line in markdown:
        if line.startswith("- "):
            if listbuffer:
                output.append(listbuffer)
            listbuffer = line
            continue
        # Only go up to 2 levels for bullets
        elif listbuffer:
            if line.startswith("  - "):
                output.append(listbuffer.replace("- ", "- key: "))
                output.append("  subitems:")
            else:
                output.append(listbuffer)
            listbuffer = None
        # Fix special characters for LateX
        line = line.replace("%", "\\%").replace("$", "\$") 
        output.append(line)
    return "\n".join([line for line in output])


def href_html2tex(link):
    """Converts html links to Latex links"""
    link = link.replace("\n", "^%")
    matcher = r'<a href=[\'"]?([^\'" >]+)[\'"]?.*?>(<\w+>)*([^<>"]+).*?</a>'
    texfmt = r"\\href{\1}{\\textcolor{heading}{\\textbf{\3}}}"
    output = re.sub(matcher, texfmt, link)
    return output.replace("^%", "\n")


def split_frontmatter(text):
    """Separates the frontmatter (between '---') and determines the text mode"""
    frontmatter = []
    markdown = []
    curr = None
    mode = None
    for line in text.split("\n"):
        if line.startswith("---"):
            curr = frontmatter if not frontmatter else markdown
            continue
        elif "blocktype:" in line:
            mode = "bullets" if "bullets" in line else "text"
            continue
        if curr is not None:
            curr.append(line)
    # This leads into the markdown material, specifying block text with a pipe if needed
    modetag = " |" if mode == "text" else ""
    frontmatter.append(f"content:{modetag}")
    return frontmatter, markdown, mode


def load_markdowns_rec(path):
    print(f"Grabbing markdown content from {path}")
    output = defaultdict(list)
    for filename in glob.glob(f"{path}/**/*.md"):
        try:
            print(f"  loading {filename}")
            with open(filename, "r") as fh:
                yaml_str = md2yaml(fh.read())
                loaded = yaml.load(yaml_str, Loader=yaml.Loader)
                output[loaded["type"]].append(loaded)
        except IOError as exc:
            print("Couldn't load {}".format(filename))
            print(exc)

    return output


def post_process_context(context):
    output = copy.deepcopy(context)
    # Personal, Interests, Skills assume one entry
    output["contact"] = output["contact"][0]
    output["interests"] = output["interests"][0]
    output["skills"] = output["skills"][0]

    # Skills: add the stars
    for catlist in output["skills"]["categories"].values():
        for item in catlist:
            filled_stars = "\\bigstar" * int(item["rating"])
            item["rating"] = f"${filled_stars}$"

    # Reformat dates and sort for each case
    for content_type in ["education", "work", "projects"]:
        output[content_type] = sorted(
            output[content_type], key=lambda x: x["date"], reverse=True
        )
        for item in output[content_type]:
            item["date"] = dateutil.parser.parse(item["date"]).strftime("%B %Y")

    return output

    return proc_context


def write_template(template, context, output_location):
    env_args = {"trim_blocks": True, "lstrip_blocks": True}
    jenv = Environment(loader=FileSystemLoader("src"), **env_args)
    template = jenv.get_template(template)
    str_output = template.render(context)

    with open(output_location, "w") as fh:
        fh.write(str_output)

    print(f"  wrote {output_location}")


if __name__ == "__main__":
    # Modify these as needed
    markdown_path = "../content"
    template_file = "template.tex.j2"
    output = "build/template_output.xtx"
    cls_template_file = "resume.cls"

    # Loads all markdown files recursively from markdown_path
    context = load_markdowns_rec(markdown_path)
    proc_context = post_process_context(context)
    write_template(template_file, proc_context, output)
    write_template(cls_template_file, {"theme": "dark"}, "build/resume.cls")
    write_template(cls_template_file, {"theme": "light"}, "build/light_resume.cls")
