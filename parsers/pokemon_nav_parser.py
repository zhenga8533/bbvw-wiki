from util.file import save
import requests


def main():
    pokedex = requests.get("https://pokeapi.co/api/v2/pokemon/?offset=0&limit=649").json()
    nav = ""

    generations = ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova"]
    pokedex_start = [0, 151, 251, 386, 493]

    for i, pokemon in enumerate(pokedex["results"]):
        name = pokemon["name"]
        if i in pokedex_start:
            nav += f"      - {generations[pokedex_start.index(i)]}:\n"

        nav += f'          - "#{f"{i + 1:03}"} {name.capitalize()}": pokemon/{name}.md\n'

    save("output/pokemon_nav.md", nav)


if __name__ == "__main__":
    main()
