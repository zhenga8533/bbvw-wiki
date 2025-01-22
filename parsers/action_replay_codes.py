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
    logger = Logger("Action Replay Codes Parser", f"{LOG_PATH}action_replay_codes.log", LOG)
    content = load(f"{INPUT_PATH}Action Replay Codes.txt", logger)

    # Set up variables
    lines = content.split("\n")
    n = len(lines)
    md = ""

    game_ids = {}
    game_version = None

    parse_code = False
    codes = {}
    code_data = {
        "name": None,
        "description": None,
        "blaze_black": "",
        "volt_white": "",
    }

    # Parse the content
    logger.log(logging.INFO, "Parsing Action Replay Code content")
    for i in range(n):
        line = lines[i].strip()
        logger.log(logging.DEBUG, f"Processing line {i + 1}/{n}")

        # Empty Lines
        if line == "":
            code_name = code_data["name"]
            if code_data["name"] is not None:
                if code_data["name"] not in codes:
                    codes[code_name] = code_data
                else:
                    codes[code_name]["blaze_black"] += code_data["blaze_black"]
                    codes[code_name]["volt_white"] += code_data["volt_white"]

                code_data = {
                    "name": None,
                    "description": None,
                    "blaze_black": "",
                    "volt_white": "",
                }
        # Pokémon Game IDs
        elif line.startswith("Pokémon"):
            game_version = "_".join(line.split(" ")[1:]).lower()
            game_ids[game_version] = f"### {line}\n\n"
            parse_code = True
        elif line.startswith("Game ID (Full)"):
            game_ids[game_version] += f"```\n{line}\n"
        elif line.startswith("Game ID (Clean)"):
            game_ids[game_version] += f"{line}\n```\n\n"
        # Action Replay Codes
        elif parse_code:
            if code_data["name"] is None:
                code_data["name"] = line
            elif all(c.isupper() or c.isdigit() or c.isspace() for c in line):
                code_data[game_version] += f"{line}<br>"
            else:
                code_data["description"] = line
        # Misc lines
        else:
            md += line + "\n\n"
    logger.log(logging.INFO, "Action Replay Code content parsed successfully!")

    # Save the parsed content
    md += "---\n\n## Game IDs\n\n"
    md += game_ids["blaze_black"]
    md += game_ids["volt_white"]
    md += "---\n\n## Action Replay Codes\n\n"

    # Format codes into Markdown tables
    for code in codes:
        code_data = codes[code]
        code_name = code_data["name"]
        code_desc = code_data["description"]
        code_bb = code_data["blaze_black"]
        code_vw = code_data["volt_white"]

        md += f"### {code_name}\n\n"
        if code_desc is not None:
            md += f"{code_desc}\n\n"
        md += "| Blaze Black | Volt White |\n"
        md += "|-------------|------------|\n"
        md += f"| <pre>{code_bb}</pre> | <pre>{code_vw}</pre> |\n\n"

    save(f"{OUTPUT_PATH}action_replay_codes.md", md, logger)


if __name__ == "__main__":
    main()
