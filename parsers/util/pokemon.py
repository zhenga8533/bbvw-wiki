import requests


class Pokemon:
    def __init__(self, data: dict):
        """
        Initialize the Pokemon with the given data.

        :param data: The data of the Pokemon (PokeAPI v2).
        """

        # Game data
        self.game_indices = [game_index["game_index"] for game_index in data["game_indices"]]
        self.location_area_encounters = []
        self.cry = data["cries"]["legacy"]
        self.sprites = data["sprites"]["versions"]["generation-v"]["black-white"]["animated"]

        # Species data
        self.name = data["name"]
        self.id = data["id"]
        self.height = data["height"] / 10
        self.weight = data["weight"] / 10

        # Battle data
        self.abilities = [ability["ability"]["name"] for ability in data["abilities"]]
        self.moves = [
            {
                "name": move["move"]["name"],
                "level_learned_at": detail["level_learned_at"],
                "move_learn_method": detail["move_learn_method"]["name"],
            }
            for move in data["moves"]
            for detail in move["version_group_details"]
            if detail["version_group"]["name"] == "black-white"
        ]
        self.stats = {stat["stat"]["name"]: stat["base_stat"] for stat in data["stats"]}
        self.ev_yield = {stat["stat"]["name"]: stat["effort"] for stat in data["stats"]}
        self.types = [type["type"]["name"] for type in data["types"]]

        # Wild data
        self.base_experience = data["base_experience"]
        self.held_items = [
            {
                "name": held_item["item"]["name"],
                "sprite": requests.get(held_item["item"]["url"]).json()["sprites"]["default"],
                "rarity": held_item["version_details"][11]["rarity"],
            }
            for held_item in data["held_items"]
        ]

    def to_string(self) -> str:
        """
        Return the string representation of the Pokemon.

        :return: The string representation of the Pokemon.
        """

        return (
            f"{self.name} (ID: {self.id})\n"
            f"Height: {self.height} m\n"
            f"Weight: {self.weight} kg\n"
            f"Base experience: {self.base_experience}\n"
            f"Types: {', '.join(self.types)}\n"
            f"Abilities: {', '.join(self.abilities)}\n"
            f"Stats: {', '.join([f'{stat}: {value}' for stat, value in self.stats.items()])}\n"
            f"EV yield: {', '.join([f'{stat}: {value}' for stat, value in self.ev_yield.items()])}\n"
            f"Moves: {', '.join([f'{move["name"]} (level {move["level_learned_at"]}, learned by {move["move_learn_method"]})' for move in self.moves])}\n"
            f"Held items: {', '.join([f'{held_item["name"]} (rarity: {held_item["rarity"]})' for held_item in self.held_items])}\n"
            f"Game indices: {', '.join([str(game_index) for game_index in self.game_indices])}\n"
            f"Location area encounters: {', '.join(self.location_area_encounters)}\n"
            f"Cry: {self.cry}\n"
            f"Sprites: {', '.join([f'{sprite}: {url}' for sprite, url in self.sprites.items()])}"
        )

    def to_html(self) -> str:
        """
        Parses
        """

        html = ""

        return html
