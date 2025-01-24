from dotenv import load_dotenv
from util.file import load, save
from util.format import clean_variable_name, format_id, verify_asset_path
from util.pokemon_set import PokemonSet
from util.logger import Logger
import logging
import os


def main():
    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    WILD_ENCOUNTER_PATH = os.getenv("WILD_ENCOUNTER_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Important Trainer Rosters Parser", f"{LOG_PATH}important_trainer_rosters.log", LOG)
    content = load(f"{INPUT_PATH}Important Trainer Rosters.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = 0
    listing_type = None
    pokemon_sets = []

    # Wild encounter rosters
    wild_rosters = {}
    location = None
    trainer = None

    def add_pokemon_sets():
        nonlocal md
        nonlocal pokemon_sets
        nonlocal wild_rosters
        nonlocal location

        if len(pokemon_sets) == 0:
            return

        md += "</code></pre>\n\n"
        base_md = []
        base_tables = []
        pokemon_mds = ["", "", ""]
        pokemon_tables = ["", "", ""]

        for pokemon_set in pokemon_sets:
            name = pokemon_set.species
            if name.endswith("1") or name.endswith("2") or name.endswith("3"):
                num = int(name[-1])
                pokemon_set.species = name[:-1]
                if pokemon_mds[num - 1] != "":
                    pokemon_mds[num - 1] += "<br>"
                pokemon_mds[num - 1] += "\n    ".join(pokemon_set.to_string().split("\n"))
                pokemon_tables[num - 1] += "\n    ".join(pokemon_set.to_table().split("\n")) + "\n"
            else:
                base_md.append(pokemon_set.to_string())
                base_tables.append(pokemon_set.to_table())
        pokemon_sets = []

        # Wild roster header
        if location not in wild_rosters:
            wild_rosters[location] = ""
        wild_rosters[location] += f"---\n\n## {trainer}\n\n"

        # Set trainer sprite
        trainer_id = format_id(trainer, "_")
        trainer_sprite = f"../../assets/important_trainers/{trainer_id}.png"
        trainer_parts = trainer_id.split("_")
        # Try all subarray combinations of trainer_parts
        for start_index in range(len(trainer_parts)):
            for end_index in range(start_index + 1, len(trainer_parts) + 1):
                subarray = trainer_parts[start_index:end_index]
                trainer_sprite = f"../../assets/important_trainers/{'_'.join(subarray)}.png"

                if verify_asset_path(trainer_sprite, logger):
                    wild_rosters[location] += f"![{trainer}]({trainer_sprite})\n\n"
                    break

        if pokemon_mds[0] != "":
            br = "\n    <br>"
            if len(base_md) > 0:
                base_md = br.join("\n    ".join(base.split("\n")).rstrip() for base in base_md) + br
            else:
                base_md = ""

            starters = ["Tepig", "Snivy", "Oshawott"]
            for i in range(3):
                md += f'=== "{starters[i]}"\n\n    <pre><code>'
                md += base_md
                md += pokemon_mds[i].strip() + "</code></pre>\n\n"

                # Add the table to the wild rosters
                wild_rosters[location] += f'=== "{starters[i]}"\n\n'
                wild_rosters[location] += "    | Pokemon | Attributes | Moves |\n"
                wild_rosters[location] += "    |:-------:|------------|-------|\n"
                for table in base_tables:
                    wild_rosters[location] += "    " + "\n    ".join(table.split("\n")) + "\n"
                wild_rosters[location] += "    " + "\n    ".join(pokemon_tables[i].split("\n")) + "\n\n"
        else:
            md += "<pre><code>" + "\n".join(base_md) + "</code></pre>\n\n"

            # Add the table to the wild rosters
            wild_rosters[location] += "| Pokemon | Attributes | Moves |\n"
            wild_rosters[location] += "|:-------:|------------|-------|\n"
            for table in base_tables:
                wild_rosters[location] += table + "\n"
            wild_rosters[location] += "\n"

    # Parse the content
    logger.log(logging.INFO, "Parsing Important Trainer Rosters content")
    for i in range(n):
        next_line = lines[i + 1] if i + 1 < n else ""
        line = lines[i].strip()
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "" or line == "---":
            listing = 0
        elif next_line == "---":
            add_pokemon_sets()
            md += f"## {line}\n\n"
        # Start of a new section
        elif next_line.startswith("Battle Type"):
            add_pokemon_sets()
            md += f"---\n\n### {line}\n\n<pre><code>"
            trainer = line
        elif ": " in line:
            category, value = line.split(": ")
            if category == "Location":
                location = value

            md += f"<b>{category}:</b> {value}\n"
        # Pokémon Team
        elif "’s Team" in line:
            add_pokemon_sets()
        # Pokémon Team Details
        elif (
            line.startswith("Species")
            or line.startswith("Level")
            or line.startswith("Item")
            or line.startswith("Ability")
            or line.startswith("Move #")
        ):
            strs = line.split("\t")
            listing = 1
            listing_type = clean_variable_name(strs[0].lower())

            for s in strs[1:]:
                if listing > len(pokemon_sets):
                    pokemon_sets.append(PokemonSet())
                pokemon_sets[listing - 1].__dict__[listing_type] = s
                listing += 1
        elif listing:
            strs = line.split("\t")

            for s in strs:
                if listing > len(pokemon_sets):
                    pokemon_sets.append(PokemonSet())
                pokemon_sets[listing - 1].__dict__[listing_type] = s
                listing += 1
        # Misc lines
        else:
            md += f"{line}\n\n"

    add_pokemon_sets()
    logger.log(logging.INFO, "Important Trainer Rosters content parsed successfully!")

    # Parse wild rosters into markdown files
    for location, roster in wild_rosters.items():
        file_path = f"{WILD_ENCOUNTER_PATH + location.replace(' ', '_').lower()}/important_trainers.md"
        save(file_path, roster, logger)

    save(f"{OUTPUT_PATH}important_trainer_rosters.md", md, logger)


if __name__ == "__main__":
    main()
