import os

from pypdf import PdfReader

from parse_immoscout.datamodel import ImmoScoutHouse
from parse_immoscout.utils import extract_data

# Filepath definitions
dirname = os.path.dirname(os.path.abspath(__name__))  # dirname of the project locally
data_file = os.path.join(
    'data',
    '6E-sqm',
    'Einbauküche kann übernommen werden - Anmietung zum 01.11.2024 möglich.pdf',
)  # path to file within the project
file = os.path.join(dirname, data_file)  # full local path to file
file_dirname = os.path.dirname(file)  # name of the subfolder where file is located
file_basename = os.path.basename(file)  # name of the file

# Reading PDF
reader = PdfReader(file)

# Scout-ID extraction
last_page_text = reader.pages[-1].extract_text()
scout_id = extract_data(
    text=last_page_text, pattern=r'Scout\-ID\s*\:\s*(\d+)', type=int
)

# Datamodel population
immoscout_house = ImmoScoutHouse(scout_id=scout_id)

# Print the model as JSON
immoscout_house_json = immoscout_house.model_dump_json()
output_json = os.path.join(file_dirname, file_basename.replace('.pdf', '.json'))
with open(output_json, 'w') as f:
    f.write(immoscout_house_json)
