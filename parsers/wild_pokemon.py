from util.file import load, save


def main():
    content = load("files/Wild Pokemon.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    locations = []
    special_encounter = False

    curr_location = None
    location_md = ""

    for i in range(n):
        last_line = lines[i - 1] if i > 0 else ""
        line = lines[i].strip()

        if line == "" or line.startswith("="):
            if special_encounter and not last_line.endswith("Encounter"):
                md += "```\n\n"
                special_encounter = False
        elif last_line.startswith("="):
            md += f"---\n\n## {line}\n\n"
            if location_md != "" and curr_location != "Black City / White Forest":
                save(f"wild_encounters/{curr_location.lower().replace(' ', '-')}.md", location_md)

            location_md = "| Pokémon | Encounter Type | Chance |\n| --- | --- | --- |\n"
            curr_location = line
            locations.append(line)
        elif ": " in line:
            encounter_type, encounters = line.split(": ")
            encounters = encounters.split(", ")

            md += f"{encounter_type}\n\n"
            md += f"```\n"
            for i, encounter in enumerate(encounters):
                pokemon, chance = encounter.split(" (")
                chance = chance.rstrip(")")

                # Add data to base md
                md += f"{i + 1}. {pokemon} ({chance})\n"

                # Add data to wild encounter md
                pokemon_id = (
                    "".join(char for char in pokemon if char.isalnum() or char.isspace()).replace(" ", "-").lower()
                )
                location_md += f"| [{pokemon}](../pokemon/{pokemon_id}.md/) | {encounter_type} | {chance} |\n"
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

            if location_md.endswith("| --- | --- | --- |\n"):
                location_md = f"## {line}\n\n"
            else:
                location_md += f"\n## {line}\n\n"
            location_md += f"| Pokémon | Encounter Type | Chance |\n| --- | --- | --- |\n"
        else:
            md += line + "\n\n"

    # Generate nav for mkdocs.yml
    nav = ""

    for location in locations:
        if "/" in location:
            continue
        nav += f"      - {location}: wild_encounters/{location.lower().replace(' ', '-')}.md\n"

    save(f"wild_encounters/{curr_location.lower().replace(' ', '-')}.md", location_md)
    save("output/wild_encounters_nav.md", nav.rstrip())
    save("output/wild_pokemon.md", md)


if __name__ == "__main__":
    main()
