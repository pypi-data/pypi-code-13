"""
ccli/commands/

This module contains the different CLI commands for this project.
"""
import click

from .company import company


####################################################################################################
# Main CLI Group

@click.group()
def cli():
    pass


####################################################################################################
# Add subgroups to group "cli"

cli.add_command(company)
