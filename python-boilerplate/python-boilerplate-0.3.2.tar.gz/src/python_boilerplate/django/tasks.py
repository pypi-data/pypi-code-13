from invoke import run, task


@task
def reset_migrations(keep_data=False):
    """
    Remove all migration files. If --keep-data is set, it does not remove
    migrations named as XXXX_data_*.py.
    """

    import os

    for x in os.walk(os.getcwd()):
        print(x)