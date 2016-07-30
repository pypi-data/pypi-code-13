from wagtail.wagtailcore import hooks
from django.contrib.staticfiles.templatetags.staticfiles import static

@hooks.register('insert_global_admin_js')
def enqueue_plugin_scripts():
    scripts = {}
    for hook in hooks.get_hooks('enqueue_scripts'):
        scripts.update(hook())

    HTML = '\n'.join([
        '<script src="{}"></script>'.format(
            static(meta['source'])
        ) for handle, meta in scripts.items()
    ])

    return HTML

@hooks.register('insert_global_admin_css')
def enqueue_plugin_styles():
    styles = {}
    for hook in hooks.get_hooks('enqueue_styles'):
        styles.update(hook())

    HTML = '\n'.join([
        '<link rel="stylesheet" href="{}">'.format(
            static(meta['source'])
        ) for handle, meta in styles.items()
    ])

    return HTML
