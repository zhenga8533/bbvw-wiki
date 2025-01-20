from util.file import load, save
import glob
import json


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

    # Adjust current moveset
    for key in move_changes:
        file_pattern = f"pokemon/{key}*.json"
        files = glob.glob(file_pattern)

        for file_path in files:
            pokemon_data = json.loads(load(file_path))
            for line in move_changes[key]:
                if line.startswith("+"):
                    pass
                elif line.startswith("-"):
                    pass
                elif line.startswith("="):
                    pass

    save("output/level_up_move_changes.md", md)


if __name__ == "__main__":
    main()
