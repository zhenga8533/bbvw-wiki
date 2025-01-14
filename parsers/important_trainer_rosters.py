from util.file import load, save
from util.format import replace_last


def main():
    content = load("files/Important Trainer Rosters.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = 0
    teaming = False

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
                md += "</code></pre>\n\n"
                listing = 0
            md += f"#### {line}\n\n<pre><code>\n"
            teaming = True
        elif line.startswith("Battle Type:") or line.startswith("Reward:") or line.startswith("Location:"):
            s = line.split(": ")
            md += f"<b>{s[0]}:</b> {s[1]}\n"
        elif "’s Team" in line:
            md += f"\n<b><u>{line}</u></b>\n"
        elif line.startswith("Species"):
            md += "\n<b>Species:</b>\n"
            listing = 1

            species = line.split("\t")[1:]
            for s in species:
                md += f"{listing}. {s}\n"
                listing += 1
        elif line.startswith("Level"):
            md += "\n<b>Levels:</b>\n"
            listing = 1

            levels = line.split("\t")[1:]
            for level in levels:
                md += f"{listing}. {level}\n"
                listing += 1
        elif line.startswith("Item"):
            md += "\n<b>Items:</b>\n"
            listing = 1

            items = line.split("\t")[1:]
            for item in items:
                md += f"{listing}. {item}\n"
                listing += 1
        elif line.startswith("Ability"):
            md += "\n<b>Abilities:</b>\n"
            listing = 1

            abilities = line.split("\t")[1:]
            for ability in abilities:
                md += f"{listing}. {ability}\n"
                listing += 1
        elif line.startswith("Move #"):
            moves = line.split("\t")
            md += f"\n<b>{moves[0]}</b>\n"
            listing = 1

            for move in moves[1:]:
                md += f"{listing}. {move}\n"
                listing += 1
        else:
            if listing:
                strs = line.split("\t")

                for s in strs:
                    if s.startswith("(") and s.endswith(")"):
                        replace_last(s, ":</b>", f" {s}</b>")
                        continue
                    md += f"{listing}. {s}\n"
                    listing += 1
            else:
                md += f"{line}\n"

    save("output/important_trainer_rosters.md", md)


if __name__ == "__main__":
    main()
