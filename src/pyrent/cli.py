import os

import click

from pyrent.immoscout24 import ImmoScout24Parser


def process_pdf(filepath):
    """Helper function to process a single PDF."""
    parser = ImmoScout24Parser()
    immoscout_house = parser.parse(filepath=filepath)
    click.echo(immoscout_house.model_dump_json(indent=4))


def process_directory(directory):
    """Helper function to process all PDFs in a directory recursively."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                full_path = os.path.join(root, file)
                click.echo(f'Found PDF: {full_path}')
                process_pdf(full_path)


@click.group()
def cli():
    """CLI for parsing real estate PDF files with pyrent."""
    pass


@cli.command()
@click.argument('path')
def immoscout24(path):
    """Parse a PDF file or directory with ImmoScout24 parser."""
    if os.path.isfile(path):
        click.echo(f'Parsing file: {path}')
        process_pdf(path)
    elif os.path.isdir(path):
        click.echo(f'Parsing all PDFs in directory: {path}')
        process_directory(path)
    else:
        click.echo('Please provide a valid PDF file or directory.')


@cli.command()
@click.argument('path')
def immowelt(path):
    """Parse a PDF file or directory with Immowelt parser."""
    click.echo('We have not developed a parser for Immowelt data yet!')


if __name__ == '__main__':
    cli()
