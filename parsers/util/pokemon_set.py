class PokemonSet:
    def __init__(self):
        self.species = "-"
        self.level = "0"
        self.item = "-"
        self.ability_reg = "-"
        self.ability_cln = "-"
        self.move_1 = "-"
        self.move_2 = "-"
        self.move_3 = "-"
        self.move_4 = "-"

    def to_string(self):
        s = f"<b>{self.species}</b> @ {self.item if self.item != "-" else "No Item"}\n"
        s += f"<b>Ability:</b> {self.ability_reg if self.ability_reg != "-" else "?"}\n"
        s += f"<b>Level:</b> {self.level}\n"
        if self.move_1 != "-" or self.move_2 != "-" or self.move_3 != "-" or self.move_4 != "-":
            s += f"<b>Moves:</b>\n"
            s += f"1. {self.move_1}\n"
            s += f"2. {self.move_2}\n"
            s += f"3. {self.move_3}\n"
            s += f"4. {self.move_4}\n"
        return s
