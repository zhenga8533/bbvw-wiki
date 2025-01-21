from util.file import load, save


def main():
    content = load("files/Wild Pokemon.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    curr_location = None
    locations = []
    special_encounter = False

    for i in range(n):
        last_line = lines[i - 1] if i > 0 else ""
        line = lines[i].strip()

        if line == "" or line.startswith("="):
            if special_encounter and not last_line.endswith("Encounter"):
                md += "```\n\n"
                special_encounter = False
        elif last_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
            curr_location = line
            locations.append(line)
        elif ": " in line:
            encounter_type, encounters = line.split(": ")

            md += f"{encounter_type}\n\n"
            md += f"```\n"
            for i, encounter in enumerate(encounters.split(", ")):
                pokemon, chance = encounter.split(" (")
                chance = chance[:-2]

                md += f"{i + 1}. {pokemon} ({chance}%)\n"
            md += "```\n\n"
        elif line.endswith("Encounter"):
            md += line + "\n\n```\n"
            special_encounter = True
        elif line.startswith("* "):
            md += "```\n\n"
            special_encounter = False
            md += f"<sub><sup>_{line[2:]}_</sup></sub>\n\n"
        elif special_encounter:
            md += f"{line.rstrip(".")}\n"
        elif " – " in line:
            md += f"#### <u>{line}</u>\n\n"
        else:
            md += line + "\n\n"

    # Generate nav for mkdocs.yml
    nav = ""

    for location in locations:
        nav += f"      - {location}: wild_pokemon/{location.lower().replace(' ', '_')}.md\n"

    save("output/wild_pokemon_nav.md", nav.rstrip())
    save("output/wild_pokemon.md", md)


if __name__ == "__main__":
    main()
