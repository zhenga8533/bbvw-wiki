from dotenv import load_dotenv
from util.file import load, save, verify_asset_path
from util.format import format_id
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
    logger = Logger("Trainer Rosters Parser", f"{LOG_PATH}trainer_rosters.log", LOG)
    content = load(f"{INPUT_PATH}Trainer Rosters.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""
    wild_md = ""

    list_index = 0
    location = None
    important_trainers = []
    generic_trainers = []

    # Parse the content
    logger.log(logging.INFO, "Parsing Trainer Rosters content")
    for i in range(n):
        next_line = lines[i + 1] if i + 1 < n else ""
        line = lines[i]
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Skip empty lines and parse trainer data
        if line == "---":
            continue
        elif line == "":
            list_index = 0
            if len(important_trainers) > 0:
                wild_md += "---\n\n## Important Trainers\n\n"
                for i, trainer in enumerate(important_trainers):
                    wild_md += f"{i + 1}. [{trainer}](important_trainer_rosters.wild_md#{format_id(trainer)})\n"
                wild_md += "\n"
                important_trainers = []
            if len(generic_trainers) > 0:
                wild_md += "---\n\n## Generic Trainers</h3>\n\n"
                wild_md += "| Trainer | P1 | P2 | P3 | P4 | P5 | P6 |\n"
                wild_md += "|:-------:|:--:|:--:|:--:|:--:|:--:|:--:|\n"
                for trainer in generic_trainers:
                    wild_md += trainer + "\n"
                wild_md += "\n"
                generic_trainers = []
            if location is not None:
                file_path = f"{WILD_ENCOUNTER_PATH}{location.lower().replace(" ", "_")}/trainer_rosters.md"
                save(file_path, wild_md, logger)
                wild_md = ""
                location = None
        # Location header
        elif next_line == "---":
            md += f"\n---\n\n## {line}\n\n"
            location = line
        # Important trainer
        elif line.startswith("* "):
            name = line[2:]
            list_index += 1
            md += f"{list_index}. [{name}](important_trainer_rosters.md#{format_id(name)})\n"
            important_trainers.append(name)
        # Generic trainer
        elif ": " in line:
            list_index += 1
            trainer, pokemon = line.split(": ")

            # Fetch trainer sprite
            trainer_id = format_id(trainer).replace("-", "_")
            trainer_sprite = f"../../assets/trainers/{trainer_id}.png"
            trainer_parts = trainer_id.split("_")
            trainer_i = len(trainer_parts) - 1
            while not verify_asset_path(trainer_sprite, logger) and trainer_i > 0:
                trainer_sprite = f"../../assets/trainers/{"_".join(trainer_parts[:trainer_i])}.png"
                trainer_i -= 1
            trainer_md = f"| ![{trainer}]({trainer_sprite})<br>{trainer} |"

            md += f"{list_index}. {trainer}:\n"
            for i, p in enumerate(pokemon.split(", ")):
                parts = p.split(" ")
                level = parts.pop()[1:]
                pokemon_name = " ".join(parts)
                pokemon_id = format_id(pokemon_name)

                md += f"    {i + 1}. Lv. {level} [{pokemon_name}](../../pokemon/{pokemon_id}.wild_md/)\n"
                trainer_md += f" ![{pokemon_name}](../../assets/sprites/{pokemon_id}/front.png)<br>"
                trainer_md += f"[{pokemon_name}](../../pokemon/{pokemon_id}.wild_md/)<br>Lv. {level} |"
            generic_trainers.append(trainer_md)
        else:
            md += f"\n{line}\n"

    logger.log(logging.INFO, "Trainer Rosters content parsed successfully!")

    save(f"{OUTPUT_PATH}trainer_rosters.md", md, logger)


if __name__ == "__main__":
    main()
