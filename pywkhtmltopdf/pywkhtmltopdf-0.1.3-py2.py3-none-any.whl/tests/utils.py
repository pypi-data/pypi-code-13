"""
Utility functions for managing test data and converting files.
"""

import pywkhtmltopdf as pdf
import os

def render_pdf(input_html):
    c = pdf.HTMLToPDFConverter()
    return c.convert(input_html)

def convert_to_pdf(input_filename, output_filename):
    with open(input_filename, 'r') as fp:
        data = render_pdf(fp.read())
    with open(output_filename, 'wb') as fp:
        fp.write(data)

def convert_all():
    """
    Converts all HTML files in the test data directory to PDFs in the same
    directory.
    """
    d = os.path.join(os.path.dirname(__file__), 'data')
    files = [os.path.join(d, f) for f in os.listdir(d) if f.endswith('.html')]
    for input_filename in files:
        output_filename = os.path.splitext(input_filename)[0] + '.pdf'
        convert_to_pdf(input_filename, output_filename)
