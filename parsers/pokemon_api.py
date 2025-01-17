from util.file import save
from util.pokemon import Pokemon
import requests


def fetch_pokemon_varieties(num: int) -> list:
    """
    Fetch from the Pokemon API the varieties of the Pokemon with the given number.

    :param num: The number of the Pokemon to fetch.
    :return: The varieties of the Pokemon with the given number.
    """

    url = f"https://pokeapi.co/api/v2/pokemon-species/{num}"
    response = requests.get(url)
    data = response.json()

    varieties = [variety["pokemon"]["name"] for variety in data["varieties"]]
    return varieties


def fetch_pokemon_data(name: str) -> dict:
    """
    Fetch from the Pokemon API the data of the Pokemon with the given name.

    :param name: The name of the Pokemon to fetch.
    :return: The data of the Pokemon with the given name.
    """

    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    response = requests.get(url)
    data = response.json()
    return data


def main():
    start = 494
    end = 494

    for i in range(start, end + 1):
        varieties = fetch_pokemon_varieties(i)

        for variety in varieties:
            data = fetch_pokemon_data(variety)
            pokemon = Pokemon(data)
            save(f"pokemon/{pokemon.name}.md", pokemon.to_html())


if __name__ == "__main__":
    main()
