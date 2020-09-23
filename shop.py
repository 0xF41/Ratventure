

class Player:
    def __init__(self, gold):
        self.gold = gold


class Gear:
    def __init__(self, attack, defence, gold):
        self.attack = attack
        self.defence = defence
        self.gold = gold

    def __str__(self):
        return f"[ATTACK: {self.attack} | DEFENCE: {self.defence} | PRICE: {self.gold}"


class Shop:
    def __init__(self):
        self.list_of_gear = []

    def add_gear(self, gear_obj: Gear):
        self.list_of_gear.append(gear_obj)

    def list_shop_menu(self):
        pass

    def buy_gear(self):
        pass
