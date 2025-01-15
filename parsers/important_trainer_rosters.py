from util.file import load, save
from util.format import clean_variable_name, parse_camel_case
from util.pokemon_set import PokemonSet


def main():
    content = load("files/Important Trainer Rosters.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = 0
    listing_type = None
    teaming = False
    pokemon_sets = []

    for i in range(n):
        next_line = lines[i + 1] if i + 1 < n else ""
        line = lines[i].strip()

        # Skip empty lines
        if line == "":
            continue
        # Start of section
        elif next_line.startswith("Battle Type"):
            # Close previous section
            if teaming:
                for p in pokemon_sets:
                    md += "\n" + p.to_string()
                pokemon_sets = []

                md += "</code></pre>\n\n"
                listing = 0

            md += f"---\n\n#### {line}\n\n<pre><code>"
            teaming = True
        elif line.startswith("Battle Type:") or line.startswith("Reward:") or line.startswith("Location:"):
            s = line.split(": ")
            md += f"<b>{s[0]}:</b> {s[1]}\n"
        elif "’s Team" in line:
            for p in pokemon_sets:
                md += "\n" + p.to_string()
            pokemon_sets = []
            listing = 1

            md += f"\n<b><u>{line}</u></b>\n"
        elif (
            line.startswith("Species")
            or line.startswith("Level")
            or line.startswith("Item")
            or line.startswith("Ability")
            or line.startswith("Move #")
        ):
            strs = line.split("\t")
            listing = 1
            listing_type = clean_variable_name(strs[0].lower())

            for s in strs[1:]:
                if listing > len(pokemon_sets):
                    pokemon_sets.append(PokemonSet())
                pokemon_sets[listing - 1].__dict__[listing_type] = parse_camel_case(s)
                listing += 1
        else:
            if listing:
                strs = line.split("\t")

                for s in strs:
                    if listing > len(pokemon_sets):
                        pokemon_sets.append(PokemonSet())
                    pokemon_sets[listing - 1].__dict__[listing_type] = parse_camel_case(s)
                    listing += 1
            else:
                md += f"{line}\n"
                if not teaming:
                    md += "\n"

    if len(pokemon_sets) > 0:
        for p in pokemon_sets:
            md += "\n" + p.to_string()
        md += "</code></pre>\n"

    save("output/important_trainer_rosters.md", md)


if __name__ == "__main__":
    main()
