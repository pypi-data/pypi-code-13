""" Simple HTTP Server
    Se pot citi tabele .xls si .xlsx
    urmand sa fie afisate pe adresa: ip:PORT
    ex. http://10.0.10.20:8000/
"""

# pylint: disable=C0103

import SimpleHTTPServer
import SocketServer
from string import Template
import xlrd
import logging
import cgi
import unicodedata
import argparse
import os
import tempfile
import sys


class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })
        #for item in form.list:
            #logging.error(item)
        result = upload_table(form.list[0].file, form.list[0].filename)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        # self.send_header("Content-length", len(result) + 1)
        self.end_headers()
        self.wfile.write(result.encode('utf-8'))
        self.wfile.close()

        # SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)


def false_row(table_sheet):
    """ aflu indicele randurilor complet goale """
    false_row_index = []

    for row in range(table_sheet.nrows):
        nr_cols = 0
        for col in range(table_sheet.ncols):
            if table_sheet.cell(row, col).value == '' or table_sheet.cell(row, col).value == ' ':
                nr_cols += 1
            else:
                break
        if nr_cols == table_sheet.ncols:
            false_row_index.append(row)

    return false_row_index


def false_col(table_sheet):
    """ aflu indicele coloanelor complet goale """
    false_col_index = []

    for col in range(table_sheet.ncols):
        nr_rows = 0
        for row in range(table_sheet.nrows):
            if table_sheet.cell(row, col).value == '' or table_sheet.cell(row, col).value == ' ':
                nr_rows += 1
            else:
                break
        if nr_rows == table_sheet.nrows:
            false_col_index.append(col)

    return false_col_index


def render_html_header(table_sheet, cell_value, row, column, table_row_col_head):
    """ citire header """
    if table_sheet.cell(row, column).ctype == xlrd.XL_CELL_ERROR:
        # cell_value este aici errorCode
        default_error_text = xlrd.error_text_from_code[0x2a]  # same as "#N/A!"
        result = unicode(xlrd.error_text_from_code.get(cell_value,
                                                       default_error_text), "ascii")
        render_row_col = table_row_col_head.substitute(table_row_col_head=result)
    elif isinstance(cell_value, unicode) or cell_value == '':
        render_row_col = table_row_col_head.substitute(table_row_col_head=cell_value)
    else:
        render_row_col = table_row_col_head.substitute(table_row_col_head=
                                                       str("{:,}".format(int(cell_value))))

    return render_row_col


def render_html_body(table_sheet, cell_value, row, column, table_row_col):
    """ citire body table """
    if table_sheet.cell(row, column).ctype == xlrd.XL_CELL_ERROR:
        # cell_value este aici errorCode
        default_error_text = xlrd.error_text_from_code[0x2a]  # same as "#N/A!"
        result = unicode(xlrd.error_text_from_code.get(cell_value,
                                                       default_error_text), "ascii")
        render_row_col = table_row_col.substitute(table_row_col=result) + "\t"
    elif isinstance(cell_value, unicode) or cell_value == '':
        render_row_col = table_row_col.substitute(table_row_col=cell_value) + "\t"
    else:
        render_row_col = table_row_col.substitute(table_row_col=
                                                  str("{:,}".format(int(cell_value)))) + "\t"

    return render_row_col


def process_sheet(table_sheet, table_rows, table_row_col, table_row_col_head):
    """ afisarea unui sheet din tabel """
    false_row_index = false_row(table_sheet)
    false_col_index = false_col(table_sheet)


    # print table_sheet.merged_cells
    #
    # max_row_high = 0
    # for crange in table_sheet.merged_cells:
    #     rlo, rhi, clo, chi = crange
    #     if rlo == 0:
    #         max_row_high = rhi
    #
    # print max_row_high

    #nr_header = 0

    render_head = ""
    render_rows = ""
    for row in range(table_sheet.nrows):
        if row in false_row_index:
            continue
        row_cols = ""
        #nr_row = 0
        for column in range(table_sheet.ncols):
            cell_value = table_sheet.cell(row, column).value
            if cell_value != xlrd.empty_cell:
                if column in false_col_index:
                    continue
                if row == 0:
                    render_row_col = render_html_header(table_sheet, cell_value, row, column, table_row_col_head)
                    #nr_header += 1
                else:
                    render_row_col = render_html_body(table_sheet, cell_value, row, column, table_row_col)
                    #nr_row += 1
                if render_row_col != "":
                    row_cols += render_row_col
        if row == 0:
            render_head += table_rows.substitute(table_row_cols=row_cols)
        else:
            render_rows += table_rows.substitute(table_row_cols=row_cols) + "\t\t\t"
        #print str(nr_row) + " " + str(nr_header)
    return render_rows, render_head


