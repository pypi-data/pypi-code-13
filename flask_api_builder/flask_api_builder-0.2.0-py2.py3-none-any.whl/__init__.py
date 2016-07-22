"""
A really simple app that allows you to write out your RESTful API's spec
in a logical form and automatically generate the necessary boilerplate.`
"""

__version__ = '0.2.0'
__all__ = [
        'MalformedParameterWarning',
        'Function',
        'APIGenerator',
        'make_api',
        'parse_spec',
        'Rule',
]


from collections import namedtuple
import re
import warnings
import jinja2


class MalformedParameterWarning(Warning):
    """
    A warning printed when the parser thinks that a user wrote a malformed
    parameter.
    """


Rule = namedtuple('Rule', ('method', 'url', 'description', 'name'))

FUNCTION_TEMPLATE = jinja2.Template('''
@{{ blueprint }}.route('{{ url }}', methods=['{{ method|default('GET') }}'])
def {{ name }}({{ args_list|join(', ') }}):
    """
    {{ docstring }}
    """
    # TODO: Complete me!
    raise NotImplemented''')

PREAMBLE_TEMPLATE = jinja2.Template("""
from flask import Blueprint, jsonify

{{ blueprint }} = Blueprint({{ bp_args|join(', ') }})
""")

ERROR_HANDLER_TEMPLATE = jinja2.Template("""
@{{ blueprint }}.errorhandler(404)
def page_not_found(error):
    response = jsonify({'error': 'not found'})
    response.status_code = 404
    return response

@{{ blueprint }}.errorhandler(500)
def server_error(error):
    response = jsonify({'error': 'server error'})
    response.status_code = 500
    return response
""")


def _is_true(string):
    """
    Check if something is truthy.
    """
    return str(string.lower().strip()) in ['true', '1', 'yes', 'y']


class Function:
    """
    The class in charge of extracting all arguments from the url, generating
    a default name (if necessary), and rendering an individual REST endpoint
    function for Flask.
    """
    def __init__(self, url, method, description, blueprint='api',
                 name=None, template=None):
        self.url = url
        self.method = method.upper()
        self.description = description
        self.blueprint = blueprint
        self.name = name or None
        self.template = template or FUNCTION_TEMPLATE

    def get_args(self):
        """
        Find all the arguments in the url. These are usually bits
        that look like "<int:task_id>" and so on...
        """
        parameters = re.findall(r'<(?:[\w_]+:)?([\w_]+)>', self.url)

        if (self.url.count('<') != len(parameters) or
                self.url.count('<') != len(parameters)):
            warnings.warn(
                'The number of "<" or ">" is different from the number of '
                'parameters found. Make sure parameters look like '
                '"<int:task_id>"',
                MalformedParameterWarning)

        return parameters

    def generate_name(self, args):
        """
        Try to create a stock name for the function given the information
        provided.

        The idea is to create names like the following:
        * get_tasks
        * get_tasks_by_id
        * delete_task_by_id

        Most of the time you'll probably get gibberish, but there's a reason
        you are given the option of specifying a name in your spec.
        """
        name = []
        name.append(self.method.lower())

        # Get the last "word" in the url that isn't a parameter
        for word in reversed(self.url.split('/')):
            if '<' in word or '>' in word:
                continue
            else:
                name.append(word)
                break

        # If there are any arguments, then add "by_[last arg]"
        if args:
            name.append('by')
            name.append(args[-1])

        return '_'.join(name)

    def render(self):
        """
        Render the template given the information we already have.
        """
        args = self.get_args()
        name = self.name or self.generate_name(args)

        func = self.template.render(
            blueprint=self.blueprint,
            url=self.url,
            method=self.method,
            name=name,
            args_list=args,
            docstring=self.description)
        return func

    def __repr__(self):
        return '<{}: url="{}" method="{}">'.format(
            self.__class__.__name__,
            self.url,
            self.method)



class APIGenerator:
    """
    The generator which will render both the preamble and all the functions,
    then join it all together into one string.
    """
    def __init__(self, config, function_template=None):
        self.config = config
        self.blueprint = config.get('blueprint-name', 'api')
        self.rules = self.config['rules']
        self.function_template = function_template

    def preamble(self):
        """
        Generate the import statements and the blueprint definition.
        """
        bp_args = []
        bp_args.append(repr(self.blueprint))
        bp_args.append('__name__')

        if 'prepend-with' in self.config:
            bp_args.append('url_prefix="{}"'.format(self.config['prepend-with']))

        return PREAMBLE_TEMPLATE.render(blueprint=self.blueprint,
                                        bp_args=bp_args)

    def functions(self):
        """
        Turn each of the function "Rules" into their corresponding Function
        representations.
        """
        funcs = []
        for rule in self.rules:
            func = Function(
                rule.url,
                rule.method.upper(),
                rule.description,
                blueprint=self.blueprint,
                name=rule.name,
                template=self.function_template)
            funcs.append(func)
        return funcs

    def error_handlers(self):
        """
        Make a couple useful error handler routes for the user.
        """
        return ERROR_HANDLER_TEMPLATE.render(blueprint=self.blueprint)


    def render(self):
        """
        Generate our API file.
        """
        lines = []

        # Add the preamble
        lines.append(self.preamble())

        # Give it a bit of space
        lines.append('')
        lines.append('')

        if _is_true(self.config.get('error-handlers', 'true')):
            # Add the error handlers
            lines.append(self.error_handlers())

            # Give it a bit of space
            lines.append('')
            lines.append('')

        lines.extend(f.render()+'\n' for f in self.functions())

        return '\n'.join(lines).strip()


def parse_spec(spec):
    """
    Parse a spec line by line and create a config dictionary from the results.

    The parser will go through each line, splitting them wherever there are
    2 or more whitespace characters next to each other.

    Depending on the number of fields in the resulting list, the parser will
    populate the config dictionary accordingly.

    If there is only one field, assume that the user has provided some sort
    of assignment in the form "key: value", split on the ":" and then
    add the resulting key/value pair to the dictionary.

    If there are 3 fields, assume they are [METHOD, URL, DESCRIPTION] and
    add the corresponding rule to the dictionary.

    If there are 4 fields, assume they are [METHOD, URL, DESCRIPTION, NAME]
    and add the corresponding rule to the dictionary.

    Otherwise there is a syntax error.
    """
    config = {}
    config['rules'] = []

    for i, line in enumerate(spec.splitlines()):
        # Remove trailing whitespace
        line = line.strip()

        # Skip comments and empty lines
        if line.startswith('#') or not line:
            continue

        # Split by multiple space sections
        groups = re.split(r'\s\s+', line)

        if len(groups) == 1:
            # It's an option
            left, right = groups[0].split(':')

            # If it fails, throw syntax error
            config[left.strip().lower()] = right.strip()
        elif len(groups) == 3:
            method, url, description = groups
            new_rule = Rule(method, url, description, None)
            config['rules'].append(new_rule)
        elif len(groups) == 4:
            method, url, description, name = groups
            new_rule = Rule(method, url, description, name)
            config['rules'].append(new_rule)
        else:
            raise SyntaxError('Too many fields on line {}'.format(i+1))

    return config


def make_api(spec):
    """
    Given a spec, parse the spec, make the API generator, and then render
    an API for the user.
    """
    cfg = parse_spec(spec)
    generator = APIGenerator(cfg)
    return generator.render().strip()
