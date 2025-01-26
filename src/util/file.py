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

    # Create the directory if it does not exist
    directory = file_path.rsplit("/", 1)[0]
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.log(logging.INFO, f"Created directory '{directory}'.")

    # Save the content to the file
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
        # Load the content of the file into a string
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


def verify_asset_path(asset_path: str, logger: Logger) -> None:
    """
    Verify that the asset path exists.

    :param asset_path: The path to the asset.
    :param logger: The logger object
    :return: None
    """

    check_path = "../docs/" + asset_path.lstrip("../")
    if os.path.exists(check_path):
        logger.log(logging.INFO, f"Asset found at {check_path}")
        return True
    else:
        logger.log(logging.WARNING, f"Asset does not exist at {check_path}")

    return False
