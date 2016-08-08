import click
from oplevelse import oplevelse


@oplevelse.command()
@click.pass_obj
def langs(api):
	"""List available langs"""
	for lang in api.lang_list():
		click.echo(lang.get('name'))
