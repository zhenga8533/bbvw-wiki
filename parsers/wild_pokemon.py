from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import logging
import os


def parse_special_encounter(data):
    lines = data.strip().split("\n")
    pokemon, level = lines[0].split(", ")
    location = ",<br>".join(lines[1].split(", "))
    encounter_id = "Set"
    chance = "–"
    if len(lines) > 2:
        encounter_data = lines[2].split(", ")
        encounter_id = "_".join(encounter_data[0:-1]).replace(" ", "_").lower()
        chance = encounter_data[-1]
    pokemon_id = format_id(pokemon)

    md = "| Sprite | Pokémon | Level | Encounter Type | Location | Chance |\n| :---: | --- | --- | :---: | --- | --- |\n"
    md += f"| ![{pokemon_id}](../../assets/sprites/{pokemon_id}/front.gif) "
    md += f"| {pokemon} "
    md += f"| {level} "
    if encounter_id == "Set":
        md += f"| {encounter_id} "
    else:
        md += f"| ![{encounter_id}](../../assets/encounter_types/{encounter_id}.png){{: style='max-width: 24px;' }} "
    md += f"| {location} "
    md += f"| {chance} "
    md += "|\n"

    return md


def main():
    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    WILD_ENCOUNTER_PATH = os.getenv("WILD_ENCOUNTER_PATH")
    logger = Logger("Wild Pokémon Parser", f"{LOG_PATH}wild_pokemon.log", LOG)
    content = load(f"{INPUT_PATH}Wild Pokemon.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    locations = []
    encounter_header = ""
    encounter_data = ""
    special_encounter = False

    curr_location = None
    location_md = ""
    location_header = "| Sprite | Pokémon | Encounter Type | Chance |\n| :---: | --- | :---: | --- |\n"

    # Parse the content
    logger.log(logging.INFO, "Parsing Wild Pokémon content")
    for i in range(n):
        last_line = lines[i - 1] if i > 0 else ""
        line = lines[i].strip()
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "" or line.startswith("="):
            if special_encounter and not last_line.endswith("Encounter"):
                md += "```\n\n"

                # Parse special encounter data
                location_md += encounter_header
                location_md += parse_special_encounter(encounter_data)
                special_encounter = False
        # Pokémon location
        elif last_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
            if location_md != "" and curr_location != "Black City / White Forest":
                save(
                    f"{WILD_ENCOUNTER_PATH}{curr_location.lower().replace(" ", "_")}/wild_pokemon.md",
                    location_md,
                    logger,
                )

            location_md = location_header
            curr_location = line
            locations.append(line)
        # Wild Pokémon encounters
        elif ": " in line:
            encounter_type, encounters = line.split(": ")
            encounters = encounters.split(", ")

            md += f"{encounter_type}\n\n"
            md += f"```\n"
            location_md = location_md.rstrip(location_header) + f"\n\n### {encounter_type}\n"

            if not location_md.endswith(location_header):
                location_md += f"\n{location_header}"

            for i, encounter in enumerate(encounters):
                pokemon, chance = encounter.split(" (")
                chance = chance.rstrip(")")
                pokemon_id = format_id(pokemon)
                encounter_id = format_id(encounter_type).replace("-", "_")

                md += f"{i + 1}. [{pokemon}](../pokemon/{pokemon_id}.md/) ({chance})\n"
                location_md += f"| ![{pokemon_id}](../../assets/sprites/{pokemon_id}/front.gif) "
                location_md += f"| [{pokemon}](../../pokemon/{pokemon_id}.md/) "
                location_md += f"| ![{encounter_type}](../../assets/encounter_types/{encounter_id}.png){{: style='max-width: 24px;' }} "
                location_md += f"| {chance} |\n"

            md += "```\n\n"
        # Special encounter header
        elif line.endswith("Encounter"):
            md += line + "\n\n```\n"
            encounter_header = f"\n### {line}\n\n"
            encounter_data = ""
            special_encounter = True
        # Special encounter description
        elif line.startswith("* "):
            md += "```\n\n"
            md += f"<sub><sup>_{line[2:]}_</sup></sub>\n\n"

            if special_encounter:
                special_encounter = False
                location_md += encounter_header
                location_md += parse_special_encounter(encounter_data)
                encounter_data = ""
        # Special encounter data
        elif special_encounter:
            line = line.rstrip(".") + "\n"
            encounter_data += line
            md += line
        # Location subheader
        elif " – " in line:
            md += f"#### <u>{line}</u>\n\n"

            location_md = location_md.rstrip(location_header) + f"\n\n---\n\n## {line}\n\n"
            location_md += location_header
        # Misc lines
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Wild Pokémon parsed successfully!")

    save(f"{WILD_ENCOUNTER_PATH}{curr_location.lower().replace(" ", "_")}/wild_pokemon.md", location_md, logger)
    save(f"{OUTPUT_PATH}wild_pokemon.md", md, logger)


if __name__ == "__main__":
    main()
