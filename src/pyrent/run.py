import os

from pyrent.immoscout24 import ImmoScout24Parser

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


# Parsing ImmoScout24 house offer
immoscout_house = ImmoScout24Parser().parse(filepath=file)

# Print the model as JSON
immoscout_house_json = immoscout_house.model_dump_json(indent=4)
output_json = os.path.join(file_dirname, file_basename.replace('.pdf', '.json'))
with open(output_json, 'w') as f:
    f.write(immoscout_house_json)
