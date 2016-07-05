"""

    ITE.py

    This file is part of ANNarchy.

    Copyright (C) 2013-2016  Julien Vitay <julien.vitay@gmail.com>,
    Helge Uelo Dinkelbach <helge.dinkelbach@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    ANNarchy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
from ANNarchy.core.Global import _error, _warning
from ANNarchy.parser.Equation import Equation
from ANNarchy.parser.StringManipulation import *

from pprint import pprint
import re

def translate_ITE(name, eq, condition, description, untouched, split=True):
    " Recursively processes the different parts of an ITE statement"
    def process_condition(condition):
        if_statement = condition[0]
        then_statement = condition[1]
        else_statement = condition[2]

        if_code = Equation(name, if_statement, description,
                          untouched = untouched.keys(),
                          type='cond').parse()
        if isinstance(then_statement, list): # nested conditional
            then_code =  process_condition(then_statement)
        else:
            then_code = Equation(name, then_statement, description,
                          untouched = untouched.keys(),
                          type='return').parse().split(';')[0]
        if isinstance(else_statement, list): # nested conditional
            else_code =  process_condition(else_statement)
        else:
            else_code = Equation(name, else_statement, description,
                          untouched = untouched.keys(),
                          type='return').parse().split(';')[0]

        code = '(' + if_code + ' ? ' + then_code + ' : ' + else_code + ')'
        return code

    if split:
        # Main equation, where the right part is __conditional__
        translator = Equation(name, eq, description,
                              untouched = untouched.keys())
        code = translator.parse()
    else:
        code = eq

    # Process the (possibly multiple) ITE
    for i in range(len(condition)):
        itecode =  process_condition(condition[i])
        # Replace
        if isinstance(code, str):
            code = code.replace('__conditional__'+str(i), itecode)
        else:
            code[0] = code[0].replace('__conditional__'+str(i), itecode)

    return code


def extract_ite(name, eq, description, split=True):
    """ Extracts if-then-else statements and processes them.

    If-then-else statements must be of the form:

    .. code-block:: python

        variable = if condition: ...
                       val1 ...
                   else: ...
                       val2

    Conditional statements can be nested, but they should return only one value!
    """

    def transform(code):
        " Transforms the code into a list of lines."
        res = []
        items = []
        for arg in code.split(':'):
            items.append( arg.strip())
        for i in range(len(items)):
            if items[i].startswith('if '):
                res.append( items[i].strip() )
            elif items[i].endswith('else'):
                res.append(items[i].split('else')[0].strip() )
                res.append('else' )
            else: # the last then
                res.append( items[i].strip() )
        return res


    def parse(lines):
        " Recursive analysis of if-else statements"
        result = []
        while lines:
            if lines[0].startswith('if'):
                block = [lines.pop(0).split('if')[1], parse(lines)]
                if lines[0].startswith('else'):
                    lines.pop(0)
                    block.append(parse(lines))
                result.append(block)
            elif not lines[0].startswith(('else')):
                result.append(lines.pop(0))
            else:
                break
        return result[0]

    # If no if, not a conditional
    if not 'if ' in eq:
        return eq, []

    # Process the equation
    condition = []
    # Eventually split around =
    if split:
        left, right =  eq.split('=', 1)
    else:
        left = ''
        right = eq

    nb_then = len(re.findall(':', right))
    nb_else = len(re.findall('else', right))
    # The equation contains a conditional statement
    if nb_then > 0:
        # A if must be right after the equal sign
        if not right.strip().startswith('if'):
            _error(eq, '\nThe right term must directly start with a if statement.')

        # It must have the same number of : and of else
        if not nb_then == 2*nb_else:
            _error(eq, '\nConditional statements must use both : and else.')

        multilined = transform(right)
        condition = parse(multilined)
        right = ' __conditional__0 ' # only one conditional allowed in that case
        if split:
            eq = left + '=' + right
        else:
            eq = right
    else:
        _print(eq)
        _error('Conditional statements must define "then" and "else" values.\n var = if condition: a else: b')

    return eq, [condition]
