import click
from oplevelse import oplevelse


@oplevelse.group()
@click.pass_obj
def task(api):
	"""Task management operations"""


@task.command()
@click.argument('lang')
@click.pass_obj
def list(api, lang):
	"""List tasks for specified lang"""
	for task in api.task.list(lang):
		click.echo(task.get('name'))

@task.command()
@click.argument('lang')
@click.argument('task')
@click.pass_obj
def fetch(api, lang, task):
	"""Fetch specified task"""
	api.task.get(lang, task)