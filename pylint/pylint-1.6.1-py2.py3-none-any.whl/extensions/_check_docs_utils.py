# Licensed under the GPL: https://www.gnu.org/licenses/old-licenses/gpl-2.0.html
# For details: https://github.com/PyCQA/pylint/blob/master/COPYING

"""Utility methods for docstring checking."""

from __future__ import absolute_import, print_function

import re

import astroid

from pylint.checkers.utils import node_ignores_exception


def space_indentation(s):
    """The number of leading spaces in a string

    :param str s: input string

    :rtype: int
    :return: number of leading spaces
    """
    return len(s) - len(s.lstrip(' '))


def returns_something(return_node):
    """Check if a return node returns a value other than None.

    :param return_node: The return node to check.
    :type return_node: astroid.Return

    :rtype: bool
    :return: True if the return node returns a value other than None,
        False otherise.
    """
    returns = return_node.value

    if returns is None:
        return False

    return not (isinstance(returns, astroid.Const) and returns.value is None)


def possible_exc_types(node):
    """
    Gets all of the possible raised exception types for the given raise node.

    .. note::

        Caught exception types are ignored.


    :param node: The raise node to find exception types for.
    :type node: astroid.node_classes.NodeNG

    :returns: A list of exception types possibly raised by :param:`node`.
    :rtype: list(str)
    """
    excs = []
    if isinstance(node.exc, astroid.Name):
        excs = [node.exc.name]
    elif (isinstance(node.exc, astroid.Call) and
          isinstance(node.exc.func, astroid.Name)):
        excs = [node.exc.func.name]
    elif node.exc is None:
        handler = node.parent
        while handler and not isinstance(handler, astroid.ExceptHandler):
            handler = handler.parent

        if handler and handler.type:
            excs = (exc.name for exc in astroid.unpack_infer(handler.type))

    excs = set(exc for exc in excs if not node_ignores_exception(node, exc))
    return excs

def docstringify(docstring):
    for docstring_type in [SphinxDocstring, GoogleDocstring, NumpyDocstring]:
        instance = docstring_type(docstring)
        if instance.is_valid():
            return instance

    return Docstring(docstring)

class Docstring(object):
    re_for_parameters_see = re.compile(r"""
        For\s+the\s+(other)?\s*parameters\s*,\s+see
        """, re.X | re.S)

    # These methods are designed to be overridden
    # pylint: disable=no-self-use
    def __init__(self, doc):
        doc = doc or ""
        self.doc = doc.expandtabs()

    def is_valid(self):
        return False

    def exceptions(self):
        return set()

    def has_params(self):
        return False

    def has_returns(self):
        return False

    def match_param_docs(self):
        return set(), set()

    def params_documented_elsewhere(self):
        return self.re_for_parameters_see.search(self.doc) is not None

class SphinxDocstring(Docstring):
    re_type = r"[\w\.]+"

    re_xref = r"""
        (?::\w+:)?                    # optional tag
        `{0}`                         # what to reference
        """.format(re_type)

    re_param_in_docstring = re.compile(r"""
        :param                  # Sphinx keyword
        \s+                     # whitespace

        (?:                     # optional type declaration
        ({type})
        \s+
        )?

        (\w+)                   # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """.format(type=re_type), re.X | re.S)

    re_type_in_docstring = re.compile(r"""
        :type                   # Sphinx keyword
        \s+                     # whitespace
        ({type})                # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """.format(type=re_type), re.X | re.S)

    re_raise_in_docstring = re.compile(r"""
        :raises                 # Sphinx keyword
        \s+                     # whitespace

        (?:                     # type declaration
        ({type})
        \s+
        )?

        (\w+)                   # Parameter name
        \s*                     # whitespace
        :                       # final colon
        """.format(type=re_type), re.X | re.S)

    re_rtype_in_docstring = re.compile(r":rtype:")

    re_returns_in_docstring = re.compile(r":returns?:")

    def is_valid(self):
        return bool(self.re_param_in_docstring.search(self.doc) or
                    self.re_raise_in_docstring.search(self.doc) or
                    self.re_rtype_in_docstring.search(self.doc) or
                    self.re_returns_in_docstring.search(self.doc))

    def exceptions(self):
        types = set()

        for match in re.finditer(self.re_raise_in_docstring, self.doc):
            raise_type = match.group(2)
            types.add(raise_type)

        return types

    def has_params(self):
        if not self.doc:
            return False

        return self.re_param_in_docstring.search(self.doc) is not None

    def has_returns(self):
        if not self.doc:
            return False

        return (self.re_rtype_in_docstring.search(self.doc) and
                self.re_returns_in_docstring.search(self.doc))

    def match_param_docs(self):
        params_with_doc = set()
        params_with_type = set()

        for match in re.finditer(self.re_param_in_docstring, self.doc):
            name = match.group(2)
            params_with_doc.add(name)
            param_type = match.group(1)
            if param_type is not None:
                params_with_type.add(name)

        params_with_type.update(re.findall(self.re_type_in_docstring, self.doc))
        return params_with_doc, params_with_type


