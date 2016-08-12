import markdown
from markdown.extensions.toc import slugify

def lang_slugify(lang):
    def l_slugify(value, separator):
        return slugify(lang + "__" + value, separator)
    return l_slugify

def get_markdown(md_file, lang, table_of_content):
    with open(md_file, "r") as f:
        text = f.read()

    return markdown.markdown(
        text=text,
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
                'title': table_of_content,
                'slugify': lang_slugify(lang)
            }
        })


print("<p><a href='#lang-en'>Documenation in english</a></p>")
print("<p><a href='#lang-fr'>Documenation en Français</a></p>")
print("<p><a href='#lang-bottom'>Bottom of documentation</a></p>")
print("<hr id='lang-en'/>")
print(get_markdown("documentation_en.md", "en", "Table of contents"))
print("<hr id='lang-fr'/>")
print(get_markdown("documentation_fr.md", "fr", "Sommaire"))
print("<hr id='lang-bottom' style='visibility: hidden' />")
