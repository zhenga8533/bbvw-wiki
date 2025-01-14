import keyword
import re


def clean_variable_name(s):
    # Remove invalid characters
    s = s.replace(" ", "_")
    valid_chars = "".join(c if c.isalnum() or c == "_" else "" for c in s)
    # Ensure it doesn't start with a digit
    if valid_chars and valid_chars[0].isdigit():
        valid_chars = "_" + valid_chars
    # Ensure it's not a Python keyword
    if valid_chars in keyword.kwlist:
        valid_chars += "_"
    return valid_chars


def parse_camel_case(s: str) -> str:
    """
    Parse a camel case string into a space separated string.

    :param s: The camel case string to parse.
    :return: The space separated string.
    """

    return re.sub("([a-z])([A-Z])", r"\1 \2", s)
