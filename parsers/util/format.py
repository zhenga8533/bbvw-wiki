import keyword
import logging
import os
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


def create_image_table(headings: list, images: list, logger):
    table_header = "|"
    table_divider = "|"
    table_body = "|"

    for i in range(len(images[0])):
        # Check if image exists
        image_path = None
        for image in images:
            check_path = image[i].rstrip("../") + "../docs/"
            if os.path.exists(check_path):
                image_path = image[i]
                break
        if image_path is None:
            logger.log(logging.ERROR, f"Image {i} does not exist")
            continue

        table_header += f" {headings[i]} |"
        table_divider += " --- |"
        table_body += f" ![{headings[i]}]({image_path}) |"
    if table_header + table_divider + table_body == "|||":
        return ""

    return f"{table_header}\n{table_divider}\n{table_body}\n\n"


def format_id(pokemon_name: str, start_index: int = 0) -> str:
    """
    Format a Pokémon name to a valid identifier.

    :param pokemon_name: The name of the Pokémon.
    :param start_index: The index to start splitting the Pokémon name.
    :return: The formatted Pokémon name.
    """

    pokemon_name = remove_special_characters(pokemon_name)
    pokemon_name = "-".join(pokemon_name.split(" ")[start_index:]).lower()

    return pokemon_name.lower()


def remove_special_characters(s: str) -> str:
    """
    Remove special characters from a string.

    :param s: The string to remove special characters from.
    :return: The string without special characters.
    """

    return re.sub(r"[^a-zA-Z0-9\s]", "", s)
