from dotenv import load_dotenv
from util.file import save
from util.format import revert_id
from util.logger import Logger
import logging
import os
import string


def main():
    # Load environment variables and logger
    load_dotenv()
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    WILD_ENCOUNTER_PATH = os.getenv("WILD_ENCOUNTER_PATH")
    LOG = os.getenv("LOG")
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Wild Encounters", f"{LOG_PATH}wild_encounters.log", LOG)

    nav = ""
    location_order = [
        "",
        "nuvema_town",
        "route_1",
        "accumula_town",
        "route_2",
        "striaton_city",
        "dreamyard",
        "route_3",
        "wellspring_cave",
        "nacrene_city",
        "pinwheel_forest",
        "skyarrow_bridge",
        "castelia_city",
        "liberty_garden",
        "route_4",
        "desert_resort",
        "relic_castle",
        "nimbasa_city",
        "anville_town",
        "route_5",
        "driftveil_drawbridge",
        "driftveil_city",
        "cold_storage",
        "route_6",
        "chargestone_cave",
        "mistralton_city",
        "route_7",
        "celestial_tower",
        "route_17",
        "route_18",
        "p2_laboratory",
        "mistralton_cave",
        "rumination_field",
        "twist_mountain",
        "icirrus_city",
        "dragonspiral_tower",
        "relic_castle",
        "route_8",
        "moor_of_icirrus",
        "tubeline_bridge",
        "route_9",
        "opelucid_city",
        "route_10",
        "victory_road",
        "pokémon_league",
        "n's_castle",
        "the_royal_unova",
        "challenger's_cave",
        "route_11",
        "village_bridge",
        "route_12",
        "lacunosa_town",
        "route_13",
        "giant_chasm",
        "undella_town",
        "undella_bay",
        "abyssal_ruins",
        "route_14",
        "abundant_shrine",
        "black_city",
        "white_forest",
        "route_15",
        "poké_transfer_lab",
        "marvelous_bridge",
        "route_16",
        "lostlorn_forest",
    ]
    os_walk = os.walk(WILD_ENCOUNTER_PATH)
    locations = sorted(
        os.walk(WILD_ENCOUNTER_PATH),
        key=lambda x: location_order.index(x[0].split("/")[-1]),
    )

    # Loop through all directories in wild encounters
    for dirpath, _, filenames in locations:
        if dirpath == WILD_ENCOUNTER_PATH:
            continue
        logger.log(logging.INFO, f"Processing {dirpath}...")
        logger.log(logging.DEBUG, f"Files found: {filenames}")

        location = revert_id(dirpath.rsplit("/", 1)[-1], symbol="_")
        nav += f"      - {location}:\n"

        for file_name in filenames:
            category = revert_id(file_name.split(".")[0], symbol="_")
            nav += f"          - {category}: {dirpath}/{file_name}\n"

    save(f"{OUTPUT_PATH}wild_encounters.md", nav, logger)


if __name__ == "__main__":
    main()
