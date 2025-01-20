from util.file import load, save
import glob
import json
import re


def main():
    content = load("files/Level Up Move Changes.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = False
    curr_pokemon = None
    move_changes = {}

    for i in range(n):
        line = lines[i].strip()

        if line == "":
            if listing:
                md += "```\n\n"
                listing = False
        elif line.startswith("#"):
            md += f"**{line}**\n\n```\n"
            curr_pokemon = line.split(" ")[1].replace(" ", "-").lower()
            listing = True
        elif line.endswith("Pokémon"):
            md += f"---\n\n## {line}\n\n"
        elif line == "Key" or line == "General Attack Changes":
            md += f"---\n\n## {line}\n\n```\n"
            listing = True
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"

            if curr_pokemon is not None:
                if curr_pokemon in move_changes:
                    move_changes[curr_pokemon].append(line)
                else:
                    move_changes[curr_pokemon] = [line]
            elif line.startswith("• "):
                match = re.match(r"• (.+) is now (\d+) power\.", line)
                if match:
                    move_name, power = match.groups()
                    move_name = move_name.replace(" ", "-").lower()
                    move_data = json.loads(load(f"moves/{move_name}.json"))
                    move_data["power"] = int(power)
                    save(f"moves/{move_name}.json", json.dumps(move_data, indent=4))

    # Adjust current moveset
    for key in move_changes:
        file_pattern = f"data/{key}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            pokemon_data = json.loads(load(file_path))
            moves = pokemon_data["moves"].get("black-white", None)
            if moves is None:
                continue

            for line in move_changes[key]:
                parts = line.split(" ")
                level = int(parts[2])
                name = "-".join(parts[4:]).lower()
                move_index = next(
                    (
                        i
                        for i, move in enumerate(moves)
                        if move["name"].replace(" ", "").lower() == name.replace(" ", "").lower()
                    ),
                    None,
                )

                if line.startswith("+"):
                    if move_index is not None:
                        moves[move_index]["level_learned_at"] = level
                        moves[move_index]["learn_method"] = "level-up"
                    else:
                        moves.append({"name": name, "level_learned_at": level, "learn_method": "level-up"})
                elif line.startswith("-"):
                    replace_index = next(
                        (i for i, move in enumerate(moves) if move["level_learned_at"] == level), None
                    )
                    if replace_index is not None:
                        moves[replace_index]["name"] = name
                    else:
                        print(f"Could not find move at level {level} for {key}")
                elif line.startswith("="):
                    if move_index is not None:
                        moves[move_index]["level_learned_at"] = level
                    else:
                        print(f"Could not find move {name} for {key}")

            save(file_path, json.dumps(pokemon_data, indent=4))

    save("output/level_up_move_changes.md", md)


if __name__ == "__main__":
    main()
