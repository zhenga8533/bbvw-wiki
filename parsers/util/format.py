from util.file import verify_asset_path
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
            if verify_asset_path(image[i], logger):
                image_path = image[i]
                break
        if image_path is None:
            logger.log(logging.WARNING, f"Image {i} does not exist")
            continue

        table_header += f" {headings[i]} |"
        table_divider += " --- |"
        table_body += f" ![{headings[i]}]({image_path}) |"
    if table_header + table_divider + table_body == "|||":
        return ""

    return f"{table_header}\n{table_divider}\n{table_body}\n\n"


def fix_pokemon_id(pokemon_id: str) -> str:
    fix_map = {
        "basculin": "basculin-red-striped",
        "darmanitan": "darmanitan-standard",
        "keldeo": "keldeo-ordinary",
        "meloetta": "meloetta-aria",
        "deoxys": "deoxys-normal",
        "shaymin": "shaymin-land",
        "tornadus": "tornadus-incarnate",
        "thundurus": "thundurus-incarnate",
        "landorus": "landorus-incarnate",
        "giratina": "giratina-altered",
        "wormadam": "wormadam-plant",
    }

    if pokemon_id in fix_map:
        return fix_map[pokemon_id]
    return pokemon_id


def format_id(name: str, start_index: int = 0) -> str:
    name = remove_special_characters(name)
    name = "-".join(name.split(" ")[start_index:]).lower()
    name = fix_pokemon_id(name)

    return name


def remove_special_characters(s: str) -> str:
    """
    Remove special characters from a string.

    :param s: The string to remove special characters from.
    :return: The string without special characters.
    """

    return re.sub(r"[^a-zA-Z0-9\s-]", "", s)
