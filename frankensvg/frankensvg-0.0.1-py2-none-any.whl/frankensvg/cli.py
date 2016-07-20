import svgwrite
import yaml
import click


def read_config(filename):
    """ Read YAML config from `filename`. """
    with open(filename) as f:
        config = yaml.safe_load(f)
    return config or {}


def mergedicts(*a):
    """ Merge a list of dictionaries. """
    result = {}
    for d in a:
        result.update(d)
    return result


def pick(d, *fields):
    """ Pick keys from a dictionary if present.

    If a field starts with a '+' it is converted to a list if it isn't one
    already.
    """
    result = {}
    for f in fields:
        listify = f.startswith('+')
        if listify:
            f = f[1:]
        if f in d:
            value = d[f]
            if listify and not isinstance(value, (list, tuple)):
                value = [value]
            result[f] = value
    return result


def pop(d, *fields):
    """ Pop keys from a dictionary if present.

    If a field starts with a '+' it is converted to a list if it isn't one
    already.
    """
    result = pick(d, *fields)
    for f in result:
        d.pop(f)
    return result


def text(d, tmpl, context, **opts):
    """ Create a paragraph of text. """
    content = tmpl.format(**context)
    group_opts = pick(
        opts, 'font_family', 'font_size', 'font_weight', 'text_decoration')
    group = d.g(**group_opts)
    text_opts = pick(opts, '+x', '+y')
    text = group.add(d.text("", **text_opts))
    space_width = opts.get('space_width')
    line_height = opts.get('line_height')
    blank_line_height = opts.get('blank_line_height')
    blanks = 0
    for line in content.strip().splitlines():
        if not line.strip():
            blanks += 1
            continue
        indent = len(line) - len(line.lstrip(" "))
        text.add(d.tspan(
            "\n" + line + "\n",
            x=text_opts['x'], dx=["%d" % (indent * space_width,)],
            dy=["%g" % (line_height + blank_line_height * blanks,)]))
        blanks = 0
    return group


@click.command()
@click.option(
    "--config", "-c", default="input.yaml", help="YAML input file")
@click.option(
    "--output", "-o", default="output.svg", help="SVG output file")
def cli(config, output):
    """ Generate an simple SVG from a YAML description.
    """
    config = read_config(config)

    context = config['context']
    page = config['page']
    items = config['items']
    defaults = {'image': {}, 'text': {}}
    defaults.update(config.get('defaults', {}))

    size = (page['width'], page['height'])
    d = svgwrite.drawing.Drawing(size=size)

    for item in items:
        itype = item.pop('type')
        if itype == "image":
            opts = mergedicts(defaults['image'], item)
            image = opts.pop('image')
            fit = pop(opts, 'horiz', 'vert')
            img_elem = d.add(d.image(image, **opts))
            if fit:
                img_elem.fit(**fit)
        elif itype == "text":
            opts = mergedicts(defaults['text'], item)
            tmpl = opts.pop('text')
            d.add(text(d, tmpl, context, **opts))
        else:
            raise ValueError("Invalid item type %r" % (itype,))

    d.saveas(output)
