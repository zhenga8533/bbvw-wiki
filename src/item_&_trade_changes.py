from dotenv import load_dotenv
from util.file import load, save
from util.logger import Logger
import logging
import os


def main():
    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Item & Trade Changes Parser", f"{LOG_PATH}item_trade_changes.log", LOG)
    content = load(f"{INPUT_PATH}Item & Trade Changes.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    parse_locations = False

    # Parse the content
    logger.log(logging.INFO, "Parsing Item & Trade Changes content")
    for i in range(n):
        line = lines[i].strip()
        line = line.replace("* ", "x")
        line = line.replace("�", "e")
        line = line.replace("Poke Ball", "Poké Ball")
        next_line = lines[i + 1].strip() if i + 1 < n else ""
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "---" or line == "":
            continue
        # Start of trade changes
        elif line == "-------------":
            save(f"{OUTPUT_PATH}item_changes.md", md, logger)
            md = ""
            parse_locations = False
        # "Use" item changes
        elif line.endswith(":"):
            md += f"**{line}**\n\n"
        # Item changes header
        elif next_line == "---":
            parse_locations = True

            md += f"\n---\n\n## {line}\n"
            md += "| Old Item | New Item |\n"
            md += "|----------|----------|\n"
        # Item changes table
        elif parse_locations:
            items = line.split(" -> ")
            md += f"| {items[0]} | {items[1]} |\n"
        elif line.startswith("TRADE #"):
            md += f"\n---\n\n## {line.title()}\n\n"
            md += f"|   | Give | Receive |\n"
            md += f"|---|------|---------|\n"
        # Trade changes
        elif line.startswith("Original") or line.startswith("New"):
            sections = line.split(": ")
            category = sections[0]
            trade = sections[1].split(" -> ")
            md += f"| {category} | {trade[0]} | {trade[1]} |\n"
        # Misc changes
        else:
            md += line + "\n"
    logger.log(logging.INFO, "Item & Trade Changes parsed successfully!")

    save(f"{OUTPUT_PATH}trade_changes.md", md, logger)


if __name__ == "__main__":
    main()
