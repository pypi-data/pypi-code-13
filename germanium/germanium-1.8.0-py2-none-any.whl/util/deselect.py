from selenium.webdriver.support.select import Select

from germanium.impl import _ensure_list
from ._element import _element
from .find_germanium_object import find_germanium_object


def deselect_g(context, selector, text=None, *argv, **kw):
    index = None
    if "index" in kw:
        index = kw.get("index")
        kw.pop("index")

    value = None
    if "value" in kw:
        value = kw.get("value")
        kw.pop("value")

    germanium = find_germanium_object(context)
    select_element = _element(germanium, selector)

    s = Select(select_element)

    if text is not None:
        for single_text in _ensure_list(text):
            s.deselect_by_visible_text(single_text)
    if index is not None:
        for single_index in _ensure_list(index):
            single_index = int(single_index)
            s.deselect_by_index(single_index)
    if value is not None:
        for single_value in _ensure_list(value):
            s.deselect_by_value(single_value)

    if not text and not index and not value:
        s.deselect_all()
