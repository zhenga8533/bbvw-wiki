from util.file import save
import requests


def main():
    pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=649").json()
    nav = ""

    for i, pokemon in enumerate(pokedex["results"]):
        name = pokemon["name"]
        nav += f'      - "#{f"{i + 1:03}"} {name.capitalize()}": pokemon/{name}.md\n'

    save("output/pokemon_nav.md", nav)


if __name__ == "__main__":
    main()
