# -*- coding: utf-8 -*-

import click

from .wcloud import generate_wordcloud


@click.command()
@click.argument('file', type=click.File('r'))
@click.option('--output', '-o', default='wordcloud.png',
              help='Output filename of wordloud image')
@click.option('--bgcolor', '-b', default='black',
              help='Background color of wordcloud (default=\'black\')')
@click.option('--width', '-w', default=600, type=click.INT,
              help='Width of wordcloud image (default=600)')
@click.option('--height', '-h', default=500, type=click.INT,
              help='Height of wordcloud image (default=500)')
@click.option('--max-words', '-x', default=1000, type=click.INT,
              help='The maximum number of words (default=1000)')
@click.option('--mask', '-m', default=None, type=click.File('rb'),
              help='Path to mask image (default=None)')
def main(file, output, bgcolor, width, height, max_words, mask):
    text = ''.join(file.readlines())
    wc = generate_wordcloud(text, bgcolor, width, height, max_words, mask)
    wc.to_file(output)
    click.echo('Wordcloud saved in {}'.format(output))


if __name__ == "__main__":
    main()
