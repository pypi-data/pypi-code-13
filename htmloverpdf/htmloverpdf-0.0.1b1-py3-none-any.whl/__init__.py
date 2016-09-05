"""htmloverpdf"""

import io
from copy import deepcopy
import gi
gi.require_version('Poppler', '0.18')
from gi.repository import Poppler, Gio, GLib
import cairo
import cairocffi
from lxml import etree
import weasyprint

def render(html):
    """Convert HTML to a PDF"""

    output = io.BytesIO()
    surface = cairo.PDFSurface(output, 595, 842)
    ctx = cairo.Context(surface)
    cffictx = cairocffi.Context._from_pointer(cairocffi.ffi.cast('cairo_t **', id(ctx) + object.__basicsize__)[0], incref=True)

    html = etree.parse(io.StringIO(html), etree.HTMLParser())

    for pdf in html.xpath("//img[substring(@src, string-length(@src) - 3)=\'.pdf\']"):
        for prev in pdf.xpath("preceding-sibling::*"):
            pdf.getparent().remove(prev)
        pdfsrc = pdf.get("src")
        pdf.getparent().remove(pdf)
        section = deepcopy(html)
        for nextpdf in section.xpath("//img[substring(@src, string-length(@src) - 3)=\'.pdf\']"):
            for nextel in nextpdf.xpath("following-sibling::*"):
                nextpdf.getparent().remove(nextel)
            nextpdf.getparent().remove(nextpdf)

        html_pages = weasyprint.HTML(tree=section).render().pages
        surface.set_size(html_pages[0].width * 72 / 96.0, html_pages[0].height * 72 / 96.0)

        if pdfsrc != "blank.pdf":
            with weasyprint.default_url_fetcher(str(pdfsrc))['file_obj'] as fetch:
                pdf_pages = Poppler.Document.new_from_stream(Gio.MemoryInputStream.new_from_bytes(GLib.Bytes.new_take(fetch.read())), -1, None, None)
        else:
            pdf_pages = None
        for pageno in range(max(pdf_pages.get_n_pages() if pdf_pages else 0, len(html_pages))):
            if pdf_pages and pageno < pdf_pages.get_n_pages():
                pdf_pages.get_page(pageno).render_for_printing(ctx)
            if pageno < len(html_pages):
                html_pages[pageno].paint(cffictx)
            ctx.show_page()
    surface.finish()
    return output.getbuffer()
