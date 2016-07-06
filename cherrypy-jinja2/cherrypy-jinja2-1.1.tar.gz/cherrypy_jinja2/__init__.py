#   Copyright 2015-2016 University of Lancaster
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import cherrypy

import jinja2


class Jinja2Tool(cherrypy.Tool):
    def __init__(self, point='before_handler', name=None, priority=30):
        self._point = point
        self._name = name
        self._priority = priority

        self._environments = {}

    def callable(self, search_path, template):
        environment = self._environments.get(search_path, None)

        if not environment:
            environment = jinja2.Environment(
                loader=jinja2.FileSystemLoader(search_path))
            self._environments[search_path] = environment

        template_name = template

        template = environment.get_or_select_template(template_name)

        inner_handler = cherrypy.serving.request.handler

        def wrapper(*args, **kwargs):
            context = inner_handler(*args, **kwargs)
            response = template.render(context)
            return response

        cherrypy.serving.request.handler = wrapper


def install_tool():
    cherrypy.tools.jinja2 = Jinja2Tool()