def upload_table(file_input, filename):

    if filename == '':
        with open("templates/index_error.template", 'r') as index_error:
            index_err_message = Template(index_error.read())
            return index_err_message.substitute(error_message="Please enter a file!")

    if filename[len(filename)-4:] != ".xls" and filename[len(filename)-5:] != ".xlsx":
        with open("templates/index_error.template", 'r') as index_error:
            index_err_message = Template(index_error.read())
            return index_err_message.substitute(error_message="Wrong file extension!")


    if filename[len(filename)-4:] == ".xls":
        workbook = xlrd.open_workbook(file_contents=file_input.read(), encoding_override='cp1252', formatting_info=True)
    else:
        workbook = xlrd.open_workbook(file_contents=file_input.read(), encoding_override='cp1252')

    list_of_sheets_name = workbook.sheet_names()

    id_tabs_list = []
    for sheet_name in list_of_sheets_name:
        sheet_name = unicodedata.normalize('NFKD', sheet_name).encode('ASCII', 'ignore')
        sheet_name = sheet_name.lower()
        sheet_name = sheet_name.replace(' ', '-')
        id_tabs_list.append(sheet_name)

    with open("templates/index.template", 'r') as index_file:
        index = Template(index_file.read())
        with open("templates/table.template", 'r') as table_file:
            table = Template(table_file.read())
            with open("templates/table_rows.template", 'r') as table_rows_file:
                table_rows = Template(table_rows_file.read())
                with open("templates/table_row_col.template", 'r') as table_row_col:
                    table_row_col = Template(table_row_col.read())
                    with open("templates/table_row_col_head.template", 'r') as table_row_col_head:
                        table_row_col_head = Template(table_row_col_head.read())
                        with open("templates/tabs.template", 'r') as tabs:
                            tabs = Template(tabs.read())
                            num_sheet = 0
                            render_table = ""
                            render_tab = ""
                            active = " in active"
                            for sheet in workbook.sheets():
                                if num_sheet != 0:
                                    render_tab += tabs.substitute(tab=list_of_sheets_name[num_sheet],
                                                                  tab_id=id_tabs_list[num_sheet]) + "\t\t\t\t"
                                    active = ""
                                render_table_rows, render_table_head = process_sheet(sheet, table_rows,
                                                                                     table_row_col, table_row_col_head)
                                render_table += table.substitute(tab_id=id_tabs_list[num_sheet],
                                                                 active=active,
                                                                 table_head=render_table_head,
                                                                 table_rows=render_table_rows) + "\t\t\t\t"
                                num_sheet += 1
            #print render_table
            return index.substitute(tab_id=id_tabs_list[0],
                                    first_tab=list_of_sheets_name[0],
                                    tab=render_tab,
                                    table=render_table)


def main():

    parser = argparse.ArgumentParser(description='Server PORT.')
    parser.add_argument("-p", "--port", help='set PORT (default: 8000)', type=int)

    if parser.parse_args().port is not None:
        PORT = parser.parse_args().port
    else:
        PORT = 8000

    wdir = os.path.dirname(os.path.realpath(__file__))
    os.chdir(wdir)
    print '================'
    print wdir

    # work = tempfile.mkdtemp(prefix="xlserver")

    httpd = SocketServer.TCPServer(("", PORT), RequestHandler)

    print "serving at port", PORT
    httpd.serve_forever()


if __name__ == "__main__":
    main()
