from util.file import load, save


def main():
    content = load("files/Item & Trade Changes.txt")

    lines = content.split("\n")
    n = len(lines)
    md = ""

    parse_locations = False

    for i in range(n):
        line = lines[i].strip()
        line = line.replace("* ", "x")
        line = line.replace("�", "e")
        line = line.replace("Poke Ball", "Poké Ball")
        next_line = lines[i + 1].strip() if i + 1 < n else ""

        if line == "---" or line == "":
            continue
        elif line == "-------------":
            save("output/item_changes.md", md)
            md = ""
            parse_locations = False
        elif line.endswith(":"):
            md += f"**{line}**\n\n"
        elif next_line == "---":
            parse_locations = True

            md += f"\n---\n\n## {line}\n"
            md += "| Old Item | New Item |\n"
            md += "|----------|----------|\n"
        elif parse_locations:
            items = line.split(" -> ")
            md += f"| {items[0]} | {items[1]} |\n"
        elif line.startswith("TRADE #"):
            md += f"\n---\n\n## {line.title()}\n\n"
            md += f"|   | Give | Receive |\n"
            md += f"|---|------|---------|\n"
        elif line.startswith("Original") or line.startswith("New"):
            sections = line.split(": ")
            category = sections[0]
            trade = sections[1].split(" -> ")
            md += f"| {category} | {trade[0]} | {trade[1]} |\n"
        else:
            md += line + "\n"

    save("output/trade_changes.md", md)


if __name__ == "__main__":
    main()
