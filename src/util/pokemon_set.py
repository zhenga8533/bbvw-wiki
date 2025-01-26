from util.format import format_id, split_camel_case


class PokemonSet:
    def __init__(self):
        """
        Track the details of a Pokemon set to format into a markdown element.

        :return: None
        """

        self.species = None
        self.level = "0"
        self.item = "No Item"
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
        s += (split_camel_case(self.item) if self.item != "-" else "No Item") + "\n"
        s += f"<b>Ability:</b> {split_camel_case(self.ability_reg)}\n"
        s += f"<b>Level:</b> {self.level}\n"
        if self.move_1 != "—" or self.move_2 != "—" or self.move_3 != "—" or self.move_4 != "—":
            s += f"<b>Moves:</b>\n"
            s += f"1. {split_camel_case(self.move_1)}\n"
            s += f"2. {split_camel_case(self.move_2)}\n"
            s += f"3. {split_camel_case(self.move_3)}\n"
            s += f"4. {split_camel_case(self.move_4)}\n"
        return s

    def to_table(self):
        """
        Convert the PokemonSet object to a table.

        :return: The PokemonSet object as a table.
        """

        id = format_id(self.species)
        table = f"| ![{self.species}](../../assets/sprites/{id}/front.png) |"
        table += f"[{self.species}](../../pokemon/{id}.md/) Lv. {self.level}<br>"
        item = split_camel_case(self.item) if self.item != "-" else "No Item"
        table += f"**Item:** {item}<br>"
        table += f"**Ability:** {split_camel_case(self.ability_reg)} | "
        table += f"1. {split_camel_case(self.move_1)}<br>"
        table += f"2. {split_camel_case(self.move_2)}<br>"
        table += f"3. {split_camel_case(self.move_3)}<br>"
        table += f"4. {split_camel_case(self.move_4)} |"

        return table
