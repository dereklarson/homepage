import glob
import logging
import yaml
from collections import defaultdict
from jinja2 import Environment, FileSystemLoader


def md2yaml(text):
    """Converts the Gatsby markdown syntax to a yaml parseable string.
    It ends up being just a matter of converting the second --- of the frontmatter
    into the name of a key that describes the remaining content, and checking a bit
    the nature of the content (bullets or plaintext)
    """
    output = []
    frontmatter = 0
    mode = None
    for line in text.split("\n"):
        if line.startswith("---"):
            if not frontmatter:
                output.append(line)
            else:
                modetag = " |" if mode == "text" else ""
                output.append(f"content:{modetag}")
            frontmatter += 1
        elif "blocktype:" in line:
            mode = "bullets" if "bullets" in line else "text"
        elif frontmatter >= 2:
            if "<a" in line or "</a>" in line:
                # Skip hyperlinks
                continue
            elif line.startswith(" - "):
                output.append(line)
            else:
                output.append(f"    {line}")
        else:
            output.append(line)
    return "\n".join(output)


def load_markdowns_rec(path):
    output = defaultdict(list)
    for filename in glob.glob(f"{path}/**/*.md"):
        try:
            logging.warning(f"loading {filename}")
            with open(filename, "r") as fh:
                text = fh.read()
                yaml_str = md2yaml(text)
                if "Aleph" in filename:
                    print(yaml_str)
                loaded = yaml.load(yaml_str, Loader=yaml.Loader)
                output[loaded["type"]].append(loaded)
        except IOError as exc:
            logging.warning("Couldn't load {}".format(filename))
            logging.warning(exc)

    return output


def get_context():
    context = load_markdowns_rec("../content")
    context.update(
        {
            "name": "{Derek}{Larson}",
            "phone": "415-792-7219",
            "email": "larson.derek.a@gmail.com",
            "homepage": "dereklarson.info",
            "skills": ["Python", "MonteCarlo", "Stats",],
        }
    )
    return context


def write_template(template, context, output_location):
    env_args = {"trim_blocks": True, "lstrip_blocks": True}
    jenv = Environment(loader=FileSystemLoader("src"), **env_args)
    template = jenv.get_template(template)
    str_output = template.render(context)

    with open(output_location, "w") as fh:
        fh.write(str_output)

    print(f"  wrote {output_location}")


if __name__ == "__main__":
    context = get_context()
    write_template("template.tex.j2", context, "build/out_template.xtx")
