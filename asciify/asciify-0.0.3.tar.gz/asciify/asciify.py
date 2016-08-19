from word_renderer import WordRenderer
import click

@click.command()
@click.option('--text', help='Text to asciify')
@click.option('--pos', default='X', help='Character that serves as positive space')
@click.option('--neg', default=' ', help='Character that serves as negative space')
def main(text, pos, neg):
	renderer = WordRenderer()
	print renderer.create_rendered_word(text, pos, neg)

if __name__ == '__main__':
	main()