from setuptools import setup

setup(
    name='lektor-preview-markdown',
    version='0.1',
    description='Adds filter to trim a Markdown post to a specified length.',
    author=u'Brian Cappello',
    author_email='briancappello@gmail.com',
    url='https://github.com/briancappello/lektor-preview-markdown.git',
    license='MIT',
    py_modules=['lektor_preview_markdown'],
    entry_points={
        'lektor.plugins': [
            'preview-markdown = lektor_preview_markdown:PreviewMarkdownPlugin',
        ]
    }
)
