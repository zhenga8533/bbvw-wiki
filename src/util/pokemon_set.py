from util.ability import get_ability
from util.format import format_id
from util.item import get_item
from util.move import get_move


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

    def to_table(self):
        """
        Convert the PokemonSet object to a table.

        :return: The PokemonSet object as a table.
        """

        id = format_id(self.species)
        table = f"| ![{self.species}](../../assets/sprites/{id}/front.png) |"
        table += f"**Lv. {self.level}** [{self.species}](../../pokemon/{id}.md/)<br>"

        # Item tooltip
        table += f"**Item:** "
        if self.item == "-":
            table += f"No Item<br>"
        else:
            item_data = get_item(self.item)
            item_effect = item_data["flavor_text_entries"].get("black-white", item_data["effect"]).replace("\n", " ")
            table += f'<span class="tooltip" title="{item_effect}">{self.item}</span><br>'

        # Ability tooltip
        table += f"**Ability:** "
        if self.ability_cln == "?":
            table += "?"
        else:
            ability_data = get_ability(self.ability_reg)
            ability_effect = (
                ability_data["flavor_text_entries"].get("black-white", ability_data["effect"]).replace("\n", " ")
            )
            table += f'<span class="tooltip" title="{ability_effect}">{self.ability_reg}</span> | '

        # Move tooltips
        for i, move in enumerate([self.move_1, self.move_2, self.move_3, self.move_4]):
            if move == "—":
                table += f"{i + 1}. —<br>"
                continue

            move_data = get_move(move)
            move_effect = move_data["flavor_text_entries"].get("black-white", move_data["effect"]).replace("\n", " ")
            table += f"{i + 1}: <span class='tooltip' title='{move_effect}'>{move}</span><br>"

        return table[:-4] + " |"
