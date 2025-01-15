from util.file import load, save
import re
import string


def main():
    content = load("files/Level Up Move Changes.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""
    listing = False

    for i in range(n):
        line = lines[i].strip()

        if line == "":
            if listing:
                md += "```\n\n"
                listing = False
            continue
        elif line.startswith("#"):
            md += f"**{line}**\n\n```\n"
            listing = True
        elif line.endswith("Pokémon"):
            md += f"## {line}\n\n"
        elif line == "Key" or line == "General Attack Changes":
            md += f"## {line}\n\n```\n"
            listing = True
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"

    save("output/level_up_move_changes.md", md)


if __name__ == "__main__":
    main()
