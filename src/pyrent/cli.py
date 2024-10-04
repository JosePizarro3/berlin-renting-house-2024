import json
import os

import click

from pyrent.immoscout24 import ImmoScout24Parser


def get_name_string(json_data: dict) -> str:
    """
    Gets the name string for the JSON data.

    Args:
        json_data (dict): JSON data from the specific parser.

    Returns:
        str: Name string for the JSON data. It follows the format `{scout_id}_{zip_code}_{construction_year}_{total_cold}EUR_{square_meter}m2`.
    """
    zip_code = json_data.get('zip_code', '00000')
    construction_year = json_data.get('construction_year', '0000')
    total_cold = int(json_data.get('price', {}).get('total_cold', 0))
    square_meter = int(json_data.get('square_meter', 0))
    scout_id = json_data.get('scout_id', 0)
    return f'{scout_id}_{zip_code}_{construction_year}_{total_cold}EUR_{square_meter}m2'


def process_pdf(filepath: str) -> dict:
    """
    Helper function to process a single PDF file.

    Args:
        filepath (str): Path to the PDF file.

    Returns:
        dict: JSON data for the parsed PDF file.
    """
    parser = ImmoScout24Parser()
    immoscout_house = parser.parse(filepath=filepath)
    return json.loads(immoscout_house.model_dump_json())


def process_directory(directory: str, save_to_json: bool = False) -> dict:
    """
    Helper function to process all PDFs in a directory recursively.

    Args:
        directory (str): Path to the directory containing PDF files.
        save_to_json (bool, optional): Optional flag to save the data to individual JSON files. Defaults to False.

    Returns:
        dict: Dictionary containing the JSON data for all the parsed PDF files.
    """
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.pdf'):
                full_path = os.path.join(root, file)

                # Extract required attributes
                json_data = process_pdf(filepath=full_path)
                key = get_name_string(json_data=json_data)
                results[key] = json_data

                # Save JSON to a file if the flag is set
                if save_to_json:
                    # Construct the filename based on scout_id and other attributes
                    filepath_to_save = os.path.join(root, f'{key}.json')
                    # Write the JSON data to the file
                    with open(filepath_to_save, 'w', encoding='utf-8') as json_file:
                        json.dump(
                            {key: json_data}, json_file, ensure_ascii=False, indent=4
                        )
    return results


@click.group()
def cli():
    """CLI for parsing real estate PDF files with pyrent."""
    pass


@cli.command()
@click.argument('path')
@click.option('--show-json', is_flag=True, help='Show JSON output in the terminal.')
@click.option('--save-to-json', is_flag=True, help='Save results to JSON files.')
def immoscout24(path: str, show_json: bool, save_to_json: bool) -> None:
    """Parse a PDF file or directory with ImmoScout24 parser."""
    # Individual PDF file
    if os.path.isfile(path):
        json_data = process_pdf(filepath=path)
        key = get_name_string(json_data=json_data)

        if save_to_json:
            filepath_json = os.path.join(os.path.dirname(path), f'{key}.json')
            with open(filepath_json, 'w', encoding='utf-8') as json_file:
                json.dump({key: json_data}, json_file, ensure_ascii=False, indent=4)

        if show_json:
            click.echo(
                json.dumps(json_data, indent=4, ensure_ascii=False)
            )  # Print directly if show_json is True
    # Directory containing PDF files
    elif os.path.isdir(path):
        if show_json:
            # Print the results as a JSON dictionary
            click.echo(
                json.dumps(
                    process_directory(directory=path, save_to_json=save_to_json),
                    indent=4,
                    ensure_ascii=False,
                )
            )  # Print as a dictionary
        else:
            process_directory(directory=path, save_to_json=save_to_json)
    else:
        click.echo('Please provide a valid PDF file or directory.')


if __name__ == '__main__':
    cli()
