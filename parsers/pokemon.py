from dotenv import load_dotenv
from util.file import load, save
from util.format import create_image_table
from util.logger import Logger
import glob
import json
import logging
import os
import requests


def parse_evolution_line(evolution, pokemon_set, level=1, index=1):
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    names = [evolution["name"]]

    for name in names[:]:
        if name not in pokemon_set:
            names.remove(name)
            file_pattern = f"{POKEMON_INPUT_PATH}{name}*.json"
            files = glob.glob(file_pattern)

            for file_path in files:
                new_name = file_path.split("\\")[-1].split(".")[0]
                if new_name != name and new_name in pokemon_set and new_name not in names:
                    names.append(new_name)
    if len(names) == 0:
        return ""

    md = ""
    for name in names:
        md += f"{'    ' * (level - 1)}{index}. "
        evolution_details = evolution["evolution_details"]
        if len(evolution_details) > 0:
            md += f"{evolution_details[-1]["trigger"]["name"].replace("-", " ").title()}: "
        md += f"[{name.title()}]({name}.md/)\n"

        if evolution["evolutions"]:
            for i, sub_evolution in enumerate(evolution["evolutions"], 1):
                md += parse_evolution_line(sub_evolution, pokemon_set, level + 1, i)
        md += "\n"

    return md.strip()


