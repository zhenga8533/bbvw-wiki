from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import glob
import json
import logging
import os


def main():
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
                sprites += f"![{name}](../assets/sprites/{name}/front.gif)\n"
            md += f"**{', '.join(links)}**\n\n{sprites}\n<pre><code>"

            curr_pokemon = line
            listing = True
        # Region header
        elif line.endswith("Pokémon") or line == "Evolution Changes":
            md += f"---\n\n## {line}\n\n"
        # General change list
        elif line.startswith("The following Pokémon"):
            strs = line.split(": ")
            md += f"**{strs[0]}:**\n\n```\n"

            pokemon = strs[1].split(", ")
            for i, p in enumerate(pokemon):
                md += f"{i + 1}. {p.rstrip('.')}\n"
            md += "```\n\n"
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

        # Parse new items
        items = []
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

        for line in lines:
            # Parse new items
            if line.startswith("Item"):
                item_data = line.split(": ")[1].split(", ")
                for item in item_data:
                    parts = item.split(" ")
                    item_name = "-".join(parts[:-1]).lower()
                    rarity = int("".join(c for c in parts[-1] if c.isdigit()))
                    if next((i for i in items if i["name"] == item_name), None) is not None:
                        continue

                    items.append(
                        {
                            "name": item_name,
                            "rarity": [
                                {
                                    "version": "black",
                                    "rarity": rarity,
                                }
                            ],
                        }
                    )

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

            # Parse new TMs
            elif line.startswith("TM"):
                parts = line.split(": ")[1]
                tm_parts = parts.split("TM")[1:]
                tms = [
                    "-".join(tm for tm in tm_part.split(" ") if len(tm) > 0 and tm[0].isupper())
                    .lower()
                    .rstrip(".")
                    .rstrip(",")
                    for tm_part in tm_parts
                ]

            # Parse new HMs
            elif line.startswith("HM"):
                parts = line.split(": ")[1]
                hm_parts = parts.split("HM")[1:]
                hms = [
                    "-".join(hm for hm in hm_part.split(" ") if len(hm) > 0 and hm[0].isupper())
                    .lower()
                    .rstrip(".")
                    .rstrip(",")
                    for hm_part in hm_parts
                ]

            # Parse new tutor moves
            elif line.startswith("Tutor"):
                parts = line.split(": ")[1]
                move_parts = parts.split("and")
                tutor_moves = [
                    "-".join(
                        move for move in move_part.split(" ") if len(move) > 0 and move[0].isupper() and move != "Can"
                    )
                    .lower()
                    .rstrip(".")
                    .rstrip(",")
                    for move_part in move_parts
                ]

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

        for p in pokemon:
            file_pattern = f"{POKEMON_INPUT_PATH + p}*.json"
            files = glob.glob(file_pattern)

            for file_path in files:
                pokemon_data = json.loads(load(file_path, logger))
                moves = pokemon_data["moves"].get("black-white", None)
                if moves is None:
                    continue

                if len(items) > 0:
                    pokemon_data["items"] = items
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
                    moves.extend([{"name": tm, "level_learned_at": 0, "learn_method": "machine"} for tm in tms])
                if len(hms) > 0:
                    moves.extend([{"name": hm, "level_learned_at": 0, "learn_method": "machine"} for hm in hms])
                if len(tutor_moves) > 0:
                    moves.extend(
                        [{"name": move, "level_learned_at": 0, "learn_method": "tutor"} for move in tutor_moves]
                    )
                for stat in stats:
                    pokemon_data["stats"][stat] = stats[stat]

                save(file_path, json.dumps(pokemon_data, indent=4), logger)
    logger.log(logging.INFO, "Pokémon data updated successfully!")

    save(f"{OUTPUT_PATH}pokemon_changes.md", md, logger)


if __name__ == "__main__":
    main()
