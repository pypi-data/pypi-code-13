# -*- coding: utf-8 -*-
from lektor.pluginsystem import Plugin
from markupsafe import Markup

SCRIPT = '''
<!-- Google Tag Manager -->
<noscript><iframe src="//www.googletagmanager.com/ns.html?id={google_tag_manager_id}"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'//www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
}})(window,document,'script','dataLayer','{google_tag_manager_id}');</script>
<!-- End Google Tag Manager -->
'''

class GoogleTagManagerPlugin(Plugin):
    name = u'Google Tag Manager'
    description = u'Adds support for Google Tag Manager to Lektor CMS'

    def on_setup_env(self):
        google_tag_manager_id = self.get_config().get('GOOGLE_TAG_MANAGER_ID')

        if google_tag_manager_id is None:
            raise RuntimeError('GOOGLE_TAG_MANAGER_ID is not configured. '
                               'Please configure it in '
                               '`./configs/google-tag-manager.ini` file')

        def google_tag_manager():
            return Markup(SCRIPT.format(google_tag_manager_id=google_tag_manager_id))

        self.env.jinja_env.globals['generate_google_tag_manager'] = google_tag_manager
