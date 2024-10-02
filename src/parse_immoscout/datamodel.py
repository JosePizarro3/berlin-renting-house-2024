from typing import Optional

from pydantic import BaseModel, Field


class ImmoScoutHouse(BaseModel):
    """
    A base model class used to represent a house object offer from ImmoScout24. The information in this model
    is extracted from the PDF generated when printing the web of the offer.
    """

    scout_id: Optional[int] = Field(None, title='Scout ID')
