
import docutils.nodes
import docutils.parsers.rst
import docutils.statemachine
import importlib
import os
import textwrap
import xml.etree.ElementTree

yes = set(('yes', 'true', '1', 't', 'y'))

class ZConfigSectionKeys(docutils.parsers.rst.Directive):

    required_arguments = 3 # package, file name, section name

    def run(self):

        package, file_name, section_name = self.arguments
        package = importlib.import_module(package)
        file_name = os.path.join(os.path.dirname(package.__file__), file_name)
        self.state.document.settings.record_dependencies.add(file_name)

        root = xml.etree.ElementTree.parse(file_name)
        [section] = [e for e in root.iter('sectiontype')
                     if e.attrib['name'] == section_name]

        doc = []
        append = doc.append
        for key in sorted(section.iter('key'), key=lambda e: e.attrib['name']):
            append('``{}`` (*{}*'.format(key.attrib['name'],
                                         key.attrib.get('datatype', 'string')))
            if key.attrib.get('required', '').lower() in yes:
                append(', **required**')
            if key.attrib.get('default') is not None:
                append(', default: {}'.format(key.attrib['default']))
            append(')\n')

            descr = []
            for d in key.iter('description'):
                descr.append(''.join(d.itertext()).strip('\n').rstrip() + '\n')

            descr = textwrap.dedent(''.join(descr))

            for line in descr.splitlines():
                append('  ' + line + '\n')

            append('\n')

        result = docutils.statemachine.ViewList(
            ''.join(doc).splitlines(), file_name)
        node = docutils.nodes.paragraph()
        node.document = self.state.document
        self.state.nested_parse(result, 0, node)
        return node.children

def setup(app):
    app.add_directive('zconfigsectionkeys', ZConfigSectionKeys)
