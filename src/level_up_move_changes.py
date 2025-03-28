from dotenv import load_dotenv
from util.file import load, save
from util.format import find_pokemon_sprite, format_id
from util.logger import Logger
from util.move import get_move
import glob
import json
import logging
import os
import re


def main():
    """
    Parse the level up move changes content and save it as a Markdown file.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    MOVE_INPUT_PATH = os.getenv("MOVE_INPUT_PATH")
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    logger = Logger("Level Up Move Changes Parser", f"{LOG_PATH}level_up_move_changes.log", LOG)
    content = load(f"{INPUT_PATH}Level Up Move Changes.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = False
    curr_pokemon = None
    move_changes = {}

    # Parse the content
    logger.log(logging.INFO, "Parsing Level Up Move Changes content")
    for i in range(n):
        line = lines[i].strip()
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "":
            if listing:
                md += "```\n\n"
                listing = False
        # Pokémon
        elif line.startswith("#"):
            name = format_id(line, start_index=1)
            md += f"**[{line}](../pokemon/{name}.md/)**\n\n"
            pokemon_sprite = find_pokemon_sprite(name, "front", logger)
            md += pokemon_sprite + "\n\n```\n"

            curr_pokemon = format_id(line, start_index=1)
            listing = True
        # Region header
        elif line.endswith("Pokémon"):
            md += f"---\n\n## {line}\n\n"
        # General changes and key
        elif line == "Key" or line == "General Attack Changes":
            md += f"---\n\n## {line}\n\n```\n"
            listing = True
        # General changes list
        elif line.startswith("• "):
            match = re.match(r"• (.+) is now (\d+) power\.", line)
            md += f"{line}\n"

            if match:
                move_name, power = match.groups()
                logger.log(logging.DEBUG, f"Updating move {move_name} to power {power}")
                move_name = format_id(move_name)

                try:
                    move_path = f"{MOVE_INPUT_PATH + move_name}.json"
                    move_data = get_move(move_name)
                    move_data["power"] = int(power)
                    save(move_path, json.dumps(move_data, indent=4), logger)
                except:
                    continue
        # Move changes
        elif curr_pokemon is not None:
            if curr_pokemon in move_changes:
                move_changes[curr_pokemon].append(line)
            else:
                move_changes[curr_pokemon] = [line]
            md += f"{line}\n"
        # Misc changes
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"
    logger.log(logging.INFO, "Level Up Move Changes parsed successfully!")

    # Adjust current moveset
    logger.log(logging.INFO, "Adjusting Pokémon movesets")
    for key in move_changes:
        file_pattern = f"{POKEMON_INPUT_PATH + key}*.json"
        files = glob.glob(file_pattern)

        # Loop through each Pokémon file
        for file_path in files:
            pokemon_data = json.loads(load(file_path, logger))
            moves = pokemon_data["moves"].get("black-white", None)
            if moves is None:
                continue

            # Loop through each move change and adjust the moveset
            for line in move_changes[key]:
                parts = line.split(" ")
                level = int(parts[2])
                name = " ".join(parts[4:])
                id = format_id(name)
                move_index = next(
                    (
                        i
                        for i, move in enumerate(moves)
                        if move["name"] == format_id(name) and move["learn_method"] == "level-up"
                    ),
                    None,
                )

                # Add move to learnset
                if line.startswith("+"):
                    logger.log(logging.DEBUG, f"Adding move {name} at level {level} for {key} (+)")

                    # Replace move if it already exists
                    if move_index is not None:
                        moves[move_index]["level_learned_at"] = level
                        moves[move_index]["learn_method"] = "level-up"
                        logger.log(logging.DEBUG, f"Updated move {name} to level {level} for {key}")
                    # Add move to learnset if it doesn't exist
                    else:
                        moves.append({"name": id, "level_learned_at": level, "learn_method": "level-up"})
                        logger.log(logging.DEBUG, f"Added move {name} at level {level} for {key}")
                # Remove move from learnset
                elif line.startswith("-"):
                    logger.log(logging.DEBUG, f"Replacing move at level {level} for {key} (-)")
                    replace_index = next(
                        (i for i, move in enumerate(moves) if move["level_learned_at"] == level), None
                    )

                    # Replace move if it exists
                    if replace_index is not None:
                        moves[replace_index]["name"] = name
                        moves[replace_index]["learn_method"] = "level-up"
                        logger.log(logging.DEBUG, f"Replaced move at level {level} with {name} for {key}")
                    # Add move to learnset if it doesn't exist
                    else:
                        logger.log(logging.DEBUG, f"Could not find move at level {level} for {key}")
                elif line.startswith("="):
                    logger.log(logging.DEBUG, f"Updating move {name} to level {level} for {key} (=)")

                    # Update move if it exists
                    if move_index is not None:
                        moves[move_index]["level_learned_at"] = level
                        logger.log(logging.DEBUG, f"Updated move {name} to level {level} for {key}")
                    # Add move to learnset if it doesn't exist
                    else:
                        logger.log(logging.DEBUG, f"Could not find move {name} for {key}")

            save(file_path, json.dumps(pokemon_data, indent=4), logger)
    logger.log(logging.INFO, "Pokémon movesets adjusted successfully!")

    save(f"{OUTPUT_PATH}level_up_move_changes.md", md, logger)


if __name__ == "__main__":
    main()
