#Global settings for the helloworld app, to be overrided in local_settings.py.
from django.conf.global_settings import *
ROOT_URLCONF='helloworld.config.urls'
ENABLE_BEAKER=False
MEDIA_URL="http://localhost/media/img/"
SECRET_KEY='12345va1110ht'
ENABLE_TIDYLIB=False
TEMPLATE_CONTEXT_PROCESSORS = (
   #'django.core.context_processors.auth',
   #'django.template.context_processors.media',          # MEDIA_URL
   #'django.template.context_processors.request',        # request
   #'mainapp.config.context_processors.settings',    # settings
   #'mainapp.config.context_processors.rss',
   #'mainapp.config.context_processors.hginfo',     # hg version (requires hgtools)
   #'mainapp.config.context_processors.link_set',   # custom link_set obj (dct)
   #'mainapp.config.context_processors.last_mod',   # Page's Last modified Timestamp
   #'blogengine.contrib.addthis.context_processors.addthis_widget', # addthis widget
   #'blogengine.contrib.comments.context_processors.comment_form',  # free comments form
    'helloworld.config.context_processors.request',
    )

