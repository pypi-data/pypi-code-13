import click


@click.group()
def cli():
    pass


@cli.command()
def sync():
    """
    Send books to kindle from pc.
    """
    click.echo('Sync downloads and send them to kindle.')

    # watch for new files
    # move to dest
    # send mail
