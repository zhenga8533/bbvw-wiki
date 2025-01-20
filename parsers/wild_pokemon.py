from util.file import load, save


def main():
    content = load("files/Wild Pokemon.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""
    encounter = False
    encountered = False
    special = False

    for i in range(n):
        last_line = lines[i - 1] if i > 0 else ""
        line = lines[i].strip()

        if last_line.startswith("="):
            if encounter:
                md += "</code></pre>\n\n"
            if special:
                md += "```\n\n"

            md += f"\n---\n\n## {line}\n\n<pre><code>"
            encounter = True
            encountered = False
            special = False
        elif line.startswith("=") or line == "":
            continue
        elif line.endswith("Encounter"):
            if special:
                md += "```\n\n"

            md += "</code></pre>\n\n"
            md += f"**{line}**\n```\n"

            special = True
            encounter = False
        elif special and line.startswith("* "):
            md += "```\n"
            md += f"\n<sub><sup>_{line[2:]}_</sub></sup>\n\n"

            special = False
        elif line.startswith("There are no Wild Pokemon"):
            md += f"```\n{line}\n"
            special = False
        elif encounter or special:
            if ": " in line:
                if encountered:
                    md += "\n"

                strs = line.split(": ")
                md += f"<b>{strs[0]}:</b>\n"

                pokemon = strs[1].split(", ")
                for i, p in enumerate(pokemon):
                    md += f"{i + 1}. {p}\n"
                encountered = True
            else:
                md += f"{line}\n"
        else:
            md += f"{line}\n\n"

    save("output/wild_pokemon.md", md)


if __name__ == "__main__":
    main()
