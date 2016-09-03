# coding: utf-8
# pylint: disable=invalid-name, too-many-locals, fixme
# pylint: disable=too-many-branches, too-many-statements
# pylint: disable=dangerous-default-value
"""k5viz.

Usage:
  k5viz.py <filename> [--output=<filename>] [--format=<ext>] [--no-show]
  k5viz.py (-h | --help)
  k5viz.py --version

Options:
  -h --help            Show this screen.
  --version            Show version.
  --format=<ext>       Format to output [default: pdf].
  --output=<filename>  Output filename [default: network].
  --no-show            Disable showing the network

"""
import sys, os, platform, json, re, copy

try:
    from graphviz import Digraph
except:
    raise ImportError("k5viz requires graphviz library")

try:
    from docopt import docopt
except:
    raise ImportError("k5viz requires docopt library")

try:
    import h5py
except:
    raise ImportError("k5viz requires h5py library")

try:
    import numpy as np
except:
    raise ImportError("k5viz requires numpy library")

def _str2tuple(string):
    """convert shape string to list, internal use only

    Parameters
    ----------
    string: str
        shape string

    Returns
    -------
    list of str to represent shape
    """
    return re.findall(r"\d+", string)


def plot_network(symbol, title="plot", shape=None, node_attrs={}):
    """convert symbol to dot object for visualization

    Parameters
    ----------
    title: str
        title of the dot graph
    symbol: Symbol
        symbol to be visualized
    shape: dict
        dict of shapes, str->shape (tuple), given input shapes
    node_attrs: dict
        dict of node's attributes
        for example:
            node_attrs={"shape":"oval","fixedsize":"fasle"}
            means to plot the network in "oval"
    Returns
    ------
    dot: Diagraph
        dot object of symbol
    """
    draw_shape = False
    conf = json.loads(symbol)
    nodes = conf["nodes"]
    heads = set(conf["heads"][0])  # TODO(xxx): check careful
    # default attributes of node
    node_attr = {"shape": "box", "fixedsize": "true",
                 "width": "1.3", "height": "0.8034", "style": "filled"}
    # merge the dict provided by user and the default one
    node_attr.update(node_attrs)
    dot = Digraph(name=title)
    # color map
    cm = ("#8dd3c7", "#fb8072", "#ffffb3", "#bebada", "#80b1d3",
          "#fdb462", "#b3de69", "#fccde5")

    # make nodes
    for i in range(len(nodes)):
        node = nodes[i]
        op = node["op"]
        name = node["name"]
        # input data
        attr = copy.deepcopy(node_attr)
        label = op

        if op == "null":
            if i in heads:
                label = node["name"]
                attr["fillcolor"] = cm[0]
            else:
                continue
        elif op == "Convolution":
            label = r"Convolution\n%sx%s/%s, %s" % (_str2tuple(node["param"]["kernel"])[0],
                                                    _str2tuple(node["param"]["kernel"])[1],
                                                    _str2tuple(node["param"]["stride"])[0],
                                                    node["param"]["num_filter"])
            attr["fillcolor"] = cm[1]
        elif op == "FullyConnected":
            label = r"FullyConnected\n%s" % node["param"]["num_hidden"]
            attr["fillcolor"] = cm[1]
        elif op == "BatchNorm":
            attr["fillcolor"] = cm[3]
        elif op == "Activation" or op == "LeakyReLU":
            label = r"%s\n%s" % (op, node["param"]["act_type"])
            attr["fillcolor"] = cm[2]
        elif op == "Pooling":
            label = r"Pooling\n%s, %sx%s/%s" % (node["param"]["pool_type"],
                                                _str2tuple(node["param"]["kernel"])[0],
                                                _str2tuple(node["param"]["kernel"])[1],
                                                _str2tuple(node["param"]["stride"])[0])
            attr["fillcolor"] = cm[4]
        elif op == "Concat" or op == "Flatten" or op == "Reshape":
            attr["fillcolor"] = cm[5]
        elif op == "Softmax":
            attr["fillcolor"] = cm[6]
        else:
            attr["fillcolor"] = cm[7]

        dot.node(name=name, label=label, **attr)

    # add edges
    for i in range(len(nodes)):
        node = nodes[i]
        op = node["op"]
        name = node["name"]
        if op == "null":
            continue
        else:
            inputs = node["inputs"]
            for item in inputs:
                input_node = nodes[item[0]]
                input_name = input_node["name"]
                if input_node["op"] != "null" or item[0] in heads:
                    attr = {"dir": "back", 'arrowtail':'open'}
                    # add shapes
                    if draw_shape:
                        if input_node["op"] != "null":
                            key = input_name + "_output"
                            shape = shape_dict[key][1:]
                            label = "x".join([str(x) for x in shape])
                            attr["label"] = label
                        else:
                            key = input_name
                            shape = shape_dict[key][1:]
                            label = "x".join([str(x) for x in shape])
                            attr["label"] = label
                    dot.edge(tail_name=name, head_name=input_name, **attr)

    return dot

def main():
    # Arguments
    arguments = docopt(__doc__, version='k5viz 1.0')

    # Read file
    input_filename = arguments['<filename>']
    symbol = None
    if input_filename[-3:] == '.k5':
        # Read from within hdf5/k5
        hf = h5py.File(input_filename, 'r')
        symbol = np.array(hf.get('network')).tostring()
    else:
        symbol = open(input_filename).read()

    # Render
    fileformat = arguments['--format']
    output_filename = arguments['--output']
    show = arguments['--no-show'] == False
    viz = plot_network(symbol, title=input_filename, node_attrs={"shape":'rect',"fixedsize":'false'})
    viz.format = fileformat
    viz.render(output_filename, view=show)

if __name__ == "__main__":
    main()
