from util.file import save
import json
import requests


def calculate_hp(base: int, iv: int, ev: int, level: int) -> int:
    return int(((2 * base + iv + ev // 4) * level) // 100 + level + 10)


def calculate_stat(base: int, iv: int, ev: int, level: int, nature: float) -> int:
    return int((((2 * base + iv + ev // 4) * level) // 100 + 5) * nature)


def to_md(pokemon: dict) -> str:
    # Basic information
    pokemon_name = pokemon["name"].capitalize()
    md = f"# #{pokemon["id"]:03} {pokemon_name} - {pokemon["genus"]}\n\n"
    md += "| Official Artwork | Shiny Artwork |\n"
    md += "|------------------|---------------|\n"

    # Add official artwork
    official_artwork = pokemon["sprites"]["other"]["official-artwork"]
    md += f"| ![Official Artwork]({official_artwork["front_default"]}) | "
    md += f"![Official Artwork2]({official_artwork["front_shiny"]}) |\n\n"

    # Add flavor text
    black_flavor_text = pokemon["flavor_text_entries"]["black"].replace("\n", " ")
    white_flavor_text = pokemon["flavor_text_entries"]["white"].replace("\n", " ")
    if black_flavor_text == white_flavor_text:
        md += f"{black_flavor_text}\n\n"
    else:
        md += f"**Blaze Black:** {black_flavor_text}\n\n"
        md += f"**Volt White:** {white_flavor_text}\n\n"

    # Add animated sprites
    sprites = pokemon["sprites"]["versions"]["generation-v"]["black-white"]
    animated = sprites["animated"]
    md += "## Media\n\n"
    md += "### Sprites\n\n"
    md += "| Front | Back | S. Front | S. Back |\n"
    md += "|-------|------|----------|---------|\n"
    md += f"| ![Front]({animated["front_default"]}) | ![Back]({animated["back_default"]}) | "
    md += f"![Shiny Front]({animated["front_shiny"]}) | ![Shiny Back]({animated["back_shiny"]}) |\n\n"

    # Cries
    md += "### Cries\n\n"
    md += "Latest:\n<p><audio controls>\n"
    md += f"  <source src=\"{pokemon['cry_latest']}\" type=\"audio/ogg\">\n"
    md += "  Your browser does not support the audio element.\n"
    md += "</audio></p>\n\n"
    md += "Legacy (Black/White):\n<p><audio controls>\n"
    md += f"  <source src=\"{pokemon['cry_legacy']}\" type=\"audio/ogg\">\n"
    md += "  Your browser does not support the audio element.\n"
    md += "</audio></p>\n\n"

    # Pokédex data
    md += "## Pokédex Data\n\n"
    md += f"| National № | Type(s) | Height | Weight | Abilities | Local № |\n"
    md += f"|------------|---------|--------|--------|-----------|---------|\n"
    md += f"| #{pokemon["id"]} "
    md += f"| {" ".join([f"![{t}](../assets/types/{t}.png){{: width='48'}}" for t in pokemon["types"]])} "
    md += f"| {pokemon["height"]} m "
    md += f"| {pokemon["weight"]} kg "
    md += f"| {"<br>".join([f"{i + 1}. {ability["name"].capitalize()}" for i, ability in enumerate(pokemon["abilities"])])} "
    md += f"| #{pokemon["pokedex_numbers"].get("original-unova", "N/A")} |\n\n"

    # Stats
    md += "## Base Stats\n"
    stats = pokemon["stats"]
    hp, attack, defense, sp_attack, sp_defense, speed = stats.values()
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

    # Forms
    md += "## Forms & Evolutions\n\n"
    md += "### Forms\n\n"
    forms = pokemon["forms"]
    if len(forms) == 1:
        md += f"{pokemon_name} has no alternate forms.\n\n"
    else:
        for i, form in enumerate(forms):
            md += f"{i + 1}. {form.capitalize()}\n"
        md += "\n"

    # Evolutions
    md += "### Evolutions\n\n"
    evolutions = pokemon["evolutions"]
    if len(evolutions) == 0:
        md += f"{pokemon_name} does not evolve.\n\n"
    else:
        for i, evolution in enumerate(evolutions):
            evolution_species = evolution["species"]
            md += f"{i + 1}. {evolution_species.capitalize()}\n"

            # Add evolution's evolution
            try:
                with open(f"data/{evolution_species}.json", "r") as file:
                    evolution_data = json.load(file)
                evolution_evolutions = evolution_data["evolutions"]
                if len(evolution_evolutions) > 0:
                    for j, evo in enumerate(evolution_evolutions):
                        md += f"\t{j + 1}. {evo['species'].capitalize()}\n"
            except FileNotFoundError:
                pass

    # Training
    md += "## Training\n\n"
    md += f"| EV Yield | Catch Rate | Base Friendship | Base Exp. | Growth Rate |\n"
    md += f"|----------|------------|-----------------|-----------|-------------|\n"
    ev_yield = pokemon["ev_yield"]
    md += f"| {"<br>".join([f"{ev_yield[stat]} {stat.capitalize()}" for stat in ev_yield if ev_yield[stat] > 0])} "
    md += f"| {pokemon["capture_rate"]} "
    md += f"| {pokemon["base_happiness"]} "
    md += f"| {pokemon["base_experience"]} "
    md += f"| {pokemon["growth_rate"].capitalize()} |\n\n"

    # Breeding
    md += "## Breeding\n\n"
    md += f"| Egg Groups | Egg Cycles | Gender | Dimorphic | Color | Shape |\n"
    md += f"|------------|------------|--------|-----------|-------|-------|\n"
    md += f"| {"<br>".join([f"{i + 1}. {group.capitalize()}" for i, group in enumerate(pokemon["egg_groups"])])} "
    md += f"| {pokemon["hatch_counter"]} "
    female_rate = pokemon["female_rate"]
    md += f"| {"Genderless" if female_rate == -1 else f"{(8 - female_rate) / 8 * 100}% Male<br>{female_rate / 8 * 100}% Female"} "
    md += f"| {pokemon["has_gender_differences"]} "
    md += f"| {pokemon["color"].capitalize()} "
    md += f"| {pokemon["shape"].capitalize()} |\n\n"

    # Black/White Moves
    level_up_moves = []
    tm_moves = []
    egg_moves = []
    tutor_moves = []
    for move in pokemon["moves"]["black-white"]:
        if move["learn_method"] == "level-up":
            level_up_moves.append(move)
        elif move["learn_method"] == "machine":
            tm_moves.append(move)
        elif move["learn_method"] == "egg":
            egg_moves.append(move)
        elif move["learn_method"] == "tutor":
            tutor_moves.append(move)

    # Level Up Moves
    md += "## Moves\n\n"
    md += "### Level Up Moves\n\n"
    if len(level_up_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves by leveling up.\n"
    else:
        level_up_moves.sort(key=lambda x: (x["level_learned_at"], x["name"]))
        md += "| Lv. | Move | Type | Cat. | Power | Acc. | PP |\n"
        md += "|-----|------|------|------|-------|------|----|\n"
        for move in level_up_moves:
            with open(f"moves/{move["name"]}.json", "r") as file:
                move_data = json.load(file)
            md += f"| {move["level_learned_at"]} "
            md += f"| {move["name"].replace("-", " ").capitalize()} "
            md += f"| ![{move_data["type"]}](../assets/types/{move_data["type"]}.png){{: width='48'}} "
            md += f"| {move_data["damage_class"].capitalize()} "
            md += f"| {move_data["power"] or "—"} "
            md += f"| {move_data["accuracy"] or "—"} "
            md += f"| {move_data["pp"]} |\n"
    md += "\n"

    # TM Moves
    md += "### TM Moves\n\n"
    if len(tm_moves) == 0:
        md += f"{pokemon_name} cannot learn any TM moves.\n"
    else:
        md += "| TM | Move | Type | Cat. | Power | Acc. | PP |\n"
        md += "|----|------|------|------|-------|------|----|\n"
        for move in tm_moves:
            with open(f"moves/{move["name"]}.json", "r") as file:
                move_data = json.load(file)
            md += f"| {move_data["machines"]["black-white"]} "
            md += f"| {move["name"].replace("-", " ").capitalize()} "
            md += f"| ![{move_data["type"]}](../assets/types/{move_data["type"]}.png){{: width='48'}} "
            md += f"| {move_data["damage_class"].capitalize()} "
            md += f"| {move_data["power"] or "—"} "
            md += f"| {move_data["accuracy"] or "—"} "
            md += f"| {move_data["pp"]} |\n"
    md += "\n"

    # Egg Moves
    md += "### Egg Moves\n\n"
    if len(egg_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves by breeding.\n"
    else:
        md += "| Move | Type | Cat. | Power | Acc. | PP |\n"
        md += "|------|------|------|-------|------|----|\n"
        for move in egg_moves:
            with open(f"moves/{move["name"]}.json", "r") as file:
                move_data = json.load(file)
            md += f"| {move["name"].replace("-", " ").capitalize()} "
            md += f"| ![{move_data["type"]}](../assets/types/{move_data["type"]}.png){{: width='48'}} "
            md += f"| {move_data["damage_class"].capitalize()} "
            md += f"| {move_data["power"] or "—"} "
            md += f"| {move_data["accuracy"] or "—"} "
            md += f"| {move_data["pp"]} |\n"
    md += "\n"

    # Tutor Moves
    md += "### Tutor Moves\n\n"
    if len(tutor_moves) == 0:
        md += f"{pokemon_name} cannot learn any moves from tutors.\n"
    else:
        md += "| Move | Type | Cat. | Power | Acc. | PP |\n"
        md += "|------|------|------|-------|------|----|\n"
        for move in tutor_moves:
            with open(f"moves/{move["name"]}.json", "r") as file:
                move_data = json.load(file)
            md += f"| {move["name"].replace("-", " ").capitalize()} "
            md += f"| ![{move_data["type"]}](../assets/types/{move_data["type"]}.png){{: width='48'}} "
            md += f"| {move_data["damage_class"].capitalize()} "
            md += f"| {move_data["power"] or "—"} "
            md += f"| {move_data["accuracy"] or "—"} "
            md += f"| {move_data["pp"]} |\n"
    md += "\n"

    return md


def main():
    # pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=649").json()["results"]
    pokedex = [{"name": "eevee"}]

    for pokemon in pokedex:
        name = pokemon["name"]
        with open(f"data/{name}.json", "r") as file:
            data = json.load(file)

        md = to_md(data)
        save(f"pokemon/{name}.md", md)


if __name__ == "__main__":
    main()
