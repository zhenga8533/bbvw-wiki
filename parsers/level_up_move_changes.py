from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import glob
import json
import logging
import os
import re


def main():
    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    MOVES_PATH = os.getenv("MOVES_PATH")
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
            md += f"**{line}**\n\n"
            name = format_id(" ".join(line.split(" ")[1:]))
            md += f"![{name}](../assets/sprites/{name}/front.gif)\n\n```\n"

            curr_pokemon = format_id(line, 1)
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
            if match:
                move_name, power = match.groups()
                logger.log(logging.DEBUG, f"Updating move {move_name} to power {power}")
                move_name = format_id(move_name)

                try:
                    move_path = f"{MOVES_PATH}{move_name}.json"
                    move_data = json.loads(load(move_path, logger))
                    move_data["power"] = int(power)
                    save(move_path, json.dumps(move_data, indent=4), logger)
                except:
                    continue
            md += f"{line}\n"
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
        file_pattern = f"{POKEMON_INPUT_PATH}{key}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            pokemon_data = json.loads(load(file_path, logger))
            moves = pokemon_data["moves"].get("black-white", None)
            if moves is None:
                continue

            for line in move_changes[key]:
                parts = line.split(" ")
                level = int(parts[2])
                name = "-".join(parts[4:]).lower()
                move_index = next(
                    (
                        i
                        for i, move in enumerate(moves)
                        if move["name"].replace(" ", "").lower() == name.replace(" ", "").lower()
                    ),
                    None,
                )

                if line.startswith("+"):
                    logger.log(logging.DEBUG, f"Adding move {name} at level {level} for {key} (+)")
                    if move_index is not None:
                        moves[move_index]["level_learned_at"] = level
                        moves[move_index]["learn_method"] = "level-up"
                        logger.log(logging.DEBUG, f"Updated move {name} to level {level} for {key}")
                    else:
                        moves.append({"name": name, "level_learned_at": level, "learn_method": "level-up"})
                        logger.log(logging.DEBUG, f"Added move {name} at level {level} for {key}")
                elif line.startswith("-"):
                    logger.log(logging.DEBUG, f"Replacing move at level {level} for {key} (-)")
                    replace_index = next(
                        (i for i, move in enumerate(moves) if move["level_learned_at"] == level), None
                    )
                    if replace_index is not None:
                        moves[replace_index]["name"] = name
                        moves[replace_index]["learn_method"] = "level-up"
                        logger.log(logging.DEBUG, f"Replaced move at level {level} with {name} for {key}")
                    else:
                        logger.log(logging.DEBUG, f"Could not find move at level {level} for {key}")
                elif line.startswith("="):
                    logger.log(logging.DEBUG, f"Updating move {name} to level {level} for {key} (=)")
                    if move_index is not None:
                        moves[move_index]["level_learned_at"] = level
                        logger.log(logging.DEBUG, f"Updated move {name} to level {level} for {key}")
                    else:
                        logger.log(logging.DEBUG, f"Could not find move {name} for {key}")

            save(file_path, json.dumps(pokemon_data, indent=4), logger)
    logger.log(logging.INFO, "Pokémon movesets adjusted successfully!")

    save(f"{OUTPUT_PATH}level_up_move_changes.md", md, logger)


if __name__ == "__main__":
    main()
