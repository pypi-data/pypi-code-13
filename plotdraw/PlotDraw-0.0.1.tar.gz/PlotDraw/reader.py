__author__ = 'Wenjie'
import xlrd


def xlsReader(filename):
    data = {}
    legends = {}
    xaxis = {}
    myBook = xlrd.open_workbook(filename)
    sheet_num = myBook.nsheets
    for i in range(sheet_num):
        sheet_xaxis = []
        sheet_data = []
        sheet_legends = []
        sheet = myBook.sheet_by_index(i)
        rows = sheet.nrows
        cols = sheet.ncols
        for j in range(1, rows):
            if isinstance(sheet.cell(j, 0).value, float):
                sheet_xaxis.append(int(sheet.cell(j, 0).value))
            else:
                sheet_xaxis.append(sheet.cell(j, 0).value)
        for j in range(1, cols):
            data_col = []
            for k in range(1, rows):
                if sheet.cell(k, j).value is "":
                    break
                data_col.append(sheet.cell(k, j).value)
            sheet_data.append(data_col)
            sheet_legends.append(sheet.cell(0, j).value)
        data[sheet.name] = sheet_data
        legends[sheet.name] = sheet_legends
        xaxis[sheet.name] = sheet_xaxis
    return data, legends, xaxis


def txtReader(filename):
    data = []
    first = True
    with open(filename, "r") as lines:
        for line in lines:
            seg = line[:-1].split()
            if first:
                column = len(seg)
                for i in range(column):
                    data.append([])
                first = False
            for i in range(column):
                if seg[i] is not "":
                    data[i].append(float(seg[i]))
    return data
