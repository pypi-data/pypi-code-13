"""
ccli/commands/company/

This module contains the CLI commands in the group "company".
"""
import click

from .get import get


####################################################################################################
# CLI Group "company"

@click.group()
def company():
    pass


####################################################################################################
# Add commands to group "company"

company.add_command(get)
