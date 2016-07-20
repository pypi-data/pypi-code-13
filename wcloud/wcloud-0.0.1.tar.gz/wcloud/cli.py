# -*- coding: utf-8 -*-

import click

from .wcloud import clean_text, generate_wordcloud


@click.command()
@click.argument('file', type=click.File('rb'))
@click.option('--output', '-o', default='wordcloud.png',
              help='Output filename')
def main(file, output):
    text = b''.join(file.readlines())
    text = clean_text(text)
    wc = generate_wordcloud(text)
    wc.to_file(output)
    click.echo('Wordcloud saved in {}'.format(output))


if __name__ == "__main__":
    main()
