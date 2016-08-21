"""
Created on 06.12.2015.

@author: xx
"""

import os
import codecs

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader



class BaseGenerator:
    model = object

    def __init__(self, model):
        self.model = model
        pass

    def checkType(self, someitem):
        if someitem == 'foreignKey' or someitem == 'oneToOne' or someitem == 'manyToMany':
            return True
        else:
            return False
    
    def choice(self, someitem):
        if someitem == 'choices':
            return True
        else:
            return False

    def generate(self, template_name, output_name, render_vars, output_dir):
        env = Environment(trim_blocks=True, lstrip_blocks=True, loader=PackageLoader("generated", "templates"))
        env.filters["typeDef"] = self.typeDef
        env.filters["annotationdef"] = self.annotationdef
        env.filters["annotation_attribute_def"] = self.annotation_attribute_def
        env.tests["checkType"] = self.checkType
        env.tests["choice"] = self.choice

        template = env.get_template(template_name)
        rendered = template.render(render_vars)

        file_name = os.path.join(output_dir, output_name)
        print(file_name)
        with codecs.open(file_name, "w+", "utf-8") as f:
            f.write(rendered)

    def generate_application(self):
        # placeholder
        base_source_path = os.path.join('play_templates')