def calculate_hp(base: int, iv: int, ev: int, level: int) -> int:
    return int(((2 * base + iv + ev // 4) * level) // 100 + level + 10)


def calculate_stat(base: int, iv: int, ev: int, level: int, nature: float) -> int:
    return int((((2 * base + iv + ev // 4) * level) // 100 + 5) * nature)


def parse_stats(stats: dict) -> str:
    md = "---\n\n## Base Stats\n"
    hp = stats["hp"]
    attack = stats["attack"]
    defense = stats["defense"]
    sp_attack = stats["special-attack"]
    sp_defense = stats["special-defense"]
    speed = stats["speed"]
    md += f"|   | HP | Attack | Defense | Sp. Atk | Sp. Def | Speed |\n"
    md += f"|---|----|--------|---------|---------|---------|-------|\n"
    md += f"| **Base** | {hp} | {attack} | {defense} | {sp_attack} | {sp_defense} | {speed} |\n"
    md += f"| **Min** "
    md += f"| {calculate_hp(hp, 0, 0, 100)} "
    md += f"| {calculate_stat(attack, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(defense, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(sp_attack, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(sp_defense, 0, 0, 100, 0.9)} "
    md += f"| {calculate_stat(speed, 0, 0, 100, 0.9)} |\n"
    md += f"| **Max** "
    md += f"| {calculate_hp(hp, 31, 252, 100)} "
    md += f"| {calculate_stat(attack, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(defense, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(sp_attack, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(sp_defense, 31, 252, 100, 1.1)} "
    md += f"| {calculate_stat(speed, 31, 252, 100, 1.1)} |\n\n"
    md += "The ranges shown above are for a level 100 Pokémon. "
    md += "Maximum values are based on a beneficial nature, 252 EVs, 31 IVs; "
    md += "minimum values are based on a hindering nature, 0 EVs, 0 IVs.\n\n"

    return md


def parse_moves(moves: list, headers: list, move_key: str, logger: Logger) -> str:
    MOVES_PATH = os.getenv("MOVES_PATH")

    md_header = " | ".join(headers).strip()
    md_separator = " | ".join(["---"] * len(headers)).strip()
    md_body = ""

    for move in moves:
        move_data = json.loads(load(f"{MOVES_PATH}{move['name']}.json", logger))
        for category in headers:
            if category == "Lv.":
                md_body += f"| {move["level_learned_at"]} "
            elif category == "TM":
                md_body += f"| {move_data["machines"][move_key].upper()} "
            elif category == "Move":
                md_body += f"| {move_data["name"].replace("-", " ").title()} "
            elif category == "Type":
                md_body += f"| ![{move_data["type"]}](../assets/types/{move_data["type"]}.png){{: width='48'}} "
            elif category == "Cat.":
                md_body += f"| ![{move_data["damage_class"]}](../assets/move_category/{move_data["damage_class"]}.png){{: width='36'}} "
            elif category == "Power":
                md_body += f"| {move_data["power"] or "—"} "
            elif category == "Acc.":
                md_body += f"| {move_data["accuracy"] or "—"} "
            elif category == "PP":
                md_body += f"| {move_data["pp"]} "
        md_body += "|\n"

    return f"{md_header}\n{md_separator}\n{md_body}\n"


def to_md(pokemon: dict, pokemon_set: dict, logger: Logger) -> str:
    # Basic information
    name_id = pokemon["name"]
    pokemon_name = name_id.replace("-", " ").title()
    pokemon_id = pokemon["id"]
    md = f"# #{pokemon["id"]:03} {pokemon_name} ({pokemon["genus"]})\n\n"

    # Add official artwork
    md += create_image_table(
        ["Official Artwork", "Shiny Artwork"],
        [
            [
                f"../assets/sprites/{name_id}/official_artwork.png",
                f"../assets/sprites/{name_id}/official_artwork_shiny.png",
            ]
        ],
        logger,
    )

    # Add flavor text
    flavor_text_entries = pokemon["flavor_text_entries"]
    if "black" in flavor_text_entries and "white" in flavor_text_entries:
        black_flavor_text = flavor_text_entries["black"].replace("\n", " ")
        white_flavor_text = flavor_text_entries["white"].replace("\n", " ")
        if black_flavor_text == white_flavor_text:
            md += f"{black_flavor_text}\n\n"
        else:
            md += f"**Blaze Black:** {black_flavor_text}\n\n"
            md += f"**Volt White:** {white_flavor_text}\n\n"
    else:
        flavor_text_keys = list(flavor_text_entries.keys())
        md += f"{flavor_text_entries[flavor_text_keys[-1]].replace('\n', ' ')}\n\n"

    # Add sprites
    md += "---\n\n## Media\n\n"
    md += "### Sprites\n\n"
    image_headers = ["Front", "Back", "Front Shiny", "Back Shiny"]
    md += create_image_table(
        image_headers,
        [
            [
                f"../assets/sprites/{name_id}/front.gif",
                f"../assets/sprites/{name_id}/back.gif",
                f"../assets/sprites/{name_id}/front_shiny.gif",
                f"../assets/sprites/{name_id}/back_shiny.gif",
            ],
            [
                f"../assets/sprites/{name_id}/front.png",
                f"../assets/sprites/{name_id}/back.png",
                f"../assets/sprites/{name_id}/front_shiny.png",
                f"../assets/sprites/{name_id}/back_shiny.png",
            ],
        ],
        logger,
    )

    female_sprite_table = create_image_table(
        image_headers,
        [
            [
                f"../assets/sprites/{name_id}/front_female.gif",
                f"../assets/sprites/{name_id}/back_female.gif",
                f"../assets/sprites/{name_id}/front_shiny_female.gif",
                f"../assets/sprites/{name_id}/back_shiny_female.gif",
            ],
            [
                f"../assets/sprites/{name_id}/front_female.png",
                f"../assets/sprites/{name_id}/back_female.png",
                f"../assets/sprites/{name_id}/front_shiny_female.png",
                f"../assets/sprites/{name_id}/back_shiny_female.png",
            ],
        ],
        logger,
    )
    if female_sprite_table != "":
        md += "### Female Sprites\n\n"
        md += female_sprite_table

    # Cries
    md += "### Cries\n\n"
    md += "Latest (Gen VI+):\n<p><audio controls>\n"
    md += f"  <source src='../assets/cries/{pokemon_id}/latest.ogg' type='audio/ogg'>\n"
    md += "  Your browser does not support the audio element.\n"
    md += "</audio></p>\n\n"
    md += "Legacy:\n<p><audio controls>\n"
    md += f"  <source src='../assets/cries/{pokemon_id}/legacy.ogg' type='audio/ogg'>\n"
    md += "  Your browser does not support the audio element.\n"
    md += "</audio></p>\n\n"

    # Pokédex data
    md += "---\n\n## Pokédex Data\n\n"
    md += f"| National № | Type(s) | Height | Weight | Abilities | Local № |\n"
    md += f"|------------|---------|--------|--------|-----------|---------|\n"
    md += f"| #{pokemon["id"]} "
    md += f"| {" ".join([f"![{t}](../assets/types/{t}.png){{: width='48'}}" for t in pokemon["types"]])} "
    md += f"| {pokemon["height"]} m "
    md += f"| {pokemon["weight"]} kg "
    md += (
        f"| {"<br>".join([f"{i + 1}. {ability["name"].title()}" for i, ability in enumerate(pokemon["abilities"])])} "
    )
    md += f"| #{pokemon["pokedex_numbers"].get("original-unova", "N/A")} |\n\n"

    # Stats
    md += "---\n\n## Base Stats\n"
    stats = pokemon["stats"]
    md += parse_stats(stats)

    # Forms
    md += "---\n\n## Forms & Evolutions\n\n"
    md += '!!! warning "WARNING"\n\n'
    md += "    Some forms may not be available in Blaze Black/Volt White."
    md += " Also information on evolutions may not be 100% accurate;"
    md += " it is currently quite complex to track generational evolution data.\n\n"

    md += "### Forms\n\n"
    forms = pokemon["forms"]
    if len(forms) == 1:
        md += f"{pokemon_name} has no alternate forms.\n\n"
    else:
        for i, form in enumerate(forms):
            md += f"{i + 1}. [{form.title()}]({form}.md/)\n"
        md += "\n"

    # Evolutions
    md += "### Evolution Line\n\n"
    evolutions = pokemon["evolutions"]
    if len(evolutions) == 0:
        md += f"{pokemon_name} does not evolve.\n\n"
    else:
        md += f"{parse_evolution_line(evolutions[0], pokemon_set)}\n\n"

    if "evolution_changes" in pokemon:
        md += f"```\n{pokemon['evolution_changes']}\n```\n\n"

    # Training
    md += "---\n\n## Training\n\n"
    md += f"| EV Yield | Catch Rate | Base Friendship | Base Exp. | Growth Rate | Held Items |\n"
    md += f"|----------|------------|-----------------|-----------|-------------|------------|\n"
    ev_yield = pokemon["ev_yield"]
    md += f"| {"<br>".join([f"{ev_yield[stat]} {stat.replace("-", " ").title()}" for stat in ev_yield if ev_yield[stat] > 0])} "
    md += f"| {pokemon["capture_rate"]} "
    md += f"| {pokemon["base_happiness"]} "
    md += f"| {pokemon["base_experience"]} "
    md += f"| {pokemon["growth_rate"].title()} | "
    held_items = [
        {
            "name": item["name"].replace("-", " ").title(),
            "rarity": next(
                (r["rarity"] for r in item["rarity"] if r["version"] in {"black", "white"}),
                None,
            ),
        }
        for item in pokemon["held_items"]
    ]
    if len(held_items) == 0:
        md += f"N/A |\n\n"
    else:
        md += f"{"<br>".join([f"{item['name']} ({item['rarity']}%)" for item in held_items if item["rarity"]])} |\n\n"

    # Breeding
    md += "---\n\n## Breeding\n\n"
    md += f"| Egg Groups | Egg Cycles | Gender | Dimorphic | Color | Shape |\n"
    md += f"|------------|------------|--------|-----------|-------|-------|\n"
    md += f"| {"<br>".join([f"{i + 1}. {group.title()}" for i, group in enumerate(pokemon["egg_groups"])])} "
    md += f"| {pokemon["hatch_counter"]} "
    female_rate = pokemon["female_rate"]
    md += f"| {"Genderless" if female_rate == -1 else f"{(8 - female_rate) / 8 * 100}% Male<br>{female_rate / 8 * 100}% Female"} "
    md += f"| {pokemon["has_gender_differences"]} "
    md += f"| {pokemon["color"].title()} "
    md += f"| {pokemon["shape"].title()} |\n\n"

    # Black/White Moves
    level_up_moves = []
    tm_moves = []
    egg_moves = []
    tutor_moves = []

    moves = pokemon["moves"]
    move_keys = list(moves.keys())
    move_key = "black-white" if "black-white" in move_keys else move_keys[-1] if len(move_keys) > 0 else ""
    moves = moves.get(move_key, [])

    for move in moves:
        if move["learn_method"] == "level-up":
            level_up_moves.append(move)
        elif move["learn_method"] == "machine":
            tm_moves.append(move)
        elif move["learn_method"] == "egg":
            egg_moves.append(move)
        elif move["learn_method"] == "tutor":
            tutor_moves.append(move)

    # Moves
    md += "---\n\n## Moves\n\n"
    md += '!!! warning "WARNING"\n\n'
    md += "    Specific move information may be incorrect. "
    md += "However, the general movepool should be accurate (including changes to learnset).\n\n"

    # Level Up Moves
    md += "### Level Up Moves\n\n"
    if len(level_up_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves by leveling up.\n"
    else:
        level_up_moves.sort(key=lambda x: (x["level_learned_at"], x["name"]))
        md += parse_moves(level_up_moves, ["Lv.", "Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, logger)

    # TM Moves
    md += "### TM Moves\n\n"
    if len(tm_moves) == 0:
        md += f"{pokemon_name} cannot learn any TM moves.\n"
    else:
        tm_moves_data = []
        for move in tm_moves:
            move_data = json.loads(load(f"moves/{move['name']}.json", logger))
            tm_moves_data.append(move_data)
        tm_moves_data.sort(key=lambda x: x["machines"][move_key])
        md += parse_moves(tm_moves_data, ["TM", "Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, logger)

    # Egg Moves
    md += "### Egg Moves\n\n"
    if len(egg_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves by breeding.\n"
    else:
        md += parse_moves(egg_moves, ["Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, logger)

    # Tutor Moves
    md += "### Tutor Moves\n\n"
    if len(tutor_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves from tutors.\n"
    else:
        md += parse_moves(tutor_moves, ["Move", "Type", "Cat.", "Power", "Acc.", "PP"], move_key, logger)

    return md


def main():
    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    TIMEOUT = int(os.getenv("TIMEOUT"))
    LOG_PATH = os.getenv("LOG_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
    POKEMON_OUTPUT_PATH = os.getenv("POKEMON_OUTPUT_PATH")
    logger = Logger("Pokémon Parser", f"{LOG_PATH}pokemon.log", LOG)

    # Fetch Pokémon data from PokéAPI
    try:
        logger.log(logging.INFO, "Fetching Pokémon data from PokéAPI")
        pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=649", timeout=TIMEOUT).json()[
            "results"
        ]
        logger.log(logging.INFO, "Successfully fetched Pokémon data from PokéAPI")
    except requests.exceptions.RequestException:
        logger.log(logging.ERROR, "Failed to fetch Pokémon data from PokéAPI")
        exit(1)

    # Fetch all valid Pokémon paths
    logger.log(logging.INFO, "Fetching all valid Pokémon paths")
    pokemon_set = set()
    species = []
    forms = []

    for pokemon in pokedex:
        name = pokemon["name"]
        file_pattern = f"{POKEMON_INPUT_PATH}{name.split("-")[0]}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            new_name = file_path.split("\\")[-1].split(".")[0]
            pokemon_set.add(new_name)

            if new_name == name:
                species.append(new_name)
            else:
                forms.append(new_name)

    # Remove duplicate forms
    for form in forms[:]:
        if form in species:
            forms.remove(form)
    logger.log(logging.INFO, "Successfully fetched all valid Pokémon paths")

    # Generate nav for mkdocs.yml
    logger.log(logging.INFO, "Generating Pokémon navigation")
    generations = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova"]
    pokedex_start = [0, 151, 251, 386, 493]
    nav = ""

    for i, name in enumerate(species):
        if i in pokedex_start:
            nav += f"      - {generations[pokedex_start.index(i)]}:\n"

        clean_name = name.replace("-", " ").title()
        nav += f'          - "#{f"{i + 1:03}"} {clean_name}": {POKEMON_OUTPUT_PATH}{name}.md\n'
    nav += f"      - Pokémon Forms:\n"
    for name in forms:
        clean_name = name.replace("-", " ").title()
        nav += f"          - {clean_name}: {POKEMON_OUTPUT_PATH}{name}.md\n"

    logger.log(logging.INFO, "Successfully generated Pokémon navigation")
    save(f"{OUTPUT_PATH}pokemon_nav.md", nav, logger)

    # Generate markdown files for each Pokémon
    logger.log(logging.INFO, "Generating markdown files for each Pokémon")
    for pokemon in pokedex:
        name = pokemon["name"]
        file_pattern = f"{POKEMON_INPUT_PATH}{name.split("-")[0]}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            data = json.loads(load(file_path, logger))
            md = to_md(data, pokemon_set, logger)
            save(f"{POKEMON_OUTPUT_PATH}{data["name"]}.md", md, logger)


if __name__ == "__main__":
    main()
