import click


def heading(headline):
    click.secho(headline, bold=True)
    click.secho('='*len(headline), bold=True)


def pretty_print_object(obj, headline=None):
    if headline:
        heading(headline)
    for key, value in obj.items():
        print('{}: {}'.format(key, value))
