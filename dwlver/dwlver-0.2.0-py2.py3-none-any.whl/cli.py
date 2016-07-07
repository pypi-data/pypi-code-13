# -*- coding: utf-8 -*-

import click
import ver

@click.command()
def main(args=None):
    """Console script for dwlver"""
    click.echo(ver.version)

if __name__ == "__main__":
    main()
