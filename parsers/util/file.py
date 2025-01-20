import os


def save(file_path: str, content: str) -> None:
    """
    Save the content to a file.

    :param file_path: The path to the file.
    :param content: The content to save
    :return: None
    """

    dirs = file_path.split("/")[:-1]
    for dir in dirs:
        if not os.path.exists(dir):
            os.makedirs(dir)

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
            print(f"The content was saved to {file_path}.")
    except Exception as e:
        print(f"An error occurred while saving to {file_path}: {e}")
        exit(1)


def load(file_path: str) -> str:
    """
    Load the content of a file.

    :param file_path: The path to the file.
    :return: The content of the file.
    """

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            print(f"The content was loaded from {file_path}.")
            return content
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
        exit(1)
    except Exception as e:
        print(f"An error occurred while loading {file_path}: {e}")
        exit(1)
