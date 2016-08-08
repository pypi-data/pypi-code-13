import os
import json
import click
from oplevelse import oplevelse

@oplevelse.command()
@click.argument('github_token')
@click.pass_obj
def register(api, github_token):
    """Register with Github Personal Access Token

    https://help.github.com/articles/creating-an-access-token-for-command-line-use/
    """
    response = api.login(github_token)
    token = response['token']

    api.persist_token(token)

    click.echo('Oplevelse Token: {}'.format(token))

@oplevelse.command()
@click.argument('oplevelse_token')
@click.pass_obj
def login(api, oplevelse_token):
    """Login with Oplevelse Token

    If you dont have one, run oplevelse register --help
    """
    api.persist_token(oplevelse_token)
