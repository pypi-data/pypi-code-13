import click
import json

import axsemantics

from .common import CliData, pass_data


@click.group()
@click.option('--login', '-l', help='login email', prompt=True, envvar='AXSEMANTICS_LOGIN')
@click.option('--password', '-p', help='login password',
              prompt=True, hide_input=True, envvar='AXSEMANTICS_PASSWORD')
@click.pass_context
def cli(ctx, login, password):
    ctx.obj = {}
    ctx.obj['login'] = login
    ctx.obj['password'] = password
    axsemantics.login(login, password)


# from .excel_upload import excel
# cli.add_command(excel)

from .content_project import content_project
cli.add_command(content_project)

from .training import training
cli.add_command(training)
