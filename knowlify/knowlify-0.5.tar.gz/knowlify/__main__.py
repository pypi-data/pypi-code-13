import click
import knowlify
import config


@click.command()
@click.argument('filename_or_url', type=click.STRING, default='https://en.wikipedia.org/wiki/Mathematics')
@click.option('-p','path', type=click.STRING, default=None)
def main(filename_or_url, path):
    page = knowlify.get_page(filename_or_url)
    file_path = knowlify.output_page(page, path)
    with knowlify.engine.MicroServerEngine(file_path=file_path) as f:

        f.open_page()
        while True:
            pass

    return None


if __name__ == '__main__':
    main()
