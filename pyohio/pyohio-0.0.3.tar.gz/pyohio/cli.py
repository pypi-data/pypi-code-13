import click
import dateutil
from datetime import datetime
from pyohio import schedule

@click.group()
@click.option('--verbose', '-v', count=True)
@click.pass_context
def pyohio_cli(ctx, verbose):
    """PyOhio-related tools."""
    ctx.obj = {'verbose': verbose}

@pyohio_cli.command(name='schedule')
@click.option('--remaining', '-r', is_flag=True,
        help='Only sessions that have yet to start')
@click.option('--after',
        help='Only sessions starting after (ex: "2016-07-30 13:30")')
@click.pass_context
def pyohio_schedule(ctx, remaining, after):
    """Output the PyOhio schedule."""

    log('Downloading schedule...')
    schedule_json = schedule.get_schedule()
    if remaining and not after:
        start = datetime.now()
        log('Only returning sessions that have yet to start.')
    elif after:
        start = dateutil.parser.parse(after)
        log('Only returning sessions starting after {0}.'.format(start.isoformat()))
    else:
        start = None

    table_text = schedule.make_table(schedule_json, start_datetime=start)
    click.echo(table_text)

@click.pass_context
def log(ctx, message, verbosity=1):
    """ Output message to stderr if context verbosity >= passed verbosity.

    You'd typically want to incorporate this with a 'real' logger but this is
    good enough for our example.
    """
    verbose_count = ctx.obj.get('verbose')
    if verbose_count >= verbosity:
        click.echo(message, err=True)

if __name__ == '__main__':
    pyohio_cli()
