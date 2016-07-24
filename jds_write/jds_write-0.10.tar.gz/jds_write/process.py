import nbformat
import os
import time
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


def dict_to_code(mapping):
    """
    Function that maps a dictionary to code that can be inserted into a notebook cell
    :param mapping:
    :return:
    """
    lines = ("{} = {}".format(key, repr(value))
             for key, value in mapping.items())
    return '\n'.join(lines)


def process_nb(input_filename,
               inputpath,
               output_filename,
               outputpath,
               arg=dict(),
               timeout=600,
               insert_pos=1,
               kernel_name='python3',
               version=4
               ):
    """
    function to process a notebook (stored as a file)
    :param input_filename: name of the jupyter notebook (simple_plot.ipynb)
    :param inputpath: path of the notebook file
    :param output_filename: name of the jupyter notebook after processing (simple_plot_executed.ipynb)
    :param outputpath: output path of the notebook file
    :param arg: arguments to pass to the notebook for processing (as dictionary)
    :param timeout: number of seconds before timeout (default = 600)
    :param insert_pos: Position of the cell where the data need to be inserted (default = 1)
    :param kernel_name: (default = 'python3')
    :param version: (default=4)
    :return: output (structure with info regarding the calculations )

    """
    timestamp = "Executed:%s"
    duration = "Duration:%d seconds"
    start_time = time.time()
    output = dict()
    output['error'] = ''

    if not(os.path.exists(inputpath)):
        output['error'] = True
        output['error in cell'] = ''
        output['error type'] = 'input path of notebook file does not exist'
        return output

    if not(os.path.exists(outputpath)):
        output['error'] = True
        output['error in cell'] = ''
        output['error type'] = 'out path to store executed notebook file does not exist'
        return output

    nb_name = os.path.join(inputpath, input_filename)
    nb_name_output = os.path.join(outputpath, output_filename)

    if not(os.path.isfile(nb_name)):
        output['error'] = True
        output['error in cell'] = ''
        output['error type'] = 'notebook does not exist'
        return output

    ep = ExecutePreprocessor(timeout=timeout, kernel_name=kernel_name)
    ep.allow_errors = True

    nb = nbformat.read(nb_name, as_version=version)

    if len(arg) != 0:
        header = '# Cell inserted during automated execution.'
        footer = '# ----------------------------------------'
        code = dict_to_code(arg)
        code_cell = '\n'.join((header, code,footer))
        nb['cells'].insert(insert_pos, nbformat.v4.new_code_cell(code_cell))

    ep.preprocess(nb, {'metadata': {'path': './'}})

    control(nb, output)

    nbformat.write(nb, nb_name_output)

    output['timestamp'] = timestamp % (time.ctime(time.time()))
    output['duration'] = duration % (time.time() - start_time)
    return output


def control(nb, output):
    """
    Function to control the status of a given notebook
    :param nb: notebook name (.ipynb)
    :param output: Dict in which fields will be added
        .error : True or False
        .error in cell : nbr of the first cell where there was an error
    :return: None
    """

    cell_nr = 0
    output['error'] = False
    while cell_nr < len(nb.cells):
        if nb.cells[cell_nr].cell_type == 'code':
            if len(nb.cells[cell_nr].outputs) > 0:
                if nb.cells[cell_nr].outputs[0].output_type == 'error':

                    output['error'] = True
                    output['error in cell'] = cell_nr
                    output['error type'] = nb.cells[cell_nr].outputs[0]['ename']
                    return output
        cell_nr += 1

    return


def nb2html(input_filename,
            inputpath,
            html_filename,
            html_path,
            version=4
            ):
    """
    Converts jupyter notebook (as file) into html file the input and markdown cells are omitted
    :param input_filename: notebook file name ('Simple_plot.ipynb')
    :param inputpath: path ('./')
    :param html_filename: html filename ('Simple_Plot.html');
    :param html_path: ('./')
    :param version: (default =4)
    :return:
    """
    html_exporter = HTMLExporter()
    timestamp = "Executed:%s"
    duration = "Duration:%d seconds"
    start_time = time.time()
    output = dict()
    output['error'] = ''

    if not(os.path.exists(inputpath)):
        output['error'] = True
        output['error type'] = 'input path of notebook file does not exist'
        return output

    if not(os.path.exists(html_path)):
        output['error'] = True
        output['error type'] = 'html output path does not exist'
        return output

    nb_name = os.path.join(inputpath, input_filename)
    html_name = os.path.join(html_path, html_filename)

    if not(os.path.isfile(nb_name)):
        output['error'] = True
        output['error type'] = 'notebook does not exist'
        return output

    nb = nbformat.read(nb_name, as_version=version)

    html_exporter.template_file = 'nomarkdown_noinput.tpl'
    (body, resources) = html_exporter.from_notebook_node(nb)
    with open(html_name,"w",encoding="utf8") as f:
        f.write(body)

    return