class GoogleDocstring(Docstring):
    re_type = SphinxDocstring.re_type

    re_xref = SphinxDocstring.re_xref

    re_container_type = r"""
        (?:{type}|{xref})             # a container type
        [\(\[] [^\n]+ [\)\]]          # with the contents of the container
    """.format(type=re_type, xref=re_xref)

    _re_section_template = r"""
        ^([ ]*)   {0} \s*:   \s*$     # Google parameter header
        (  .* )                       # section
        """

    re_param_section = re.compile(
        _re_section_template.format(r"(?:Args|Arguments|Parameters)"),
        re.X | re.S | re.M
    )

    re_param_line = re.compile(r"""
        \s*  \*{{0,2}}(\w+)             # identifier potentially with asterisks
        \s*  ( [(]
            (?:{container_type}|{type})
            [)] )? \s* :                # optional type declaration
        \s*  (.*)                       # beginning of optional description
    """.format(
        type=re_type,
        container_type=re_container_type
    ), re.X | re.S | re.M)

    re_raise_section = re.compile(
        _re_section_template.format(r"Raises"),
        re.X | re.S | re.M
    )

    re_raise_line = re.compile(r"""
        \s*  ({type}) \s* :              # identifier
        \s*  (.*)                        # beginning of optional description
    """.format(type=re_type), re.X | re.S | re.M)

    re_returns_section = re.compile(
        _re_section_template.format(r"Returns?"),
        re.X | re.S | re.M
    )

    re_returns_line = re.compile(r"""
        \s* ({container_type}:|{type}:)?  # identifier
        \s* (.*)                          # beginning of description
    """.format(
        type=re_type,
        container_type=re_container_type
    ), re.X | re.S | re.M)

    def is_valid(self):
        return bool(self.re_param_section.search(self.doc) or
                    self.re_raise_section.search(self.doc) or
                    self.re_returns_section.search(self.doc))

    def has_params(self):
        if not self.doc:
            return False

        return self.re_param_section.search(self.doc) is not None

    def has_returns(self):
        if not self.doc:
            return False

        entries = self._parse_section(self.re_returns_section)
        for entry in entries:
            match = self.re_returns_line.match(entry)
            if not match:
                continue

            return_type = match.group(1)
            return_desc = match.group(2)
            if return_type and return_desc:
                return True

        return False

    def exceptions(self):
        types = set()

        entries = self._parse_section(self.re_raise_section)
        for entry in entries:
            match = self.re_raise_line.match(entry)
            if not match:
                continue

            exc_type = match.group(1)
            exc_desc = match.group(2)
            if exc_desc:
                types.add(exc_type)

        return types

    def match_param_docs(self):
        params_with_doc = set()
        params_with_type = set()

        entries = self._parse_section(self.re_param_section)
        for entry in entries:
            match = self.re_param_line.match(entry)
            if not match:
                continue

            param_name = match.group(1)
            param_type = match.group(2)
            param_desc = match.group(3)
            if param_type:
                params_with_type.add(param_name)

            if param_desc:
                params_with_doc.add(param_name)

        return params_with_doc, params_with_type

    @staticmethod
    def min_section_indent(section_match):
        return len(section_match.group(1)) + 1

    def _parse_section(self, section_re):
        section_match = section_re.search(self.doc)
        if section_match is None:
            return []

        min_indentation = self.min_section_indent(section_match)

        entries = []
        entry = []
        is_first = True
        for line in section_match.group(2).splitlines():
            if not line.strip():
                continue
            indentation = space_indentation(line)
            if indentation < min_indentation:
                break

            # The first line after the header defines the minimum
            # indentation.
            if is_first:
                min_indentation = indentation
                is_first = False

            if indentation == min_indentation:
                # Lines with minimum indentation must contain the beginning
                # of a new parameter documentation.
                if entry:
                    entries.append("\n".join(entry))
                    entry = []

            entry.append(line)

        if entry:
            entries.append("\n".join(entry))

        return entries

class NumpyDocstring(GoogleDocstring):
    _re_section_template = r"""
        ^([ ]*)   {0}   \s*?$          # Numpy parameters header
        \s*     [-=]+   \s*?$          # underline
        (  .* )                        # section
    """

    re_param_section = re.compile(
        _re_section_template.format(r"(?:Args|Arguments|Parameters)"),
        re.X | re.S | re.M
    )

    re_param_line = re.compile(r"""
        \s*  (\w+)                      # identifier
        \s*  :
        \s*  ({container_type}|{type})? # optional type declaration
        \n                              # description starts on a new line
        \s* (.*)                        # description
    """.format(
        type=GoogleDocstring.re_type,
        container_type=GoogleDocstring.re_container_type
    ), re.X | re.S)

    re_raise_section = re.compile(
        _re_section_template.format(r"Raises"),
        re.X | re.S | re.M
    )

    re_raise_line = re.compile(r"""
        \s* ({type})$   # type declaration
        \s* (.*)        # optional description
    """.format(type=GoogleDocstring.re_type), re.X | re.S | re.M)

    re_returns_section = re.compile(
        _re_section_template.format(r"Returns?"),
        re.X | re.S | re.M
    )

    re_returns_line = re.compile(r"""
        \s* ({container_type}|{type})$ # type declaration
        \s* (.*)                       # optional description
    """.format(
        type=GoogleDocstring.re_type,
        container_type=GoogleDocstring.re_container_type
    ), re.X | re.S | re.M)

    @staticmethod
    def min_section_indent(section_match):
        return len(section_match.group(1))
