import logging
import os
from util.logger import Logger


def save(file_path: str, content: str, logger: Logger) -> None:
    """
    Save the content to a file.

    :param file_path: The path to the file.
    :param content: The content to save
    :param logger: The logger object
    :return: None
    """

    dirs = file_path.split("/")[:-1]
    for dir in dirs:
        if not os.path.exists(dir):
            logger.log(logging.INFO, f"Creating directory: '{dir}'")
            os.makedirs(dir)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
            logger.log(logging.INFO, f"The content was saved to '{file_path}'.")
    except Exception as e:
        logger.log(logging.ERROR, f"An error occurred while saving to {file_path}:\n{e}")
        exit(1)


def load(file_path: str, logger: Logger) -> str:
    """
    Load the content of a file.

    :param file_path: The path to the file.
    :param logger: The logger object
    :return: The content of the file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            logger.log(logging.INFO, f"The content was loaded from '{file_path}'.")
            return content
    except FileNotFoundError:
        logger.log(logging.ERROR, f"Could not find the file '{file_path}'.")
        return ""
    except Exception as e:
        logger.log(logging.ERROR, f"An error occurred while loading '{file_path}':\n{e}")
        exit(1)
