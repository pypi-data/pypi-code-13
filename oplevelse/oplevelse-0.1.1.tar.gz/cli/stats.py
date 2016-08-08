import click
from oplevelse import oplevelse


@oplevelse.command()
@click.pass_obj
def stats(api):
	"""Show stats"""
	for action, lang in api.stats().items():
		click.echo(action)

		for lang_name, tasks in lang.items():
			click.echo('\t%s' % (lang_name))

			for task_name in tasks:
				click.echo('\t\t%s' % (task_name))
