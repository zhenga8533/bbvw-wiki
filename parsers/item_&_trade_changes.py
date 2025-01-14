from util.file import load, save
import re
import string


def main():
    content = load("files/Item & Trade Changes.txt")

    lines = content.split("\n")
    n = len(lines)
    md = "## Item Changes\n\n"
    listing = 0
    trading = False

    for i in range(n):
        line = re.sub(r"-+>", "→", lines[i]).replace("* ", "x")
        next_line = lines[i + 1] if i + 1 < n else ""

        if line == "---":  # Skip this line
            continue
        elif line == "+ + + + +":  # Start of section
            md += "---\n"
        elif line.startswith("TRADE"):  # Header
            if not trading:
                md += "## Trade Changes\n\n"
                trading = True
            md += f"#### {string.capwords(line)}\n\n```\n"
            listing = 1
        elif next_line == "---":
            md += f"#### {string.capwords(line)}\n\n```\n"
            listing = 1
        elif line == "":  # End of section
            if listing:  # Close the code block
                md += "```\n\n"
                listing = 0
            else:  # Add a new line
                md += f"{line}\n"
        else:  # Normal line
            if listing:  # Add a listing number
                md += f"{listing}. {line}\n"
                listing += 1
            else:  # Add a normal line
                md += f"{line}\n"

    if listing:
        md += "```"
    md += "\n"

    save("output/item_&_trade_changes.md", md)


if __name__ == "__main__":
    main()
