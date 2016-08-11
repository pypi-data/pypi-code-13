#!/usr/bin/env python3
import click
from d_clean import tasks


HELP_ALL = """Run stopped, images-not-in-use, dangling"""
HELP_STOPPED = """Remove all stopped containers"""
HELP_NOT_IN_USE = """Remove all images not in use"""
HELP_DANGLING = """Remove all dangling images"""


@click.group(help='')
def cli():
    pass


@click.command('all', help=HELP_ALL)
@click.option('-d', '--dry-run', default=False, is_flag=True)
def clean_all(dry_run):
    tasks.clean_all(dry_run=dry_run)


@click.command('stopped', help=HELP_STOPPED)
@click.option('-d', '--dry-run', default=False, is_flag=True)
def clean_stopped(dry_run):
    tasks.clean_stopped_containers(dry_run=dry_run)


@click.command('images-not-in-use', help=HELP_NOT_IN_USE)
@click.option('-d', '--dry-run', default=False, is_flag=True)
def clean_images_not_in_use(dry_run):
    tasks.clean_images_not_in_use(dry_run=dry_run)


@click.command('dangling', help=HELP_DANGLING)
@click.option('-d', '--dry-run', default=False, is_flag=True)
def clean_images_dangling(dry_run):
    tasks.clean_dangling_images(dry_run=dry_run)


cli.add_command(clean_all)
cli.add_command(clean_stopped)
cli.add_command(clean_images_not_in_use)
cli.add_command(clean_images_dangling)


if __name__ == '__main__':
    cli()
