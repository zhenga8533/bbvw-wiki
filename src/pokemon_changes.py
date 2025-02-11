from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id, revert_id
from util.logger import Logger
import glob
import json
import logging
import os


def parse_moves(line: str, split_key: str):
    """
    Parse the moves from a line of text.

    :param line: The line of text to parse.
    :param split_key: The key to split the line by.
    :return: The list of moves parsed from the line.
    """

    parts = line.split(": ")[1]
    move_parts = parts.split(split_key)[1:]
    moves = [
        "-".join(move for move in move_part.split(" ") if len(move) > 0 and move[0].isupper())
        .lower()
        .rstrip(".")
        .rstrip(",")
        for move_part in move_parts
    ]

    return moves


def main():
    """
    Parse the Pokémon Changes content and save it as a Markdown file.

    :return: None
    """

    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    logger = Logger("Pokemon Changes Parser", f"{LOG_PATH}pokemon_changes.log", LOG)
    content = load(f"{INPUT_PATH}Pokemon Changes.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = False
    curr_pokemon = None
    pokemon_changes = {}

    # Parse the content
    logger.log(logging.INFO, "Parsing Pokémon Changes content")
    for i in range(n):
        line = lines[i].strip()
        line = line.replace("", "→")
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "":
            if listing:
                md += "</code></pre>\n\n"
                listing = False
            continue
        # Pokémon change header
        elif line.startswith("#"):
            pokemon = line.split(", ")
            links = []
            sprites = ""

            for p in pokemon:
                name = format_id(p, start_index=1)
                links.append(f"[{p}](../pokemon/{name}.md/)")
                sprites += f'![{name}](../assets/sprites/{name}/front.gif "{revert_id(name)}")\n'
            md += f"**{', '.join(links)}**\n\n{sprites}\n<pre><code>"

            curr_pokemon = line
            listing = True
        # Region header
        elif line.endswith("Pokémon") or line == "Evolution Changes":
            md += f"---\n\n## {line}\n\n"
        # General change list
        elif line.startswith("The following Pokémon"):
            strs = line.split(": ")
            md += f"**{strs[0]}:**\n\n<pre><code>"

            pokemon = strs[1].rstrip(".").split(", ")
            for i, p in enumerate(pokemon):
                pokemon_id = format_id(p)
                md += f'{i + 1}. <a href="/bbvw-wiki/pokemon/{pokemon_id}.md/">{p}</a>\n'
            md += "</code></pre>\n\n"
        # General change header
        elif listing and ": " in line:
            strs = line.split(": ")
            md += f"<b>{strs[0]}:</b> {strs[1]}\n"

            if curr_pokemon is not None:
                if curr_pokemon in pokemon_changes:
                    pokemon_changes[curr_pokemon].append(line)
                else:
                    pokemon_changes[curr_pokemon] = [line]
        # Misc changes
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"
    logger.log(logging.INFO, "Pokémon Changes parsed successfully!")

    # Update pokemon data
    logger.log(logging.INFO, "Updating Pokémon data")
    for key in pokemon_changes:
        pokemon = [format_id(p, start_index=1) for p in key.split(", ")]
        lines = pokemon_changes[key]

        # All variables that can be updated
        items = {}
        abilities = []
        base_experience = None
        catch_rate = None
        base_happiness = None
        evolution = []
        types = []
        tms = []
        hms = []
        tutor_moves = []
        stats = {}

        # Parse the changes
        for line in lines:
            # Parse new items
            if line.startswith("Item"):
                item_data = line.split(": ")[1].split(", ")
                for item in item_data:
                    parts = item.split(" ")
                    item_name = "-".join(parts[:-1]).lower()
                    rarity = int("".join(c for c in parts[-1] if c.isdigit()))

                    items[item_name] = {
                        "black": rarity,
                        "white": rarity,
                    }

            # Parse new abilities
            elif line.startswith("Ability"):
                ability_name = format_id(line.split(": ")[1])
                if next((a for a in abilities if a["name"] == ability_name), None) is not None:
                    continue

                abilities.append(
                    {
                        "name": ability_name,
                        "is_hidden": False,
                        "slot": len(abilities) + 1,
                    }
                )

            # Parse new base XP
            elif line.startswith("Base XP"):
                parts = line.split(": ")[1].split(" → ")[1]
                base_experience = int(parts)

            # Parse new catch rate
            elif line.startswith("Catch Rate"):
                parts = line.split(": ")[1]
                catch_rate = int(parts)

            # Parse new base happiness
            elif line.startswith("Base Happiness"):
                parts = line.split(": ")[1]
                base_happiness = int(parts)

            # Parse new evolution
            elif line.startswith("Evolution"):
                evo, parts = line.split(": ")
                if evo.endswith(")"):
                    parts = f"{evo.split(' ')[1][1:-1]}: {parts}"

                evolution.append(parts)

            # Parse new types
            elif line.startswith("Type"):
                parts = line.split(": ")[1].lower().split(" / ")
                types = parts

            # Parse changed moves
            elif line.startswith("TM"):
                tms = parse_moves(line, "TM")
            elif line.startswith("HM"):
                hms = parse_moves(line, "HM")
            elif line.startswith("Tutor"):
                tutor_moves = parse_moves(line, "and")

            # Parse remaining stats
            else:
                parts = line.split(": ")
                stat_name = format_id(parts[0])
                new_value = int(parts[1].split(" → ")[1])
                stats[stat_name] = new_value

        # Update Pokémon data
        logger.log(logging.DEBUG, f"Updating Pokémon data for {pokemon} with the following changes:")
        logger.log(logging.DEBUG, f"Items: {items}")
        logger.log(logging.DEBUG, f"Abilities: {abilities}")
        logger.log(logging.DEBUG, f"Base Experience: {base_experience}")
        logger.log(logging.DEBUG, f"Catch Rate: {catch_rate}")
        logger.log(logging.DEBUG, f"Base Happiness: {base_happiness}")
        logger.log(logging.DEBUG, f"Evolution: {evolution}")
        logger.log(logging.DEBUG, f"Types: {types}")
        logger.log(logging.DEBUG, f"TMs: {tms}")
        logger.log(logging.DEBUG, f"HMs: {hms}")
        logger.log(logging.DEBUG, f"Tutor Moves: {tutor_moves}")
        logger.log(logging.DEBUG, f"Stats: {stats}")

        # Update Pokémon data with changes
        for p in pokemon:
            file_pattern = f"{POKEMON_INPUT_PATH + p}*.json"
            files = glob.glob(file_pattern)

            # Loop through each Pokémon file
            for file_path in files:
                pokemon_data = json.loads(load(file_path, logger))
                moves = pokemon_data["moves"].get("black-white", None)
                if moves is None:
                    continue

                # Update Pokémon data
                if len(items) > 0:
                    pokemon_data["held_items"] = items
                if len(abilities) > 0:
                    pokemon_data["abilities"] = abilities
                if base_experience is not None:
                    pokemon_data["base_experience"] = base_experience
                if catch_rate is not None:
                    pokemon_data["capture_rate"] = catch_rate
                if base_happiness is not None:
                    pokemon_data["base_happiness"] = base_happiness
                if evolution is not None:
                    pokemon_data["evolution_changes"] = evolution
                if len(types) > 0:
                    pokemon_data["types"] = types
                if len(tms) > 0:
                    for tm in tms:
                        tm_index = next(
                            (
                                i
                                for i, move in enumerate(moves)
                                if format_id(move["name"]) == tm and move["learn_method"] == "machine"
                            ),
                            None,
                        )
                        if tm_index is None:
                            moves.append({"name": tm, "level_learned_at": 0, "learn_method": "machine"})
                if len(hms) > 0:
                    for hm in hms:
                        hm_index = next(
                            (
                                i
                                for i, move in enumerate(moves)
                                if format_id(move["name"]) == hm and move["learn_method"] == "machine"
                            ),
                            None,
                        )
                        if hm_index is None:
                            moves.append({"name": hm, "level_learned_at": 0, "learn_method": "machine"})
                if len(tutor_moves) > 0:
                    for tutor_move in tutor_moves:
                        tutor_index = next(
                            (
                                i
                                for i, move in enumerate(moves)
                                if format_id(move["name"]) == tutor_move and move["learn_method"] == "tutor"
                            ),
                            None,
                        )
                        if tutor_index is None:
                            moves.append({"name": tutor_move, "level_learned_at": 0, "learn_method": "tutor"})
                for stat in stats:
                    pokemon_data["stats"][stat] = stats[stat]

                save(file_path, json.dumps(pokemon_data, indent=4), logger)
    logger.log(logging.INFO, "Pokémon data updated successfully!")

    save(f"{OUTPUT_PATH}pokemon_changes.md", md, logger)


if __name__ == "__main__":
    main()
