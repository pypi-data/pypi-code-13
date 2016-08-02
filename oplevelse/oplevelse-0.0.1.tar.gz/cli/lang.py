import click
from oplevelse import oplevelse


@oplevelse.group()
@click.pass_obj
def lang(api):
	"""Language management operations"""


@lang.command()
@click.pass_obj
def list(api):
	for lang in api.lang.list():
		click.echo(lang.get('name'))
