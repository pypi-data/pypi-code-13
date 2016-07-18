import os

_dir = os.path.abspath(os.path.dirname(__file__))


def template(handler, filename):
    """Render the contents of a single file."""
    with open(os.path.join(_dir, "templates", filename)) as f:
        contents = f.read()
    return contents


def all_templates(handler, directory):
    """Render the contents of all files found in a directory."""
    template_dir = os.path.join(_dir, "templates", directory)
    templates = os.listdir(template_dir)
    contents = ""
    for tmpl in templates:
        filename = os.path.join(template_dir, tmpl)
        if os.path.isfile(filename):
            contents += template(handler, filename)
    return contents
