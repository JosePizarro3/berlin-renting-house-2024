import re
from abc import ABC, abstractmethod
from typing import Any

from pypdf import PdfReader


class Quantity:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', '')
        self.pattern = kwargs.get('pattern', r'')
        self.type = kwargs.get('type', str)


class PDFParser(ABC):
    def __init__(self, **kwargs):
        self.mainfile = kwargs.get('mainfile', '')
        if not self.mainfile:
            raise ValueError(
                'A PDF `mainfile` must be provided during class instantiation.'
            )
        # Reading the PDF file
        reader = PdfReader(self.mainfile)
        full_text = ''
        for page in reader.pages:
            full_text += f'{page.extract_text()} '
        self.full_text = full_text

    def extract_data(self, pattern: str, type: type[Any] = str) -> Any:
        data = None
        match = re.search(pattern, self.full_text, re.DOTALL)
        if match:
            # Try to convert the matched group to the specified data type
            try:
                # If the data has a comma instead of a point to specify the decimals
                if type is float:
                    data = float(match.group(1).replace(',', '.'))
                else:
                    data = type(match.group(1))
            except ValueError:
                data = None
        return data

    @abstractmethod
    def _quantities(self) -> list[Quantity]:
        return []

    def parsed_data(self) -> dict:
        quantities = self._quantities()
        data = {}
        for quantity in quantities:
            data[quantity.name] = self.extract_data(
                pattern=quantity.pattern, type=quantity.type
            )
        return data
