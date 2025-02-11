from util.file import load, verify_asset_path
from util.logger import Logger
import json
import logging
import os
import re
import string


def find_pokemon_sprite(pokemon: str, view: str, logger: Logger) -> str:
    """
    Find the sprite of a Pokémon.

    :param pokemon: Pokémon to find the sprite.
    :param view: View of the sprite.
    :param logger: Logger to log the verification.
    :return: The sprite of the Pokémon.
    """

    # Load Pokemon data
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    pokemon_id = format_id(pokemon)
    sprite = f"../assets/sprites/{pokemon_id}/{view}"
    file_path = POKEMON_INPUT_PATH + pokemon_id + ".json"
    if not os.path.exists(file_path):
        file_path = file_path.replace(pokemon_id, pokemon_id.rsplit("-", 1)[0])
    pokemon_data = json.loads(load(file_path, logger))
    pokemon_text = pokemon_data["flavor_text_entries"].get("white", pokemon).replace("\n", " ")
    name = revert_id(format_id(pokemon))

    return (
        f'![{pokemon}]({sprite}.gif "{name}: {pokemon_text}")'
        if verify_asset_path(sprite + ".gif", logger)
        else (
            f'![{pokemon}]({sprite}.png "{name}: {pokemon_text}")'
            if verify_asset_path(sprite + ".png", logger)
            else "?"
        )
    )


def find_trainer_sprite(trainer: str, view: str, logger: Logger = None) -> str:
    """
    Find the sprite of a trainer.

    :param trainer: Trainer to find the sprite.
    :param view: View of the sprite.
    :param logger: Logger to log the verification.
    :return: The sprite of the trainer.
    """

    words = trainer.split()
    n = len(words)
    subsets = []

    # Iterate through all non-empty subsets
    for i in range(1, 1 << n):
        subset = []
        for j in range(n):
            # Check if the j-th element is in the subset
            if i & (1 << j):
                subset.append(words[j])
        subsets.append(" ".join(subset))
    subsets.sort(key=len, reverse=True)

    # Check if the sprite exists for any subset
    for subset in subsets:
        sprite = f"../assets/{view}/{format_id(subset, symbol="_")}"
        if verify_asset_path(sprite + ".png", logger):
            return f'![{trainer}]({sprite}.png "{trainer}")'

    # Check if the sprite exists for the full name
    if view != "important_trainers":
        return find_trainer_sprite(trainer, "important_trainers", logger)
    return f'![{trainer}](../assets/{view}/{format_id(trainer, symbol="_")}.png "{trainer}")'


def fix_pokemon_id(pokemon_id: str) -> str:
    """
    Fix the Pokemon ID to match the format used in data.

    :param pokemon_id: The Pokemon ID to fix.
    :return: The fixed Pokemon ID.
    """

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


def format_id(name: str, symbol: str = "-", start_index: int = 0) -> str:
    """
    Format a name to be used as an ID.

    :param name: The name to format.
    :param symbol: The symbol to use to separate words.
    :param start_index: The index to start at.
    :return: The formatted ID.
    """

    name = remove_special_characters(name)
    name = re.sub(r"\s+", " ", name).strip()
    name = symbol.join(name.split(" ")[start_index:]).lower()
    name = fix_pokemon_id(name)

    return name


def format_stat(stat: str) -> str:
    """
    Format the name of a stat.

    :param stat: Stat to be formatted.
    :return: Formatted stat.
    """

    stat = format_id(stat)
    if stat == "health" or stat == "hp":
        return "HP"
    elif stat == "attack":
        return "Atk"
    elif stat == "defense":
        return "Def"
    elif stat == "special-attack":
        return "Sp. Atk"
    elif stat == "special-defense":
        return "Sp. Def"
    elif stat == "speed":
        return "Spd"
    else:
        return stat


def revert_id(name: str, symbol: str = "-") -> str:
    """
    Revert an ID to a name.

    :param name: The ID to revert.
    :param symbol: The symbol used to separate words.
    :return: The reverted name.
    """

    return string.capwords(name.replace(symbol, " "))


def remove_special_characters(s: str) -> str:
    """
    Remove special characters from a string.

    :param s: The string to remove special characters from.
    :return: The string without special characters.
    """

    return re.sub(r"[^a-zA-Z0-9\s-]", "", s)


def verify_pokemon_form(id: str, logger: Logger) -> bool:
    """
    Verify if a Pokemon form is valid.

    :param id: The ID of the Pokemon.
    :param logger: The logger to use.
    :return: True if the form is valid, False otherwise.
    """

    pokemon_with_forms = [
        "unown",
        "deoxys",
        "castform",
        "burmy",
        "wormadam",
        "cherrim",
        "shellos",
        "gastrodon",
        "rotom",
        "giratina",
        "shaymin",
        "arceus",
        "basculin",
        "darmanitan",
        "deerling",
        "sawsbuck",
        "tornadus",
        "thundurus",
        "landorus",
        "keldeo",
        "meloetta",
        "genesect",
        "kyurem",
        "darmanitan",
    ]
    illegal_forms = ["white-striped", "galar"]

    # Check if the form is invalid
    for form in illegal_forms:
        if form in id:
            logger.log(logging.DEBUG, f"Illegal form {id}")
            return False

    # Validate if the Pokemon has a form
    for pokemon in pokemon_with_forms:
        if pokemon in id:
            logger.log(logging.DEBUG, f"Valid form {id} for {pokemon}")
            return True

    logger.log(logging.DEBUG, f"Invalid form {id}")
    return False
