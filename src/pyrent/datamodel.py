from typing import Optional

from pydantic import BaseModel, Field


class Price(BaseModel):
    """
    A base model class used to represent the price of a house offer from ImmoScout24. All the
    prices are given in the units specified in `currency_units`.
    """

    currency_units: str = Field(
        'EUR', title='Currency units used in the prices. Default is EUR.'
    )

    total_cold: Optional[float] = Field(None, title='Total cold rent.')

    extras: Optional[float] = Field(None, title='Additional costs.')

    heating: Optional[float] = Field(None, title='Heating costs.')

    total_warm: Optional[float] = Field(
        None,
        title='Total warm rent. This is obtained after summing `total_cold`+`extras`+`heating`.',
    )

    deposit: Optional[float] = Field(None, title='Security deposit.')

    # parent: Optional['ImmoScoutHouse'] = None


class ImmoScoutHouse(BaseModel):
    """
    A base model class used to represent a house object offer from ImmoScout24. The information in this model
    is extracted from the PDF generated when printing the web of the offer.
    """

    name: str = Field('Unknown', title='Name of the offer as published.')

    scout_id: Optional[int] = Field(None, title='ImmoScout24 ID.')

    address: Optional[str] = Field(None, title='Address of the house.')

    zip_code: Optional[str] = Field(None, title='Zip code of the house.')

    construction_year: Optional[int] = Field(
        None, title='Year of construction of the house.'
    )

    square_meter: Optional[float] = Field(
        None, title='Total square meters of the house.'
    )

    price: Optional[Price] = Field(None, title='The different prices of the house.')

    owner: Optional[str] = Field(
        'unknown',
        title='Owner of the house. It can be a private entity or some specific company (e.g., HOWOGE, Vonovia, etc.).',
    )

    def __setattr__(self, name, value):
        # If the 'price' attribute is being set or modified, update the parent reference
        # if name == 'price' and isinstance(value, Price):
        #     value.parent = self
        super().__setattr__(name, value)
