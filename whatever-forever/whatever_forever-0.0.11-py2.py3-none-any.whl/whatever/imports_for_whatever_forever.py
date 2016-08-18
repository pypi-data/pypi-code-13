
# coding: utf-8

# # What does `whatever-forever` import?

# In[10]:

info > display.HTML


# > Compare the raw globals to the new ones. 

# In[1]:

defaults = globals().copy()
from whatever import *
now = globals().copy()
from IPython import display


# In[2]:

Forever.cell('template', identity, lang='html')


# In[3]:

from jinja2 import Environment, DictLoader
env = Environment(loader=DictLoader({'panel': '','parent':''}))
Forever.cell('jinja', lambda x: env.from_string(x).render(**globals()), lang='html')


# In[4]:

get_ipython().run_cell_magic('template', 'panel -d', '{% if title %}<div class="panel panel-default">\n    <div class="panel-heading">\n        <h4 class="panel-title">\n            <a data-toggle="collapse" data-parent="#accordion" href="#collapse{{title}}">{{title}}</a>\n        </h4>\n    </div>\n    <div id="collapse{{title}}" class="panel-collapse collapse">\n        <div class="panel-body">\n            {{body}}\n        </div>\n    </div>\n</div>{% endif %}')


# In[5]:

env.loader.mapping['panel'] = panel


# In[6]:

all_the_tools = (_X(now) 
 | keyfilter(lambda x: x not in defaults.keys()) 
 | (this().keys() | list > compose)
)


# In[7]:

def serialize(x):
    try: return {
            'title': x.__name__,
            'body': convert_text(x.__doc__, 'html', 'markdown') if hasattr(x, '__doc__') else "",
        }
    except: pass
    return {}


# In[8]:

from pypandoc import convert_text
template_addons = (
    _X(all_the_tools.f()[0]) | globals().get 
    | serialize | env.get_template('panel').render
)


# In[9]:

info = (_X(all_the_tools.f()) | map(template_addons.f)  | '\n'.join
 | """<div id="accordion" class="panel-group">{}</div>""".format
)


# In[ ]:



