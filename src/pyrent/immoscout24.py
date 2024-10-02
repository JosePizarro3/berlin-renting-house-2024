import os

from pypdf import PdfReader

from pyrent.datamodel import ImmoScoutHouse, Price
from pyrent.utils import extract_data, extract_data_comma

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
full_text = ''
for page in reader.pages:
    full_text += f'{page.extract_text()} '
immoscout_house = ImmoScoutHouse()

## General metadata
# Offer name
immoscout_house.name = reader.metadata.title
# Scout-ID extraction
scout_id = extract_data(text=full_text, pattern=r'Scout\-ID\s*\:\s*(\d+)', type=int)
immoscout_house.scout_id = scout_id
# Address
address = extract_data(text=full_text, pattern=r'Adresse\n([\w\,\s]+)Wohnung', type=str)
immoscout_house.address = address
# m2
# ! `r'Wohnfläche'` in the regex does not work (probably due to a problem with PDFReader)
sqm = extract_data_comma(text=full_text, pattern=r'äche *ca\.\:\s*([\d\,]+)\s*m')
immoscout_house.square_meter = sqm

## Price
price = Price()
# Kaltmiete
total_cold = extract_data_comma(text=full_text, pattern=r'Kaltmiete\:\s*([\d\,]+)\s*\€')


# Print the model as JSON
immoscout_house_json = immoscout_house.model_dump_json()
output_json = os.path.join(file_dirname, file_basename.replace('.pdf', '.json'))
with open(output_json, 'w') as f:
    f.write(immoscout_house_json)
