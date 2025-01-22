from dotenv import load_dotenv
from util.file import load, save
from util.format import clean_variable_name
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
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Important Trainer Rosters Parser", f"{LOG_PATH}important_trainer_rosters.log", LOG)
    content = load(f"{INPUT_PATH}Important Trainer Rosters.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = 0
    listing_type = None
    teaming = False
    pokemon_sets = []

    # Parse the content
    logger.log(logging.INFO, "Parsing Important Trainer Rosters content")
    for i in range(n):
        next_line = lines[i + 1] if i + 1 < n else ""
        line = lines[i].strip()
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "":
            continue
        # Start of a new section
        elif next_line.startswith("Battle Type"):
            # Close previous section
            if teaming:
                for p in pokemon_sets:
                    md += "\n" + p.to_string()
                pokemon_sets = []

                md += "</code></pre>\n\n"
                listing = 0

            md += f"---\n\n## {line}\n\n<pre><code>"
            teaming = True
        elif line.startswith("Battle Type:") or line.startswith("Reward:") or line.startswith("Location:"):
            s = line.split(": ")
            md += f"<b>{s[0]}:</b> {s[1]}\n"
        # Pokémon Team
        elif "’s Team" in line:
            for p in pokemon_sets:
                md += "\n" + p.to_string()
            pokemon_sets = []
            listing = 1

            md += f"\n<b><u>{line}</u></b>\n"
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
            md += f"{line}\n"
            if not teaming:
                md += "\n"

    if len(pokemon_sets) > 0:
        for p in pokemon_sets:
            md += "\n" + p.to_string()
        md += "</code></pre>\n"
    logger.log(logging.INFO, "Important Trainer Rosters content parsed successfully!")

    save(f"{OUTPUT_PATH}important_trainer_rosters.md", md, logger)


if __name__ == "__main__":
    main()
