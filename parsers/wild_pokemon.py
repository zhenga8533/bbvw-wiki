from util.file import load, save
from util.format import remove_special_characters
import json


def main():
    content = load("files/Wild Pokemon.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    locations = []
    special_encounter = False

    curr_location = None
    location_md = ""
    location_header = "| Sprite | Pokémon | Encounter Type | Chance |\n| :---: | --- | :---: | --- |\n"

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

            location_md = location_header
            curr_location = line
            locations.append(line)
        elif ": " in line:
            encounter_type, encounters = line.split(": ")
            encounters = encounters.split(", ")

            md += f"{encounter_type}\n\n"
            md += f"```\n"
            location_md = location_md.rstrip(location_header) + f"\n\n### {encounter_type}\n\n"

            if not location_md.endswith(location_header):
                location_md += f"\n{location_header}"

            for i, encounter in enumerate(encounters):
                pokemon, chance = encounter.split(" (")
                chance = chance.rstrip(")")

                # Add data to base md
                md += f"{i + 1}. {pokemon} ({chance})\n"

                # Add data to wild encounter md
                pokemon_id = remove_special_characters(pokemon).replace(" ", "-").lower()
                pokemon_data = json.loads(load(f"data/{pokemon_id}.json") or "{}")
                pokemon_sprite = (
                    pokemon_data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]["front_default"]
                    if pokemon_data != {}
                    else ""
                )
                encounter_id = remove_special_characters(encounter_type).replace(" ", "_").lower()

                location_md += f"| ![{pokemon}]({pokemon_sprite}) "
                location_md += f"| [{pokemon}](../pokemon/{pokemon_id}.md/) "
                location_md += f"| ![{encounter_type}](../assets/encounter_types/{encounter_id}.png){{: style='max-width: 24px;' }} "
                location_md += f"| {chance} |\n"

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

            location_md = location_md.rstrip(location_header) + f"\n\n---\n\n## {line}\n\n"
            location_md += location_header
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
