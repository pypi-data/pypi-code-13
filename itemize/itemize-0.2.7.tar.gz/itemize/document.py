import logging
import os
import tempfile
import cups
from jinja2 import Environment, PackageLoader, FileSystemLoader
from z3c.rml import rml2pdf

logger = logging.getLogger(__name__)

class Document(object):
    def __init__(self, template_name=None, data={}):
        self._template_name = template_name
        self._data = data
        self._template = None
        self._filename = None
        self._pdf = None

        self.load_template(template_name)
        self.render()

    def load_template(self, template_name):
        # Load the RML template into the preprocessor.
        logger.info('Loading RML/Jinja2 Template.')
        environment = None
        try:
            logger.debug('Loading templates package with PackageLoader.')
            environment = Environment(loader=PackageLoader('itemize', 'templates'))
        except ImportError as e:
            logger.debug('Loading templates package with FileSystemLoader.')
            environment = Environment(loader=FileSystemLoader('templates'))

        template = environment.get_template(
            '%s/template.rml.jinja2' % template_name)
        logger.info('Loaded RML/Jinja2 Template.')

        self._template = template
        return template

    def render(self):
        # Do preprocessing.
        logger.info('Rendering template.')
        rml_text = self._template.render(self._data)
        rml_text = rml_text.strip()
        logger.info('Rendered template.')

        # Generate PDF output.
        logger.info('Generating PDF document.')
        pdf = rml2pdf.parseString(rml_text)
        logger.info('Generated PDF document.')

        self._pdf = pdf
        return self._pdf

    def save(self, path):
        filename = os.path.basename(path)
        logger.info('Saving PDF document.')

        if not self._pdf:
            self.render()

        with open(path, 'wb') as pdf_file:
            pdf_file.write(self._pdf.read())
        logger.info('Saved PDF document.')

        self._filename = filename
        return self._filename

    def print(self):

        printers = None
        try:
            connection = cups.Connection()
        except RuntimeError as e:
            logger.error(
                'Unable to connect to printer: CUPS server is not running. '
                '(Hint: run `sudo /etc/init.d/cups start`).')
        else:
            printers = connection.getPrinters()

        printed = False
        if printers:
            printer = [printer for printer in printers][0]

            if 'paused' in printers[printer]['printer-state-reasons']:
                print('Enabling printer...')
                connection.enablePrinter(printer)

            if not self.filename:
                temporary_file = tempfile.NamedTemporaryFile()
                self.save(temporary_file.name)

            logger.info('Printing document.')
            connection.printFile(printer, self.filename, 'Label', {})
            printed = True
            logger.info('Printed document.')

        return printed

    @property
    def filename(self):
        return self._filename
