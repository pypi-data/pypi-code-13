from .jdlinker import javadoc_role

__version = '1.0.6'


def setup(app):
    app.info('Initializing sphinx-JDLinker version ' + __version + '!')
    app.add_role('javadoc', javadoc_role)
    app.add_config_value('javadoc_links', [], 'env')
    app.add_config_value('javadoc_dump', False, 'env')
    # If it was set to true, initially wipe the file, or create it if necessary.
    if app.config.javadoc_dump:
        open('javadoc_dump.txt', 'w').close()
    return {'version': __version}
