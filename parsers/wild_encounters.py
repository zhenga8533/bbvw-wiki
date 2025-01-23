from dotenv import load_dotenv
from util.file import load, save
from util.format import format_id
from util.logger import Logger
import logging
import os


def main():
    # Load environment variables and logger
    load_dotenv()
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    WILD_ENCOUNTER_PATH = os.getenv("WILD_ENCOUNTER_PATH")
    LOG = os.getenv("LOG")
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Wild Encounters", f"{LOG_PATH}wild_encounters.log", LOG)

    nav = ""

    # Loop through all directories in wild encounters
    for dirpath, _, filenames in os.walk(WILD_ENCOUNTER_PATH):
        if dirpath == WILD_ENCOUNTER_PATH:
            continue
        logger.log(logging.INFO, f"Processing {dirpath}...")
        logger.log(logging.DEBUG, f"Files found: {filenames}")

        location = dirpath.rsplit("/", 1)[-1].replace("_", " ").title()
        nav += f"      - {location}:\n"

        for file_name in filenames:
            category = file_name.split(".")[0].replace("_", " ").title()
            nav += f"          - {category}: {dirpath}/{file_name}\n"

    save(f"{OUTPUT_PATH}wild_encounters.md", nav, logger)


if __name__ == "__main__":
    main()
