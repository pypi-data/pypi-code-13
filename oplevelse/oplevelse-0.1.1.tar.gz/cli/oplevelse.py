import click

from api import OplevelseAPI

        
@click.group()
@click.option('--home', default='~/oplevelse', metavar='HOME', help='Changes the oplevelse home folder location.')
@click.option('--api-url', default='http://api.oplevelse.co', metavar='API_URL', help='API server URL.')
@click.option('--token', default='', metavar='OPLEVELSE_TOKEN', help='Auth token.')
@click.option('--config', default='~/.oplevelse.json', metavar='CONFIG', type=click.Path(), help='Config file.')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def oplevelse(ctx, *args, **kwargs):
	ctx.obj = OplevelseAPI(*args, **kwargs)


class NotAuthorized(Exception):
	pass
oplevelse.NotAuthorized = NotAuthorized