import re
from typing import Any


def extract_data(text: str, pattern: str, type: type[Any] = str) -> Any:
    """
    Extracts data from a `text` using a regular expression `pattern`, and returns the matched group
    converted to the specified data `type`.

    Args:
        text (str): The text to extract data from.
        pattern (str): The regular expression pattern to match
        type (type[Any], optional): The type to return the matched group. Defaults to str.

    Returns:
        Any: The matched group converted to the specified data type.
    """
    match = re.search(pattern, text)
    if match:
        # Try to convert the matched group to the specified data type
        try:
            return type(match.group(1))
        except ValueError:
            return None
    else:
        return None
