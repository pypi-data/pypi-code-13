import os
import glob
# import json
import re
import hashlib
from datapacker.excel2class import Excel2Class
import xlrd  # must install xlrd!

class Excel2Data(object):
    """
    将Excel数据导出为JSON格式的文本
    """
    # define types
    TYPE_INT32 = 'int32'
    TYPE_INT64 = 'int64'
    TYPE_FLOAT = 'float'
    TYPE_DOUBLE = 'double'
    TYPE_Bool = 'bool'
    TYPE_STRING = 'string'

    def __init__(self, input_path='./', output_path='dist/'):
        """
        :param filename: output filename
        :param input_path: relative path
        :param output_path: relative path, default 'dist'
        """
        self.input_path = input_path
        self.output_path = output_path
        self.excel_sheets = []
        self.class_files = []
        self.suffix = '.bin'  # 导出的文件后缀
        self.password = ''

    def make_json(self, filename):
        """
        export json format file from excel sheet
        https://www.json.com/
        http://json.org/

        Example Object

        var myObject = {
         "first": "John",
         "last": "Doe",
         "age": 39,
         "sex": "M",
         "salary": 70000,
         "registered": true
        };
        Example Array

        var myArray = [
          { "name": "John Doe", "age": 29 },
          { "name": "Anna Smith", "age": 24 },
          { "name": "Peter Jones", "age": 39 }
        ];
        Why JSON?

        The JSON standard is language-independent and its data structures, arrays and objects, are universally recognized. These structures are supported in some way by nearly all modern programming languages and are familiar to nearly all programmers. These qualities make it an ideal format for data interchange on the web.

        JSON vs XML

        The XML specification does not match the data model for most programming languages which makes it slow and tedious for programmers to parse. Compared to JSON, XML has a low data-to-markup ratio which results in it being more difficult for humans to read and write.

        Data Types

        Number{ "myNum": 123.456 }
        A series of numbers; decimals ok; double-precision floating-point format.

        String{ "myString": "abcdef" }
        A series of characters (letters, numbers, or symbols); double-quoted UTF-8 with backslash escaping.

        Boolean{ "myBool": true }
        True or false.

        Array{ "myArray": [ "a", "b", "c", "d" ] }
        Sequence of comma-separated values (any data type); enclosed in square brackets.

        Object{ "myObject": { "id": 7 } };
        Unordered collection of comma-separated key/value pairs; enclosed in curly braces; properties (keys) are distinct strings.

        Null{ "myNull": null }
        Variable with null (empty) value.

        Unsupported Data Types

        Undefinedvar myUndefined;
        Variable with no value assigned.

        Datevar myDate = new Date();
        Object used to work with dates and times.

        Errorvar myError = new Error();
        Object containing information about errors.

        Regular Expressionvar myRegEx = /json/i;
        Variable containing a sequence of characters that form a search pattern.

        Functionvar myFunction = function(){};
        Variable containing a block of code designed to perform a particular task.

        Examples

        Mixed Data Types

        var myObject = {
         "myNumber": 123.456,
         "myString": "abcdef",
         "myBool": true,
         "myArray": [ "a", "b", "c", "d" ],
         "myObject": { "id": 7 },
         "myNull": null
        };

        :return: None
        """
        curpath = os.path.abspath(os.getcwd())
        # print('curdir:', curpath)

        inputpath = os.path.normpath(os.path.join(curpath, self.input_path))
        os.chdir(inputpath)

        excel_files = []
        temp_files = glob.glob('*.xlsx')
        for excel in temp_files:
            if '~' not in excel:  # 忽略临时文件
                excel_files.append(excel)

        totoalexcel = len(excel_files)
        currentexcel = 0
        if totoalexcel == 0:
            print("No Excels!")

        # for dic type
        r_dic = re.compile(r"(\d+):")

        jsondata = "{"
        for excel in excel_files:
            currentexcel += 1
            book = xlrd.open_workbook(os.path.normpath(os.path.join(self.input_path, excel)))
            # print("The number of worksheets is", book.nsheets)
            # print("Worksheet name(s):", book.sheet_names())

            # for in excel sheet
            sheet_number = len(book.sheet_names())

            #  sheet index
            sheetindex = 0

            object_name = ''  # 对象名称
            id_counter = 0  # 记录__前缀excel内容id
            for sheetname in book.sheet_names():
                sheetindex += 1
                #print('==sheet name:{0}=='.format(sheetname))

                if not excel.startswith('__'):
                    object_name = sheetname.lower()
                    jsondata += "\"{0}\":{1}".format(object_name, "[")
                elif sheetindex == 1: #  特殊处理__前缀的excel
                    # object_name = excel.lower()  # 这里是采用excel文件名称，现在不使用
                    # object_name = object_name.lstrip('__')
                    # object_name = object_name.rstrip('.xlsx')
                    # jsondata += "\"{0}\":{1}".format(object_name, "[")
                    object_name = sheetname.lower()
                    jsondata += "\"{0}\":{1}".format(object_name, "[")

                sheet = book.sheet_by_name(sheetname)  # get sheet content
                row = 0
                fileds = []
                
                for r in range(0, sheet.nrows):
                    row += 1
                    index = 0  # col index
                    if row > 1:
                        jsondata += "{"

                    for c in range(0, sheet.ncols):
                        # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                        data = sheet.cell_value(rowx=r, colx=c)

                        if row == 1:
                            parts = data.partition('.')
                            # field_type = parts[0] # field type
                            field_real = parts[2]  # filed name
                            # fileds[index]=field_real
                            fileds.append(data)
                            # print('field name:{0}'.format(field_real),)
                            # sys.stdout.write('{0},'.format(field_real))
                        else:
                            # if type(data) is types.StringType:
                            #    data = data.encode('utf-8')
                            # print('{0}:{1}'.format(fileds[index],data) )
                            fieldtype = ''
                            fieldname = fileds[index]

                            if '.' in fieldname:
                                parts = fieldname.partition('.')
                                fieldtype = parts[0]
                                fieldname = parts[2]
                            elif ':' in fieldname:
                                parts = fieldname.partition(':')
                                fieldtype = parts[2]
                                fieldname = parts[0]
                            elif '//' in fieldname or '#' in fieldname:  # comments col
                                continue

                            id_counter += 1

                            fieldtype = str(fieldtype)  # 获得字段Type

                            if fieldtype == Excel2Class.TYPE_INT32 or fieldtype == Excel2Class.TYPE_INT64:
                                try:
                                    data = int(data)
                                    if excel.startswith('__') and fieldname == 'id':  # __的id为自动递增
                                        data = id_counter
                                except:
                                    print(fieldname, "data error")
                                    return
                            elif fieldtype == Excel2Class.TYPE_FLOAT or fieldtype == Excel2Class.TYPE_DOUBLE:
                                try:
                                    data = float(data)
                                    data = round(data, 2)  # 只保留2位小数
                                except:
                                    print(fieldname, "data error")
                                    return
                            elif fieldtype == Excel2Class.TYPE_STRING or fieldtype == "string":
                                data = str(data)
                                data = data.replace("\"", "\\\"")  # 把 " 替换为 \"
                            else:
                                data = str(data)

                            if fieldtype.startswith('arr') or fieldtype.startswith('array'):  # int数组
                                data = data.strip()
                                jsondata += "\"{0}\":[{1}]".format(fieldname, data)
                            elif fieldtype.startswith('farr') or fieldtype.startswith('darr'):  # 浮点型数组
                                data = data.strip()
                                jsondata += "\"{0}\":[{1}]".format(fieldname, data)
                            elif fieldtype.startswith('sarr'):  # 字符串数组
                                data = data.strip()
                                jsondata += "\"{0}\":[{1}]".format(fieldname, data)
                            elif fieldtype.endswith('dic'):
                                data = data.strip()
                                data = r_dic.sub(r"'\1':", data)
                                data = data.replace("\'", "\"")
                                jsondata += "\"{0}\":{1}{2}{3}".format(fieldname, "{", data, "}")
                            elif fieldtype == Excel2Class.TYPE_STRING or fieldtype == 'string':
                                jsondata += "\"{0}\":\"{1}\"".format(fieldname, data)
                            else:
                                jsondata += "\"{0}\":{1}".format(fieldname, data)

                            if index < sheet.ncols-1:
                                jsondata += ","

                        index += 1
                    if row > 1:
                        jsondata += "}"
                        if row < sheet.nrows:
                            jsondata += ","

                if excel.startswith('__'):
                    if sheetindex == sheet_number:
                        jsondata += "]"
                    else:
                        jsondata += ","
                else:
                    jsondata += "]"
                    if sheetindex < sheet_number:
                        jsondata += ','
            if currentexcel < totoalexcel:
                jsondata += ','

        jsondata += "}"
        os.chdir(curpath)

        # io output
        output = os.path.normpath(os.path.join(curpath, self.output_path))
        json_output = os.path.normpath(os.path.join(output, filename + self.suffix))

        with open(json_output, 'w', encoding='utf-8') as targetf:
            targetf.write(jsondata)

        if len(self.password) > 0:
            m = hashlib.md5()

            m.update(jsondata.encode(encoding="utf-8", errors="strict"))
            m.update(self.password.encode(encoding="utf-8", errors="strict"))
            # hash_bytes = m.digest()
            hash_txt = m.hexdigest()
            hash_output = os.path.normpath(os.path.join(output, filename + '_hash' + self.suffix))
            with open(hash_output, 'w', encoding='utf-8') as targetf:
                targetf.write(hash_txt)

        os.chdir(curpath)


