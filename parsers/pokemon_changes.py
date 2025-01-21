from util.file import load, save
from util.format import format_animated_sprite, format_id
import glob
import json


def main():
    content = load("files/Pokemon Changes.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = False
    curr_pokemon = None
    pokemon_changes = {}

    for i in range(n):
        line = lines[i].strip()
        line = line.replace("", "→")

        if line == "":
            if listing:
                md += "</code></pre>\n\n"
                listing = False
            continue
        elif line.startswith("#"):
            md += f"**{line}**\n\n"
            pokemon = line.split(", ")

            for p in pokemon:
                num = p.split(" ")[0][1:].lstrip("0")
                md += format_animated_sprite(num) + "\n"
            md += "\n<pre><code>"

            curr_pokemon = line
            listing = True
        elif line.endswith("Pokémon") or line == "Evolution Changes":
            md += f"---\n\n## {line}\n\n"
        elif line.startswith("The following Pokémon"):
            strs = line.split(": ")
            md += f"**{strs[0]}:**\n\n```\n"

            pokemon = strs[1].split(", ")
            for i, p in enumerate(pokemon):
                md += f"{i + 1}. {p.rstrip(".")}\n"
            md += "```\n\n"
        elif listing and ": " in line:
            strs = line.split(": ")
            md += f"<b>{strs[0]}:</b> {strs[1]}\n"

            if curr_pokemon is not None:
                if curr_pokemon in pokemon_changes:
                    pokemon_changes[curr_pokemon].append(line)
                else:
                    pokemon_changes[curr_pokemon] = [line]
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"

    # Update pokemon data
    for key in pokemon_changes:
        pokemon = [format_id(p, 1) for p in key.split(", ")]
        lines = pokemon_changes[key]

        # Parse new items
        items = []
        abilities = []
        base_experience = None
        catch_rate = None
        base_happiness = None
        evolution = None
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
                ability_name = line.split(": ")[1].replace(" ", "-").lower()
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
                parts = line.split(": ")[1]
                if evolution is None:
                    evolution = parts
                else:
                    evolution += "\n" + parts

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
                stat_name = parts[0].replace(" ", "-").lower()
                new_value = int(parts[1].split(" → ")[1])
                stats[stat_name] = new_value

        for p in pokemon:
            file_pattern = f"data/{p}*.json"
            files = glob.glob(file_pattern)

            for file_path in files:
                with open(file_path, "r") as f:
                    pokemon_data = json.loads(f.read())
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

                save(file_path, json.dumps(pokemon_data, indent=4))

    save("output/pokemon_changes.md", md)


if __name__ == "__main__":
    main()
