# XSLX object class

DEBUG = False

import os, re, tempfile
from lxml import etree

from bl.dict import Dict
from bl.string import String
from bl.zip import ZIP
from bxml.xml import XML
from bf.text import Text

class XLSX(ZIP):
    NS = Dict(
        # document namespaces, in xl/*.xml
        xl="http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        r="http://schemas.openxmlformats.org/officeDocument/2006/relationships",
        mc="http://schemas.openxmlformats.org/markup-compatibility/2006",
        x14ac="http://schemas.microsoft.com/office/spreadsheetml/2009/9/ac"
    )

    def tempfile(self):
        "write the docx to a named tmpfile and return the tmpfile filename"
        tf = tempfile.NamedTemporaryFile()
        tfn = tf.name
        tf.close()
        os.remove(tf.name)
        shutil.copy(self.fn, tfn)
        return tfn

    def write(self, fn=None):
        fn = fn or self.fn
        if not os.path.exists(os.path.dirname(fn)):
            os.makedirs(os.path.dirname(fn))
        f = open(self.fn, 'rb'); b = f.read(); f.close()
        f = open(fn, 'wb'); f.write(b); f.close()

    def transform(self, transformer, fn=None, XMLClass=None, **params):
        return self.xml(fn=fn, transformer=transformer, XMLClass=XMLClass, **params)

    def read(self, src):
        """return file data from within the docx file"""
        return self.zipfile.read(src)

    def sheets(self):
        "return the sheets of data."
        data = Dict()
        for src in [src for src in self.zipfile.namelist() if 'xl/worksheets/' in src]:
            name = os.path.splitext(os.path.basename(src))[0]
            xml = self.xml(src)
            data[name] = xml
        return data

    def xml(self, src):
        "return the xml from the src"
        return XML(root=self.read(src))
