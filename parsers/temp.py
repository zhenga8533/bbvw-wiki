import os
import json
import requests

# Path to the directory containing all the Pokémon files
path = "data"

# Loop through all files in the directory
for filename in os.listdir(path):

    file_path = os.path.join(path, filename)

    # Open and parse the JSON file
    with open(file_path, "r") as file:
        data = json.load(file)

    sprites = data.get("sprites", {})
    name = data.get("name", "unknown_pokemon")

    # Directory to save the images
    output_directory = f"sprites/{name}"
    os.makedirs(output_directory, exist_ok=True)

    # Define the URLs to download
    official_artwork = sprites.get("other", {}).get("official-artwork", {}).get("front_default")
    shiny_artwork = sprites.get("other", {}).get("official-artwork", {}).get("front_shiny")
    black_white = sprites.get("versions", {}).get("generation-v", {}).get("black-white", {})
    front = black_white.get("front_default")
    front_female = black_white.get("front_female")
    back = black_white.get("back_default")
    back_female = black_white.get("back_female")
    front_shiny = black_white.get("front_shiny")
    front_shiny_female = black_white.get("front_shiny_female")
    back_shiny = black_white.get("back_shiny")
    back_shiny_female = black_white.get("back_shiny_female")

    animated = sprites.get("versions", {}).get("generation-v", {}).get("black-white", {}).get("animated", {})
    animated_front = animated.get("front_default")
    animated_front_female = animated.get("front_female")
    animated_back = animated.get("back_default")
    animated_back_female = animated.get("back_female")
    animated_shiny_front = animated.get("front_shiny")
    animated_front_shiny_female = animated.get("front_shiny_female")
    animated_shiny_back = animated.get("back_shiny")
    animated_back_shiny_female = animated.get("back_shiny_female")

    # List of URLs with corresponding file names
    images = [
        (official_artwork, f"official_artwork.png"),
        (shiny_artwork, f"official_artwork_shiny.png"),
        (front, f"front.png"),
        (front_female, f"front_female.png"),
        (back, f"back.png"),
        (back_female, f"back_female.png"),
        (front_shiny, f"front_shiny.png"),
        (front_shiny_female, f"front_shiny_female.png"),
        (back_shiny, f"back_shiny.png"),
        (back_shiny_female, f"back_shiny_female.png"),
        (animated_front, f"front.gif"),
        (animated_front_female, f"front_female.gif"),
        (animated_back, f"back.gif"),
        (animated_back_female, f"back_female.gif"),
        (animated_shiny_front, f"front_shiny.gif"),
        (animated_front_shiny_female, f"front_shiny_female.gif"),
        (animated_shiny_back, f"back_shiny.gif"),
        (animated_back_shiny_female, f"back_shiny_female.gif"),
    ]

    # Download and save each image
    for url, file_name in images:
        if url:  # Check if URL is valid (not None)
            response = requests.get(url)
            if response.status_code == 200:
                save_path = os.path.join(output_directory, file_name)
                with open(save_path, "wb") as img_file:
                    img_file.write(response.content)
                print(f"Saved {file_name} to {save_path}")
            else:
                print(f"Failed to download {url}. Status code: {response.status_code}")

    latest_cry = data["cry_latest"]
    legacy_cry = data["cry_legacy"]

    # Download the latest cry
    os.makedirs(f"cries/{name}", exist_ok=True)
    if latest_cry:
        response = requests.get(latest_cry)
        if response.status_code == 200:
            save_path = os.path.join(f"cries/{name}", "latest.ogg")
            with open(save_path, "wb") as cry_file:
                cry_file.write(response.content)
            print(f"Saved latest cry to {save_path}")
        else:
            print(f"Failed to download {latest_cry}. Status code: {response.status_code}")
    if legacy_cry:
        response = requests.get(legacy_cry)
        if response.status_code == 200:
            save_path = os.path.join(f"cries/{name}", "legacy.ogg")
            with open(save_path, "wb") as cry_file:
                cry_file.write(response.content)
            print(f"Saved legacy cry to {save_path}")
        else:
            print(f"Failed to download {legacy_cry}. Status code: {response.status_code}")
