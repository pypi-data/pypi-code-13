# -*- coding: utf-8 -*-
import click

from .models import Analysis, Sample


@click.command()
@click.argument('analysis_id')
@click.pass_context
def delete(context, analysis_id):
    """Delete analysis from database."""
    old_analysis = Analysis.query.get(analysis_id)
    if old_analysis:
        old_analysis.delete()
        context.obj['db'].commit()
    else:
        context.abort()


@click.command()
@click.option('-l', '--limit', default=10)
@click.argument('sample_id', required=False)
@click.pass_context
def show(context, limit, sample_id):
    """Show samples as JSON objects."""
    if sample_id:
        samples = Sample.query.filter_by(id=sample_id)
    else:
        samples = Sample.query.limit(limit)
    for sample in samples:
        click.echo(sample.to_json(pretty=True))
