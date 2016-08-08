import re
import os
import click
from oplevelse import oplevelse


@oplevelse.command()
@click.argument('lang')
@click.pass_obj
def tasks(api, lang):
	"""List tasks for a given lang"""
	for task in api.task_list(lang):
		click.echo(click.style(task.get('name'), bold=True))
		click.echo(task.get('goal'))

@oplevelse.command()
@click.argument('lang')
@click.argument('task')
@click.pass_obj
def fetch(api, lang, task):
	"""Fetch the task"""
	api.task_get(lang, task)

class FileWrapper():
	def __init__(self, home, file):
		self.file = file
		self.path = os.path.realpath(file.name)

		home_rel = os.path.relpath(self.path, home)
		match = re.match(r'^([\w-]+)\/([\w-]+)\/.*$', home_rel)
		
		self.lang, self.task = match.group(1), match.group(2)
		self.rel = os.path.relpath(self.path, os.path.join(home, self.lang, self.task))

def validate_solution(ctx, param, files):
	for file in files:
		if os.path.commonprefix([os.path.realpath(file.name), ctx.obj.home]) != ctx.obj.home:
			raise click.BadParameter('Can\'t upload %s, ensure the file is in oplevelse HOME dir' % (file.name, ))
		elif 'test' in file.name:
			raise click.BadParameter('Uploading of test files is not supported by now')
	
	files = [FileWrapper(ctx.obj.home, file) for file in files]

	if len(set(['%s.%s' % (file.lang, file.task) for file in files])) > 1:
		raise click.BadParameter('All files must belong to the same lang and task')

	return files[0].lang, files[0].task, files

@oplevelse.command()
@click.argument('solutions', type=click.File('rb'), nargs=-1, callback=validate_solution)
@click.pass_obj
def submit(api, solutions):
	"""Submit the task"""

	lang, task, files = solutions

	try:
		api.submit(lang, task, files)
	except oplevelse.NotAuthorized as e:
		click.echo(click.style('Not Authorized', fg='red'), err=True)
		click.echo(click.style('Run oplevelse auth login first', fg='red'), err=True)
