import os
import glob
import xlrd  # must install xlrd!

class Excel2Class(object):
    """
    将Excel数据导出为Class
    每个sheet是一个class,每列对应一个字段
    """
    # define types
    TYPE_INT32 = 'i'  # int
    TYPE_INT64 = 'i64'  # int64
    TYPE_FLOAT = 'f'  # float
    TYPE_DOUBLE = 'd'  # double
    TYPE_Bool = 'b'  # bool
    TYPE_STRING = 's'  # string

    # List
    TYPE_IARRAY = 'array'  # List<int>
    TYPE_FARRAY = 'farray'  # List<float>
    TYPE_DARRAY = 'darray'  # List<double>
    TYPE_SARRAY = 'sarray'  # List<string>

    # Dictionary, the key must be a int
    TYPE_IDIC = 'dic'  # Dictionary<int,int>
    TYPE_FDIC = 'fdic'  # Dictionary<int,float>  # 暂不支持
    TYPE_DDIC = 'ddic'  # Dictionary<int,double>  # 暂不支持
    TYPE_SDIC = 'sdic'  # Dictionary<int,string>  # 暂不支持

    # support languages
    LANG_CS = 'cs'  # c sharp
    LANG_PY = 'py'  # python
    LANG_PHP = 'php'  # PHP

    def __init__(self, input_path='./', output_path='dist/'):
        """
        :param input_path: relative path
        :param output_path: relative path, default 'dist'
        """
        self.input_path = input_path
        self.output_path = output_path
        self.excel_sheets = []
        self.class_files = []
        self.namespace = ''
        self.gameinfoclass = 'GameInfo'
        self.lang = Excel2Class.LANG_CS


    def make(self, namespace='', gameinfoclass='GameInfo', lang=LANG_CS):
        """
        export class files from excel sheet
        :param namespace: class namespace
        :param gameinfoclass: gameinfo class name
        :param lang: support language
        :return: None
        """
        self.namespace = namespace
        self.gameinfoclass = gameinfoclass
        self.lang = lang

        current_path = os.path.abspath(os.getcwd())
        os.chdir(current_path + self.input_path)
        excel_files = glob.glob('*.xlsx')

        # all output files saved int a folder called 'dist'
        if not os.path.isdir(self.output_path):
            os.mkdir(self.output_path)

        # init array
        self.excel_sheets = []
        self.class_files = []

        # check each excel
        for excel in excel_files:
            if excel.startswith("~"):  # 忽略临时文件
                continue
            book = xlrd.open_workbook(os.path.normpath(os.path.join(self.input_path,excel)))
            print("The number of worksheet is", book.nsheets)
            print("Worksheet name(s):", book.sheet_names())
            if book.nsheets == 0:
                continue
        
            # check each excel sheet
            for sheetname in book.sheet_names():
                sheet = book.sheet_by_name(sheetname)
                self.excel_sheets.append(sheetname)
                self.class_files.append(sheetname)

                if lang == Excel2Class.LANG_CS:  # write c# class file
                    self.write_cs(sheet, sheetname)
                elif lang == Excel2Class.LANG_PY:  # write python class file
                    self.write_py(sheet, sheetname)
                elif lang == Excel2Class.LANG_PHP:  # write php class file
                    self.write_php(sheet, sheetname)

                if excel.startswith("__"):  # __开头的excel文件，只处理第一个sheet
                    break

        if lang == Excel2Class.LANG_CS:
            self.write_cs_gameinfo()
        elif lang == Excel2Class.LANG_PY:
            self.write_py_gameinfo()
        elif lang == Excel2Class.LANG_PHP:
            self.write_php_gameinfo()
        # done!           
        os.chdir(current_path)


    def write_cs(self, sheet:xlrd.sheet.Sheet, sheetname: str):
        """
        生成.cs class file
        """
        output_filename = os.path.normpath('{0}/{1}.cs'.format(self.output_path, sheetname))

        with open(output_filename, 'w', encoding='utf-8') as targetf:
            targetf.write('using System.Collections;\n')
            targetf.write('using System.Collections.Generic;\n')
            targetf.write('using NetTiger;\n')
            targetf.write("// 2016 上海网虎网络科技有限公司版权所有，未经许可，不得使用\n")
            targetf.write("// 本代码为自动生成，请不要手工修改\n\n")
            if len(self.namespace) > 0:
                targetf.write('namespace {0}{1}\n\n'.format(self.namespace, "{"))
            targetf.write('    public class {0}: IDObject {1} \n'.format(sheetname, "{"))
                   
            for r in range(0, sheet.nrows):   # write class name
                for c in range(0, sheet.ncols):
                    # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                    data = sheet.cell_value(rowx=r, colx=c)
                    data.strip()
                    data_type = ''  # field type
                    field_name = ''  # field name
                    if '.' in data:
                        parts = data.partition('.')  # old stype int.id
                        data_type = parts[0]
                        field_name = parts[2]
                    elif ':' in data:
                        parts = data.partition(':')  # new stype id:int
                        data_type = parts[2]
                        field_name = parts[0]
                    elif '//' in data or '#' in data:  # 注释行
                        continue
                    else:  # 未加定义的类型
                        print(data, "Type Not defined!")
                        continue

                    if field_name == 'id':  # 该属性继承自基类
                        continue
                    # print(data_type, data_real)
                    # if c == sheet.ncols-1:
                    #    sep='\n'
                    if data_type == Excel2Class.TYPE_INT32:
                        data_type = 'int'
                    elif data_type == Excel2Class.TYPE_INT64:
                        data_type = 'System.Int64'
                    elif data_type == Excel2Class.TYPE_FLOAT:
                        data_type = 'float'
                    elif data_type == Excel2Class.TYPE_DOUBLE:
                        data_type = 'double'
                    elif data_type == Excel2Class.TYPE_Bool:
                        data_type = 'bool'
                    elif data_type == Excel2Class.TYPE_STRING:
                        data_type = 'string'
                    elif data_type == Excel2Class.TYPE_IARRAY or data_type == 'arr':
                        data_type = 'List<int>'
                    elif data_type == Excel2Class.TYPE_FARRAY or data_type == 'farr':
                        data_type = 'List<float>'
                    elif data_type == Excel2Class.TYPE_DARRAY or data_type == 'darr':
                        data_type = 'List<double>'
                    elif data_type == Excel2Class.TYPE_SARRAY or data_type == 'sarr':
                        data_type = 'List<string>'
                    elif data_type == Excel2Class.TYPE_IDIC:
                        data_type = 'Dictionary<int,int>'
                    elif data_type == Excel2Class.TYPE_FDIC:  # 不支持
                        data_type = 'Dictionary<int,float>'
                        print("do not support type Dictionary<int,float>")
                    elif data_type == Excel2Class.TYPE_DDIC:  # 不支持
                        data_type = 'Dictionary<int,double>'
                        print("do not support type Dictionary<int,double>")
                    elif data_type == Excel2Class.TYPE_SDIC:  # 不支持
                        data_type = 'Dictionary<int,string>'
                        print("do not support type Dictionary<int,string>")
                    targetf.write('        public {0} {1};\n'.format(data_type, field_name))
                    # print(data_type, data_real)

                break  # only scan the first row
            if len(self.namespace) > 0:
                targetf.write('    }')
            targetf.write('\n}')
            print('output .cs class:', output_filename)

    def write_py(self, sheet: xlrd.sheet.Sheet, sheetname: str):
        """
        生成.py class file
        """
        output_filename = os.path.normpath('{0}/{1}.py'.format(self.output_path, sheetname))

        with open(output_filename, 'w', encoding='utf-8') as targetf:
            targetf.write("\"\"\"\n")
            targetf.write("# 2016 上海网虎网络科技有限公司版权所有，未经许可，不得使用\n")
            targetf.write("# 本代码为自动生成，请不要手工修改\n")
            targetf.write("\"\"\"\n")
            targetf.write("\n\n")
            # targetf.write('from ntutil.jsonhelper import JsonClass\n\n')
            targetf.write('class {0}({1}): \n'.format(sheetname, "object"))
            targetf.write('    def __init__(self):\n')
             
            for r in range(0, sheet.nrows):   # write class name
                for c in range(0, sheet.ncols):
                    # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                    data = sheet.cell_value(rowx=r, colx=c)
                    data.strip()
                    data_type = ''  # field type
                    data_real = ''  # field name
                    if '.' in data:
                        parts = data.partition('.')  # old stype int.id
                        data_type = parts[0]
                        data_real = parts[2]
                    elif ':' in data:
                        parts = data.partition(':')  # new stype id:int
                        data_type = parts[2]
                        data_real = parts[0]
                    elif '//' in data or '#' in data:  # 注释行
                        continue
                    else:  # 未加定义的类型
                        print(data, "Type Not defined!")
                        continue
                    # print(data_type, data_real)
                    # if c == sheet.ncols-1:
                    #    sep='\n'
                    if data_type == Excel2Class.TYPE_INT32:
                        data_type = 0
                    elif data_type == Excel2Class.TYPE_INT64:
                        data_type = 0
                    elif data_type == Excel2Class.TYPE_FLOAT:
                        data_type = 0
                    elif data_type == Excel2Class.TYPE_DOUBLE:
                        data_type = 0
                    elif data_type == Excel2Class.TYPE_Bool:
                        data_type = "True"
                    elif data_type == Excel2Class.TYPE_STRING:
                        data_type = "''"
                    elif data_type == Excel2Class.TYPE_IARRAY or data_type == 'arr':
                        data_type = "[]"
                    elif data_type == Excel2Class.TYPE_FARRAY or data_type == 'farr':
                        data_type = "[]"
                    elif data_type == Excel2Class.TYPE_DARRAY or data_type == 'darr':
                        data_type = "[]"
                    elif data_type == Excel2Class.TYPE_SARRAY or data_type == 'sarr':
                        data_type = "[]"
                    elif data_type == Excel2Class.TYPE_IDIC:
                        data_type = "{}"
                    elif data_type == Excel2Class.TYPE_FDIC:
                        data_type = "{}"
                    elif data_type == Excel2Class.TYPE_DDIC:
                        data_type = "{}"
                    elif data_type == Excel2Class.TYPE_SDIC:
                        data_type = "{}"
                    else:
                        data_type = "None"
                    targetf.write('        self.{0} = {1}\n'.format(data_real, data_type))
                    # print(data_type, data_real)

                break  # only scan the first row

            # 为每个变量创建一个字符串名称
            for r in range(0, sheet.nrows):   # write class name
                targetf.write('\n')
                for c in range(0, sheet.ncols):
                    # print ("Cell:", sheet.cell_value(rowx=r, colx=c) )
                    data = sheet.cell_value(rowx=r, colx=c)
                    data.strip()
                    data_type = ''  # field type
                    data_real = ''  # field name
                    if '.' in data:
                        parts = data.partition('.')  # old stype int.id
                        data_type = parts[0]
                        data_real = parts[2]
                    elif ':' in data:
                        parts = data.partition(':')  # new stype id:int
                        data_type = parts[2]
                        data_real = parts[0]

                    targetf.write('    @staticmethod\n')
                    targetf.write('    def {0}_str()->str:\n'.format(data_real))
                    targetf.write('        return "{0}"\n\n'.format(data_real))

                break  # only scan the first row

            print('output .py class:', output_filename)

    def write_php(self, sheet: xlrd.sheet.Sheet, sheetname: str):
        """
        生成.php class file
        """
        pass

    def write_cs_gameinfo(self):
        """
        生成.cs version gameinfo class
        """
        gameinfo_output_path = os.path.normpath('{0}/{1}.cs'.format(self.output_path, self.gameinfoclass))

        with open(gameinfo_output_path, 'w', encoding='utf-8') as targetf:
            targetf.write('using System.Collections;\n\n')
            targetf.write('using System.Collections.Generic;\n')
            targetf.write("// 2016 上海网虎网络科技有限公司版权所有，未经许可，不得使用\n")
            targetf.write("// 本代码为自动生成，请不要手工修改\n\n")
            if len(self.namespace) > 0:
                targetf.write('namespace {0}{1}\n\n'.format(self.namespace, "{"))
            targetf.write('    public class {0}{1} \n'.format(self.gameinfoclass, "{"))
        
            # write fields
            for datatype in self.excel_sheets:
                dataname = datatype.lower()
                targetf.write('        public List<{0}> {1};\n'.format(datatype, dataname))

            if len(self.namespace) > 0:
                targetf.write('    }')
            targetf.write('\n}')

        # write IDObject as base json data class
        idobject_output_path = os.path.normpath('{0}/{1}.cs'.format(self.output_path, 'IDObject.cs'))
        with open(idobject_output_path, 'w', encoding='utf-8') as targetf:
            targetf.write("// 2016 上海网虎网络科技有限公司版权所有，未经许可，不得使用\n")
            targetf.write("// 本代码为自动生成，请不要手工修改\n\n")
            targetf.write('namespace {0}{1}\n\n'.format('NetTiger', "{"))
            targetf.write('    public class {0}{1} \n'.format('IDObject', "{"))
            # write id fields
            targetf.write('        public {0} {1} = 0;\n'.format('int', 'id'))

            targetf.write('    }')  # namespace
            targetf.write('\n}')

        print('output .cs game info:', gameinfo_output_path)

    def write_py_gameinfo(self):
        """
        生成.py version gameinfo class
        """
        gameinfo_output_path = os.path.normpath('{0}/{1}.py'.format(self.output_path, self.gameinfoclass))

        with open(gameinfo_output_path, 'w', encoding='utf-8') as targetf:
            targetf.write("\"\"\"\n")
            targetf.write("# 2016 上海网虎网络科技有限公司版权所有，未经许可，不得使用\n")
            targetf.write("# 本代码为自动生成，请不要手工修改\n")
            targetf.write("\"\"\"\n")
            # targetf.write('from ntutil.jsonhelper import JsonClass\n')
            for datatype in self.excel_sheets:
                targetf.write('import {0}\n'.format(datatype))
            targetf.write('\n')
            targetf.write('class {0}({1}): \n'.format(self.gameinfoclass, "object"))
            targetf.write('    def __init__(self):\n')
            
            # write fields
            for datatype in self.excel_sheets:
                dataname = datatype.lower()
                targetf.write('        self.{0} = {1}.{1}()\n'.format(dataname, datatype))

        print('output .py game info:', gameinfo_output_path)

    def write_php_gameinfo(self):
        """
        生成.php version gameinfo class
        """
        pass
