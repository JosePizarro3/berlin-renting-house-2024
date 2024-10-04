from pyrent.datamodel import ImmoScoutHouse, Price
from pyrent.parsing import PDFParser, Quantity


class ImmoScout24PDFParser(PDFParser):
    def _quantities(self) -> list[Quantity]:
        return [
            Quantity(name='name', pattern=r'\n(.*?)\n', type=str),
            Quantity(name='scout_id', pattern=r'Scout\-ID\s*\:\s*(\d+)', type=int),
            Quantity(name='address', pattern=r'Adresse\n([\w\,\s]+)Wohnung', type=str),
            # ! adding `Wonhfläche` to the pattern is not working, probably due to an issue reading the PDF
            Quantity(
                name='square_meter', pattern=r'äche *ca\.\:\s*([\d\,]+)\s*m', type=float
            ),
            Quantity(
                name='construction_year', pattern=r'Baujahr[\s\:]*(\d+)', type=int
            ),
            Quantity(
                name='total_cold', pattern=r'Kaltmiete\:\s*([\d\,]+)\s*\€', type=float
            ),
            Quantity(
                name='extras', pattern=r'Nebenkosten\:[\s\+]*([\d\,]+)\s*\€', type=float
            ),
            Quantity(
                name='heating', pattern=r'Heizkosten\:[\s\+]*([\d\,]+)\s*\€', type=float
            ),
            Quantity(
                name='deposit',
                pattern=r'Kaution o\.\nGenossenschafts anteile\s*\:\s*([\d\.]+)',
                type=float,
            ),
        ]


class ImmoScout24Parser:
    def parse(self, filepath: str):
        pdf_parser = ImmoScout24PDFParser(mainfile=filepath)
        data = pdf_parser.parsed_data()

        immoscout_house = ImmoScoutHouse()
        for key in ['name', 'scout_id', 'address', 'square_meter', 'construction_year']:
            setattr(immoscout_house, key, data.get(key))

        price = Price()
        for key in ['total_cold', 'extras', 'heating', 'deposit']:
            setattr(price, key, data.get(key))
        try:
            price.total_warm = price.total_cold + price.extras + price.heating
        except ValueError:
            pass
        immoscout_house.price = price

        return immoscout_house
