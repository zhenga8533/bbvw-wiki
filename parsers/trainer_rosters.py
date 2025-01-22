from dotenv import load_dotenv
from util.file import load, save
from util.logger import Logger
import logging
import os
import string


def main():
    # Load environment variables and logger
    load_dotenv()
    LOG = os.getenv("LOG")
    INPUT_PATH = os.getenv("INPUT_PATH")
    OUTPUT_PATH = os.getenv("OUTPUT_PATH")
    LOG_PATH = os.getenv("LOG_PATH")
    logger = Logger("Trainer Rosters Parser", f"{LOG_PATH}trainer_rosters.log", LOG)
    content = load(f"{INPUT_PATH}Trainer Rosters.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    listing = 0

    # Parse the content
    logger.log(logging.INFO, "Parsing Trainer Rosters content")
    for i in range(n):
        next_line = lines[i + 1] if i + 1 < n else ""
        line = lines[i]
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        if line.startswith("* "):
            line = f"<b><u>{line[2:]}</u></b>"

        # Empty Lines
        if line == "---" or line == "":
            continue
        # Start of a new section
        elif next_line == "---":
            if listing:
                md += "</code></pre>\n\n"

            md += f"---\n\n## {string.capwords(line)}\n\n<pre><code>"
            listing = 1
        # Final line
        elif line.startswith("At this point"):
            md += f"</code></pre>\n\n**{line}**\n"
        # Misc lines
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
    logger.log(logging.INFO, "Trainer Rosters content parsed successfully!")

    save(f"{OUTPUT_PATH}trainer_rosters.md", md, logger)


if __name__ == "__main__":
    main()
