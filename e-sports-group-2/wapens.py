from ControllerFunctions import show_xp_controller


class Wapen:
    def __init__(self, naam, kosten, schade, afbeelding):
        self.naam = naam
        self.kosten = kosten
        self.schade = schade
        self.afbeelding = afbeelding

# Maak een lijst van wapens
wapens = [
    Wapen("level1_stok", 0, 25, "resources/Sprites/level1_stok.png"),
    Wapen("level2_stok", 50, 50, "resources/Sprites/level2_stok.png"),
    Wapen("level3_stok", 100, 100, "resources/Sprites/level3_stok.png"),
]


class Speler:
    def __init__(self):
        self.xp = 0  # Bijvoorbeeld, stel de XP in
        self.huidig_wapen_index = 0
        self.xp_veranderd = False
        self.inventory = {} # Initialize an empty inventory
        self.weapon_inventory = {}


    def add_to_inventory(self, item, quantity=1):
        """Add a specified quantity of an item to the inventory."""
        if item in self.inventory:
            self.inventory[item] += quantity
        else:
            self.inventory[item] = quantity
        print(f"{quantity} {item}(s) added to inventory.")

    def add_weapon_to_inventory(self, weapon, quantity=1):
        """Add a weapon to the weapon inventory."""
        if weapon in self.weapon_inventory:
            self.weapon_inventory[weapon] += quantity
        else:
            self.weapon_inventory[weapon] = quantity
        print(f"{weapon.naam} added to weapon inventory with quantity {quantity}.")

    def has_item(self, item):
        """Check if the item is in the inventory."""
        return item in self.inventory and self.inventory[item] > 0

    def remove_from_inventory(self, item, quantity=1):
        """Remove a specified quantity of an item, if it exists and enough quantity is available."""
        if self.has_item(item):
            if self.inventory[item] >= quantity:
                self.inventory[item] -= quantity
                print(f"{quantity} {item}(s) removed from inventory.")
                # Remove the item entirely if quantity goes to 0
                if self.inventory[item] == 0:
                    del self.inventory[item]
            else:
                print(f"Not enough {item} to remove.")
        else:
            print(f"{item} not found in inventory.")

    def delete_inventory(self):
        self.inventory = {}
        print("Inventory deleted.")

    def view_inventory(self):
        """Print the items and quantities in the inventory."""
        if self.inventory:
            print("Inventory:")
            for item, quantity in self.inventory.items():
                print(f"{item}: {quantity}")
        else:
            print("Inventory is empty.")

    def increase_xp(self, nieuwe_xp):
        self.xp += nieuwe_xp
        self.xp_veranderd = True  # Markeer dat de XP is veranderd
        show_xp_controller(self.xp)


    def decrease_xp(self, nieuwe_xp):
        self.xp -= nieuwe_xp
        self.xp_veranderd = True  # Markeer dat de XP is veranderd


    def kies_wapen(self, index):
        # Controleer of het wapen kan worden gekocht met beschikbare XP
        wapen = wapens[index]
        if self.xp >= wapen.kosten:
            self.huidig_wapen_index=index
            return True, wapen
        else:
            return False, None
    def huidig_wapen(self):
        return wapens[self.huidig_wapen_index]

    def sell_sushi(self):
        """Sell all sushi in the inventory and add XP based on the type of sushi."""
        sushi_xp_values = {
            "sushiroll1.png": 1,
            "sushiroll2.png": 1,
            "Sushiroll3.png": 3,
            "Sushiroll6.png": 3
        }

        total_xp = 0
        for sushi, xp_value in sushi_xp_values.items():
            if sushi in self.inventory:
                quantity = self.inventory[sushi]
                total_xp += quantity * xp_value
                self.remove_from_inventory(sushi, quantity)  # Remove all of this sushi type
                print(f"Sold {quantity} {sushi} for {quantity * xp_value} XP.")

        self.xp += total_xp
        self.xp_veranderd = True
        print(f"Total XP earned: {total_xp}. Current XP: {self.xp}.")



