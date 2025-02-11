from util.ability import get_ability
from util.file import download_file, load
from util.format import find_pokemon_sprite, format_id
from util.item import get_item
from util.logger import Logger
from util.move import get_move
import json
import os


class PokemonSet:
    def __init__(self):
        """
        Track the details of a Pokemon set to format into a markdown element.

        :return: None
        """

        self.species = None
        self.level = "0"
        self.item = "-"
        self.ability_reg = "?"
        self.ability_cln = "?"
        self.move_1 = "—"
        self.move_2 = "—"
        self.move_3 = "—"
        self.move_4 = "—"

    def to_string(self):
        """
        Convert the PokemonSet object to a string.

        :return: The PokemonSet object as a string.
        """

        id = format_id(self.species)
        s = f"<a href='/bbvw-wiki/pokemon/{id}/'><b>{self.species}</b></a> @ "
        s += (self.item if self.item != "-" else "No Item") + "\n"
        s += f"<b>Ability:</b> {self.ability_reg}\n"
        s += f"<b>Level:</b> {self.level}\n"
        if self.move_1 != "—" or self.move_2 != "—" or self.move_3 != "—" or self.move_4 != "—":
            s += f"<b>Moves:</b>\n"
            s += f"1. {self.move_1}\n"
            s += f"2. {self.move_2}\n"
            s += f"3. {self.move_3}\n"
            s += f"4. {self.move_4}\n"
        return s

    def to_table(self, logger: Logger):
        """
        Convert the PokemonSet object to a table.

        :return: The PokemonSet object as a table.
        """

        # Load Pokemon data
        POKEMON_INPUT_PATH = os.getenv("POKEMON_INPUT_PATH")
        pokemon_id = format_id(self.species)
        pokemon_data = json.loads(load(POKEMON_INPUT_PATH + pokemon_id + ".json", logger))
        pokemon_types = pokemon_data["types"]

        # Create the table
        pokemon_sprite = find_pokemon_sprite(pokemon_id, "front", logger).replace("../", "../../")
        table = f"| {pokemon_sprite} | "
        table += f"**Lv. {self.level}** [{self.species}](../../pokemon/{pokemon_id}.md/)<br>"

        # Ability tooltip
        table += f"**Ability:** "
        if self.ability_cln == "?":
            table += "?<br>"
        else:
            ability_data = get_ability(self.ability_reg)
            ability_effect = (
                ability_data["flavor_text_entries"].get("black-white", ability_data["effect"]).replace("\n", " ")
            )
            table += f'<span class="tooltip" title="{ability_effect}">{self.ability_reg}</span><br>'

        # Type tooltip
        table += " ".join(f'![{t}](../../assets/types/{t}.png "{t.title()}"){{: width="48"}}' for t in pokemon_types)
        table += " | "

        # Item tooltip
        if self.item == "-":
            table += f"No Item | "
        else:
            item_data = get_item(self.item)
            item_effect = item_data["flavor_text_entries"].get("black-white", item_data["effect"]).replace("\n", " ")
            item_path = f"../docs/assets/items/{item_data['name']}.png"
            if not os.path.exists(item_path):
                download_file(item_path, item_data["sprite"], logger)

            table += f'![{self.item}]({item_path.replace("docs", "..")} "{self.item}")<br>'
            table += f'<span class="tooltip" title="{item_effect}">{self.item}</span> | '

        # Move tooltips
        for i, move in enumerate([self.move_1, self.move_2, self.move_3, self.move_4]):
            if move == "—":
                table += f"{i + 1}. —<br>"
                continue

            move_data = get_move(move)
            move_effect = move_data["flavor_text_entries"].get("black-white", move_data["effect"]).replace("\n", " ")
            table += f"{i + 1}: <span class='tooltip' title='{move_effect}'>{move}</span><br>"

        return table[:-4] + " |"
