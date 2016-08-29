'''
--------------------------------------------------------------------------
Copyright (C) 2016 Lukasz Laba <lukaszlab@o2.pl>

File version 0.5 date 2016-08-30

This file is part of SeePy.
SeePy is a python script visualisation tool.
http://seepy.org/

SeePy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

SeePy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
--------------------------------------------------------------------------
'''

import os
import re

from PyQt4 import QtGui

class Code ():
    
    def __init__(self):
        #---
        self.script_path = ''
        self.savedir = os.path.dirname(__file__)
        #---
        self.code_oryginal = ''
        self.code_parsed = ''

    def parse(self, path = ''):
        if not path :
            path = self.script_path
        if not path :
            self.newFile('x_newtemplate.py')
            path = self.script_path
        f = open(path, 'r')
        script = f.read()
        self.code_oryginal = script
        #-------------------------------------------------------------------------
        #Here the code_oryginal is changed in to code_parsed with re.sub() replace
        #-------------------------------------------------------------------------
        script = re.sub(r'\r\n', r'\n', script) #new line \n (Linux) vs \r\n (windows) problem
        #--Variable with one line comment syntax
        script = re.sub(    r'(\w+)(.+)#!(.+)',
                            r"\1\2 \nr_comment('\1 = %(\1)s \3' % vars_formated())",
                            script  )
        #--One line comment syntax
        script = re.sub(    r'#!(.+)',
                            r"r_comment('\1' % vars_formated())",
                            script  )
        #--Multi line comment syntax 
        script = re.sub(    r"#!(.{1})'''(.+?)'''",
                            r"r_comment('''\2''' % vars_formated())", 
                            script, flags=re.DOTALL )
        #--One line python code showing syntax
        script = re.sub(    r"(.+)#%code",
                            r"\1\nr_comment('''```\1```''' )",
                            script  )
        #--Multi line python code showing syntax
        script = re.sub(    r"#%code(.+?)#%", 
                            r"\1r_comment('''```\1```''' )",
                            script, flags=re.DOTALL )
        #--Image showing syntax
        script = re.sub(    r'#%img (.+)',
                            r"r_img('\1')", 
                            script  )
        #--Matplotlib plt figure syntax
        script = re.sub(    r'(\w+)(.+)#%plt',
                            r"\1\2 \nr_plt(\1)",
                            script)
        #--One line LaTex syntax comment rendering
        script = re.sub(    r'#%tex (.+)',
                            r"r_tex(r'\1' % vars())", 
                            script  )
        #--Rendering LaTex syntax from python string
        script = re.sub(    r'(\w+) #%stringtex',
                            r"\1 \nr_tex(\1)",
                            script)
        #--One line code rendering as LaTex syntax with replace ** to ^
        script = re.sub(    r'(.+)#%tex',
                            r"\1\nr_codetex(r'\1' % vars_formated())",
                            script  )
        #--Rendering SVG syntax from python string
        script = re.sub(    r'(\w+)(.+)#%svg',
                            r"\1\2 \nr_svg(\1)",
                            script)
        #--Adjustable wariable with one line comment syntax
        script = re.sub(r'#(<{2,})', r"#\1_idx_", script)
        no = 1  
        while re.search(r"#<{2,}_idx_", script):
            script = script.replace(r'<_idx_', r"<_id%s_" % no, 1)
            no += 1
        script = re.sub(    r'(\w+)(.+)#<<_(.+)_(.+)', 
                            r"\1\2 \nr_adj('\1 = %(\1)s' % vars_formated(),'\3','\4' % vars_formated(), 1, '\1\2')",
                            script  )
        script = re.sub(    r'(\w+)(.+)#<<<_(.+)_(.+)', 
                            r"\1\2 \nr_adj('%(\1)s' % vars_formated(),'\3','\4' % vars_formated(), 1, '\1\2')",
                            script  )
        script = re.sub(    r'(\w+)(.+)#<<<<_(.+)_(.+)', 
                            r"\1\2 \nr_adj('%(\1)s' % vars_formated(),'\3','\4' % vars_formated(), 2,  '\1\2')",
                            script  )     
        
        #--saving
        self.code_parsed = script 
        
    def openFile(self):
        #---asking for file path
        filename = QtGui.QFileDialog.getOpenFileName(caption = 'Open script',
                                                directory = self.savedir,
                                                filter = "Python script (*.py)")
        filename = str(filename)
        #---
        if not filename == '':
            self.savedir = os.path.dirname(filename)
            self.script_path = filename
            self.parse()
            
    def newFile(self, template_path, info='Save as', initfilename='your_script'):
        #---asking for file path
        filename = QtGui.QFileDialog.getSaveFileName(caption = 'Open script',
                                                directory = self.savedir + '/' + initfilename,
                                                filter = "Python script (*.py)")
        filename = str(filename)
        #---
        if not filename == '':
            new_template = open(template_path, 'r').read()
            self.savedir = os.path.dirname(filename)
            text_file = open(filename, "w")
            text_file.write(new_template)
            text_file.close()
            self.script_path = filename
            self.parse()
        
    def editCode(self, lineID = 'id1', setvalues = None, index = None):
        if setvalues == 'None':
            setvalues = None
        #---
        script = self.code_oryginal
        #---
        script = re.sub(r'#(<{2,})', r"#\1_idx_", script)
        no = 1  
        while re.search(r"#<{2,}_idx_", script):
            script = script.replace(r'<_idx_', r"<_id%s_" % no, 1)
            no += 1 
        #---OPTION 1 Selectind one form list if list
        if setvalues :
            setvalues = re.search(r'[[](.+)[]]', setvalues).group(1)
            setvalues = setvalues.replace(" ", "")
            setvalues = setvalues.replace("'", "")
            setvalues = setvalues.split(',')
            #---            
            expresion = re.search(r'(\w+)\s*=\s*(.+)[[](\d+)[]]\s*#<{2,}_%s_'%lineID, script)
            variable = expresion.group(1)
            listindex = int(expresion.group(3))
            #---asking for new value
            value_selected = QtGui.QInputDialog.getItem(None, 'Set new value', variable +'=', setvalues, listindex, False)[0]
            #---
            if value_selected:
                index_selected = setvalues.index(value_selected)
            else:
                index_selected = listindex
            print index_selected    
            #---
            script = re.sub(    r'(\w+)\s*=\s*(.+)[[]\w+[]]\s*#(<{2,})_%s_'%lineID,
                                r'\1 = \2[%s] #\3_%s_'%(index_selected, lineID),
                                script  )
        #---OPTION 2 Geting new variable value       
        else:  
            expresion = re.search(r'(\w+) = (.+) #<{2,}_%s_'%lineID, script)
            variable = expresion.group(1)
            value = expresion.group(2)
            #---asking for new value from choice list
            value = QtGui.QInputDialog.getText(None, 'Set new value',variable +'=', QtGui.QLineEdit.Normal,value)[0]       
            #---
            script = re.sub(    r'(\w+) = (.+)#(<{2,})_%s_'%lineID,
                                r'\1 = %s #\3_%s_'%(value, lineID),
                                script  )
        #---
        script = re.sub(r"#(<{2,})_id(.+)_", r'#\1', script)
        #---
        self.code_oryginal = script
        #---
        file = open(self.script_path, "r+")
        file.write(script)
        file.close()

# Test if main
if __name__ == '__main__':
    ScriptCode = Code()
    #ScriptCode.openFile()
    #ScriptCode.parse()
    #print ScriptCode.code_oryginal
    #print ScriptCode.code_parsed
    #print ScriptCode.savedir
    #ScriptCode.openFile()
    #ScriptCode.newFile()
    #ScriptCode.editCode()