import click

from api import OplevelseAPI

        
@click.group()
@click.option('--oplevelse-home', default='~/oplevelse',
              metavar='HOME', help='Changes the oplevelse home folder location.')
@click.option('--oplevelse-api-server', default='http://127.0.0.1:8000/',
                               metavar='API_URL',
                               help='URL the Oplevelse API server')
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def oplevelse(ctx, oplevelse_home, oplevelse_api_server, debug):
    ctx.obj = OplevelseAPI(oplevelse_home, oplevelse_api_server, debug)