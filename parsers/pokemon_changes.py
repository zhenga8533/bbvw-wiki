from util.file import load, save


def main():
    content = load("files/Pokemon Changes.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""
    listing = False

    for i in range(n):
        line = lines[i].strip()
        line = line.replace("", "→")

        if line == "":
            if listing:
                md += "</code></pre>\n\n"
                listing = False
            continue
        elif line.startswith("#"):
            md += f"**{line}**\n\n<pre><code>"
            listing = True
        elif line.endswith("Pokémon") or line == "Evolution Changes":
            md += f"## {line}\n\n"
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
        else:
            md += f"{line}\n"
            if not listing:
                md += "\n"

    save("output/pokemon_changes.md", md)


if __name__ == "__main__":
    main()
