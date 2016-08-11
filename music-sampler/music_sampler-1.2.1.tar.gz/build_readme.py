import markdown

html = markdown.markdownFromFile(
        input="documentation_fr.md",
        extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.tables'
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'noclasses': True,
            },
            'markdown.extensions.toc': {
                'title': 'Sommaire'
            }
        })
