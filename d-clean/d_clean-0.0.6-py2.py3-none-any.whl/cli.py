#!/usr/bin/env python3
import click
from d_clean import tasks


HELP_ALL = """Run stopped, images-not-in-use, volumes-not-in-use, dangling"""
HELP_STOPPED = """Remove all stopped containers"""
HELP_IMAGES = """Remove all images not in use and dangling"""
HELP_VOLUMES = """Remove all volumes not in use"""


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


@click.command('images', help=HELP_IMAGES)
@click.option('-d', '--dry-run', default=False, is_flag=True)
def clean_images(dry_run):
    tasks.clean_images_not_in_use(dry_run=dry_run)
    tasks.clean_dangling_images(dry_run=dry_run)


@click.command('volumes', help=HELP_VOLUMES)
@click.option('-d', '--dry-run', default=False, is_flag=True)
def clean_volumes(dry_run):
    tasks.clean_volumes_not_in_use(dry_run=dry_run)


cli.add_command(clean_all)
cli.add_command(clean_stopped)
cli.add_command(clean_images)
cli.add_command(clean_volumes)


if __name__ == '__main__':
    cli()
