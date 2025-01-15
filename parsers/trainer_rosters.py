from util.file import load, save
import re
import string


def main():
    content = load("files/Trainer Rosters.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""
    listing = 0

    for i in range(n):
        next_line = lines[i + 1] if i + 1 < n else ""
        line = lines[i]
        if line.startswith("* "):
            line = f"<b><u>{line[2:]}</u></b>"

        if line == "---" or line == "":  # Skip this line
            continue
        elif next_line == "---":
            if listing:
                md += "</code></pre>\n\n"

            md += f"#### {string.capwords(line)}\n\n<pre><code>"
            listing = 1
        elif line.startswith("At this point"):
            md += f"</code></pre>\n\n**{line}**\n"
        else:
            if listing:
                md += f"{listing}. "
                listing += 1

            if ": " in line:
                strs = line.split(": ")
                md += f"<b>{strs[0]}:</b>\n"

                pokemon = strs[1].split(", ")
                for p in pokemon:
                    md += f"   - {p}\n"
            else:
                md += f"{line}\n"

    save("output/trainer_rosters.md", md)


if __name__ == "__main__":
    main()
