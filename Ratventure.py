from os import system, path, listdir, walk
import random
import pickle


# Map object to generate the map for the game session


class Map():
    def __init__(self):
        self.TOWNS_MAX_NUM = 5  # Number of towns
        self.GRID_LENGTH = 8  # Map Size

        # Static Coordinates (Orb, Rat King)
        self.orb_coordinate = (0, 0)
        self.RAT_KING = (self.GRID_LENGTH - 1, self.GRID_LENGTH - 1)

        self.generate_map_objects()  # generate coordinates of map objects

    # Generate map stuff coordinates and add it to the map_object_coords list
    def generate_map_objects(self):
        self.towns = []  # Coordinate of towns
        # Coordinate of all map objects (towns, orb, ratking)
        self.map_object_coords = []
        self.generate_town_tile_coords()
        self.add_list_of_tile_coords(self.towns)
        self.add_list_of_tile_coords(self.RAT_KING)
        self.generate_orb_tile_coord()
        self.add_list_of_tile_coords(self.orb_coordinate)

    # Generate towns " T " on grid
    def generate_town_tile_coords(self):
        self.towns.append((0, 0))
        while len(self.towns) != self.TOWNS_MAX_NUM:
            town_coord = self.generate_coord()
            if town_coord not in self.towns and town_coord != self.RAT_KING:
                self.towns.append(town_coord)
        return self.towns

    # Generate orb coordinate on grid
    def generate_orb_tile_coord(self):
        while self.orb_coordinate in self.map_object_coords:
            self.orb_coordinate = self.generate_coord()

    # Returns a coordinate (x, y)
    def generate_coord(self) -> tuple:
        return (random.randint(0, self.GRID_LENGTH - 1),
                random.randint(0, self.GRID_LENGTH - 1))

    # Adds coordinates into map_object_coords
    def add_list_of_tile_coords(self, by):
        if type(by) == type(list()):
            self.map_object_coords.extend(by)
        elif type(by) == type(tuple()):
            self.map_object_coords.append(by)
        else:
            print("Error: Coordinate not added into map_object_coords")

    # Inserts coordinates of map stuff on a grid (T, H, H/T, H/K, K), and then prints map
    def display_map(self, player_coordinate: list):
        self.map_object_elements = ("   ", "H/T", " T ", " K ", "H/K", " H ")
        self.grid_row = []  # row
        self.grid = []  # row * column
        # Fill up map with empty tiles "   " initially
        for i in range(self.GRID_LENGTH):
            i = i  # rubbish line
            self.grid_row.append(self.map_object_elements[0])  # "   "
        for i in range(self.GRID_LENGTH):
            self.grid.append(list(self.grid_row))
        # Fill in rest of tiles
        for row, column in self.towns:
            self.grid[row][column] = self.map_object_elements[2]  # " T "
        self.grid[self.GRID_LENGTH - 1][self.GRID_LENGTH -
                                        1] = self.map_object_elements[3]  # " K "
        if tuple(player_coordinate) in self.towns:
            self.grid[player_coordinate[0]][player_coordinate[1]
                                            ] = self.map_object_elements[1]  # "H/T"
        elif tuple(player_coordinate) == self.RAT_KING:
            self.grid[player_coordinate[0]][player_coordinate[1]
                                            ] = self.map_object_elements[4]  # "H/K"
        else:
            # Replaces old " H " with "  "
            for row in self.grid:
                for index, element in enumerate(row):
                    if element == self.map_object_elements[5]:
                        row[index] = self.map_object_elements[0]
            # New " H " inserted into map
            self.grid[player_coordinate[0]][player_coordinate[1]
                                            ] = self.map_object_elements[5]  # H
        for row in self.grid:
            print("+---" * self.GRID_LENGTH + "+")
            row_string = "|"
            for tile in row:
                row_string += tile + "|"
            print(row_string)
        print("+---" * self.GRID_LENGTH + "+\n")


class Weapon:
    def __init__(self, name, damage, defence):
        self.name = name
        self.damage = damage
        self.defence = defence

# Creatures consists of Players and Enemies


class Creature():

    def __init__(self, name, damage, defence, HP):
        self.name = name
        self._damage = damage
        self._defence = defence
        self.max_HP = HP
        self._HP = HP

    def __str__(self):
        '''Display creature's damage, defence, and health'''
        string = ""
        string += f"Damage: {self._damage[0]}-{self._damage[1]}\n"
        string += f"Defence: {self._defence}\n"
        string += f"HP: {self.HP}"
        return string

    # HP Property
    @ property
    def HP(self):
        return self._HP

    @ HP.setter
    def HP(self, value):
        if self._HP <= self.max_HP:
            self._HP = value
        else:
            self._HP = self.max_HP

    # Damage Property
    @ property
    def damage(self):
        return self._damage

    @ damage.setter
    def damage(self, damage):
        self._damage = damage

    def add_stat_damage(self, by):
        '''Increases creatures minimum and maximum damage'''
        self._damage[0] += by
        self._damage[1] += by

    # Defence Property
    @ property
    def defence(self):
        return self._defence

    @ defence.setter
    def defence(self, value):
        self._defence = value

    def add_stat_defence(self, by):
        '''Increases creature's defence'''
        self._defence += by

    def set_creature_defence(self, defence):
        self._defence = defence

    # >>> Methods for combat
    def heal(self, by=0, full_heal=True):
        '''Fully heals a creature (full_heal=True), else heal creature by (by=0) parameter'''
        if full_heal:
            self.HP = self.max_HP
        else:
            self.HP += by

    def attack_dmg(self):
        '''Returns an integer from the creature's damage range, used in combat'''
        return random.randint(self.damage[0], self.damage[1])

    def deal_damage(self, creature) -> int:
        '''Returns damage to deal to creature'''
        if (isinstance(creature, Creature)):
            damage_to_deal = self.attack_dmg() - creature.defence
            # Ensure damage for self to deal to creature does not go below zero
            if damage_to_deal < 0:
                damage_to_deal = 0
        else:
            print("Error: {creature} is not a member from the Creature class")
        # Deduct creature's HP
        creature.lose_HP(damage_to_deal)
        return damage_to_deal

    def alive_status(self) -> bool:
        '''Returns True if creature is alive (i.e. Their HP is above zero)'''
        if(self.HP > 0):
            return True
        else:
            return False

    def lose_HP(self, by) -> int:
        '''Deducts a creature's HP'''
        self.HP -= by


# Player class for each player who plays the game


class Player(Creature):
    def __init__(self, name="The Hero"):
        super().__init__(name, [2, 4], 1, 20)

        self.coordinate = [0, 0]  # row, column
        self.day = 1

        self.weapons = []  # Store Weapon objects
        self.has_orb = False

        # TODO: Gold, experience, level, shop
        self.gold = 0  # Store currency
        self.experience = 0

    # Overwrites parent class display_stat()
    def __str__(self):
        '''Display player's statistics, indicates if player is holding the orb of power only if the player has already found it'''
        string = "\n"
        string += f"{self.name}\n"
        string += "================\n"
        string += f"  Damage: {self.damage[0]}-{self.damage[1]}\n"
        string += f" Defence: {self.defence}\n"
        string += f" Health: {self.HP}/{self.max_HP}\n"
        if self.has_orb:
            string += "You are holding the orb of power.\n"
        return string

    def sense_orb(self, map_obj: Map):
        '''Detects if the player's coordinates is on the power of orb. Prints stuff'''
        self.day += 1  # Action of sensing orb takes one day
        if tuple(self.coordinate) == map_obj.orb_coordinate:
            if not self.has_orb:
                print("You found the orb of power!")
                orb_of_power = Weapon("Orb of Power", 5, 5)
                self.weapons.append(orb_of_power)
                self.add_stat_damage(orb_of_power.damage)
                print(f"Your attack increases by {orb_of_power.damage}!")
                self.add_stat_defence(orb_of_power.defence)
                print(f"Your defence increases by {orb_of_power.defence}!")
                self.has_orb = True
            else:
                print("You have already picked up the orb of power from this location.")
        else:
            if not self.has_orb:
                print(
                    f"You sense that the Orb of Power is to the {self.sense_orb_direction(map_obj)}.")
            else:
                print(
                    "You sense the orb of power within yourself, filling you with determination.")

    def sense_orb_direction(self, map_obj: Map):
        '''Detects which direction the orb is relative to the player's current coordiante'''
        direction = ""
        if self.coordinate[0] > map_obj.orb_coordinate[0]:
            direction += "north"
        elif self.coordinate[0] < map_obj.orb_coordinate[0]:
            direction += "south"

        if self.coordinate[1] > map_obj.orb_coordinate[1]:
            direction += "west"
        elif self.coordinate[1] < map_obj.orb_coordinate[1]:
            direction += "east"
        return direction

    def rest(self):
        '''Heals the Player's health (HP) to its maximum health (MAX_HP)'''
        self.heal()  # Heals player HP
        self.day += 1  # Resting takes one day
        print("\nYou are fully healed.")

    def move(self, map_obj: Map):
        '''Prompt the player and move the player to a new coordinate on the map'''
        print("Move Character:")
        map_obj.display_map(self.coordinate)
        self.day += 1  # self movement takes one day
        move_successfully = False
        while not move_successfully:
            move_successfully = self.move_coord(map_obj, self.get_wasd_input())
        map_obj.display_map(self.coordinate)
        Ratventure.enter_to_continue()

    def move_coord(self, map_obj: Map, direction, by=1):
        '''Move the player to another coordinate on the map, returns True if player moved successfully'''
        if direction == "w":
            if self.coordinate[0] != 0:
                self.coordinate[0] -= by  # row up [W]
                return True
        elif direction == "a":
            if self.coordinate[1] != 0:
                self.coordinate[1] -= by  # column left [A]
                return True
        elif direction == "s":
            if self.coordinate[0] != map_obj.GRID_LENGTH - 1:
                self.coordinate[0] += by  # row down [S]
                return True
        elif direction == "d":
            if self.coordinate[1] != map_obj.GRID_LENGTH - 1:
                self.coordinate[1] += by  # column right [D]
                return True
        print("You have hit the edge of the map. Choose another direction.")
        return False

    def get_wasd_input(self):
        '''Prompts WASD input from the player with input validation'''
        while True:
            print("W = up; A = left; S = down; D = right")
            user_input = input("Enter WASD: ")
            # Input validation
            if user_input.lower() not in "wasd":
                print("Enter valid letter.")
                continue
            else:
                return user_input


# Enemy class for enemies the player encounters in combat (including the boss)


class Enemy(Creature):
    def __init__(self, name, damage, defence, HP, is_boss=False):
        super().__init__(name, damage, defence, HP)
        self.is_boss = is_boss  # True if the enemy is a boss
        self.original_defence = self.defence

    # Makes the enemy immune
    def immune(self, is_immune: bool = True):
        '''
        Makes the Enemy object immune by increasing its defence temporaritly.
        is_immune = True -> increases the enemy's defence by 1000000
        is_immune = False -> reverts the enemy's defence to original
        '''
        if is_immune:
            # Will cause player's attack to cause zero damage
            self.set_creature_defence(1000000)
        else:
            # Reverts original defence
            self.defence = self.original_defence

    # Returns an enemy object
    @ staticmethod
    def create_enemy(name):
        '''Returns an enemy object'''
        # TODO: Generate more random stats
        if name == "Rat":
            return Enemy("Rat", [1, 3], 1, 10)
        elif name == "Rat King":
            return Enemy("Rat King", [6, 8], 5, 20, is_boss=True)


class Menu:

    @staticmethod
    def menu_text(menu_name, custom_list=[], custom_pre_text=""):
        '''
        Arguments for menu_name:
         "main" -> Main Menu
         "town" -> Town Menu
         "combat" -> Combat Menu
         "outdoor" -> Outdoor Menu

        Argument for custom_list=[]:
        used for lists

        Return Value:
        (text, value)
        text -> the current menu text
        value -> the number of entries in the current menu text
        '''
        main_menu_list = ["New Game", "Resume Game", "Exit Game"]
        town_menu_list = ["View Character", "View Map",
                          "Move", "Rest", "Save Game", "Exit Game"]
        combat_menu_list = ["Attack", "Run"]
        outdoor_menu_list = ["View Character",
                             "View Map", "Move", "Sense Orb", "Exit Game"]

        if menu_name == "main":
            main_menu = "Welcome to Ratventure!\n----------------------\n"
            return Menu.generate_menu_entry(main_menu_list, main_menu)
        elif menu_name == "town":
            return Menu.generate_menu_entry(town_menu_list)
        elif menu_name == "combat":
            return Menu.generate_menu_entry(combat_menu_list)
        elif menu_name == "outdoor":
            return Menu.generate_menu_entry(outdoor_menu_list)
        elif menu_name == "custom":
            return Menu.generate_menu_entry(custom_list, custom_pre_text)

    @staticmethod
    def generate_menu_entry(menu_list, pre_text=""):
        '''Generates and returns a tuple of (menu text, number of menu entries) for particular menu'''
        menu = pre_text
        for num, entry in enumerate(menu_list, 1):
            menu += f"{num}) {entry}\n"
        return menu, len(menu_list)

    @staticmethod
    def choose_choice(text_max_tuple, min_value=1, user_input=""):
        '''Input validation for number choice, ranging from min_value=1 to max'''
        text, max_value = text_max_tuple[0], text_max_tuple[1]
        print(text)
        try:
            while True:
                user_input = int(input("Enter choice: "))
                if min_value <= user_input <= max_value:
                    break
                else:
                    print(
                        f"Error: Only options {min_value} to {max_value} are allowed.")
        except ValueError:
            print("Error: Enter number.")
        return user_input


class Ratventure:

    def __init__(self):
        self.new_game = True  # False if player loads game
        self.save_file_pwd = ""

    def start_game(self):
        in_main_menu = True
        while in_main_menu:
            in_main_menu = self.main_menu()
        Ratventure.enter_to_continue()

        is_detecting_tile = True
        while is_detecting_tile:
            self.detect_tile()

    def main_menu(self):
        Ratventure.clear_output()
        user_input = Menu.choose_choice(Menu.menu_text("main"))
        if user_input == 1:
            # Start game. Create Player and Map object
            self.player = Player()
            self.map = Map()
            return False
        elif user_input == 2:
            if self.load_game():
                return False
            else:
                return True
        elif user_input == 3:
            # Quit Game
            self.quit_game()
        elif user_input == 4:
            # Leaderboard
            pass
        else:
            # Future options
            pass
        return False

    # >>> Detecting tile functions
    def detect_tile(self):
        if tuple(self.player.coordinate) in self.map.towns:
            self.on_map_tile()
        elif tuple(self.player.coordinate) not in self.map.towns and tuple(self.player.coordinate) != self.map.RAT_KING:
            self.on_open_tile()
        elif tuple(self.player.coordinate) == self.map.RAT_KING:
            self.on_rat_king_tile()
        else:
            print("Error: Unknown tile")

    def on_map_tile(self):
        # ==== TOWN (T) ====
        in_town = True
        while in_town == True:
            # Town menu
            print(f"Day {self.player.day}: You are in a town.")
            user_input = ""
            user_input = Menu.choose_choice(Menu.menu_text("town"))
            Ratventure.clear_output()
            if user_input == 1:
                # View character
                print(self.player)
                pass
            elif user_input == 2:
                # View self.map
                self.map.display_map(self.player.coordinate)
            elif user_input == 3:
                # Move
                # Prompt WASD and update coordinates
                self.player.move(self.map)
                break  # Break as self.player coordinate has updated
            elif user_input == 4:
                # Rest
                self.player.rest()  # Heals self.player to their max HP
            elif user_input == 5:
                # Save Game
                self.save_game()
                pass
            elif user_input == 6:
                # Exit Game
                exit()  # Exits game
                pass
            Ratventure.enter_to_continue()

    def on_open_tile(self, enemy_obj_arg=Enemy.create_enemy("Rat")):
        # ==== OPEN TILE ====
        enemy_obj = enemy_obj_arg
        in_outdoor = True
        while in_outdoor:
            # Combat occurs in open tile. Enters combat with the rat enemy
            self.combat(enemy_obj)
            print(f"Day {self.player.day}: You are out in the open.")
            user_input = Menu.choose_choice(Menu.menu_text("outdoor"))
            if user_input == 1:
                # View character
                Ratventure.clear_output()
                print(self.player)
            elif user_input == 2:
                # View self.map
                Ratventure.clear_output()
                self.map.display_map(self.player.coordinate)
            elif user_input == 3:
                # Move
                Ratventure.clear_output()
                self.player.move(self.map)
                break
            elif user_input == 4:
                # Sense orb
                Ratventure.clear_output()
                self.player.sense_orb(self.map)
            elif user_input == 5:
                # Exit game
                exit(0)
            Ratventure.enter_to_continue()

    def on_rat_king_tile(self):
        # ==== RAT KING (K) ====
        # Spawns a rat king enemy when self.player is on K tile
        enemy_obj_king = Enemy.create_enemy("Rat King")
        self.on_open_tile(enemy_obj_arg=enemy_obj_king)
        if not enemy_obj_king.alive_status():
            print("Congratulations! You have defeated the Rat King.")
            # TODO: Leaderboard

    # >>> Game Combat Functions
    def combat(self, enemy_obj: Enemy):
        # Combat
        run_away = False
        # if not run_away:
        #     print(f"Day {self.player.day}: You are out in the open.\n")
        while enemy_obj.alive_status() and not run_away:
            print(f"Day {self.player.day}: You are out in the open.")
            print("Encounter! -", enemy_obj.name)
            print(enemy_obj)
            user_input = Menu.choose_choice(Menu.menu_text("combat"))
            if user_input == 1:
                # 1) Attack
                self.combat_player_attack(enemy_obj)
                if not self.combat_check_win_conditon(enemy_obj):
                    self.combat_enemy_attack(enemy_obj)
                    self.combat_check_lose_condition(enemy_obj)
            else:
                # 2) Run
                run_away = self.combat_player_run(enemy_obj)

    def combat_player_attack(self, enemy_obj):
        # Attack the enemy
        # Check if self.player has orb when facing boss to see if boss is immune
        if enemy_obj.is_boss:
            self.combat_check_orb_obtained(enemy_obj)

        # Calculate attack dmg to deal to enemy
        current_dmg = self.player.deal_damage(enemy_obj)
        print(
            f"You deal {current_dmg} damage to the {enemy_obj.name}.")

    def combat_enemy_attack(self, enemy_obj):
        # Enemy attacks player
        current_enemy_dmg = enemy_obj.deal_damage(self.player)
        print(
            f"Ouch! The {enemy_obj.name} hit you for {current_enemy_dmg} damage!")
        print(f"You have {self.player.HP} HP left.")
        Ratventure.enter_to_continue()

    def combat_check_win_conditon(self, enemy_obj):
        '''Checks if the combat win condition is met'''
        # Combat Win Condition
        if not enemy_obj.alive_status() and self.player.alive_status():
            print(f"The {enemy_obj.name} is dead! You are victorious!")
            Ratventure.enter_to_continue()
            return True
        else:
            return False

    def combat_check_lose_condition(self, enemy_obj):
        '''Checks if the combat lose condition is met'''
        # Combat Lose Conditon
        if not self.player.alive_status():
            print("You lose :(")
            exit(0)

    def combat_player_run(self, enemy_obj):
        print("You run and hide.")
        enemy_obj.heal()  # Enemy heals all HP
        Ratventure.enter_to_continue()
        return True

    def combat_check_orb_obtained(self, enemy_obj):
        print(self.player.has_orb)
        if not self.player.has_orb:
            print(
                f"You do not have the Orb of Power - the {enemy_obj.name} is immune!")
            enemy_obj.immune()
        else:
            enemy_obj.immune(is_immune=False)

    # >>> Saving and loading games
    def create_save_file_pwd(self, file_name="ratventure_save.pkl"):
        '''Learns the pwd of the save file (file_name) used for the game'''
        self.save_file = file_name
        self.dir_path = path.dirname(path.realpath(__file__))
        pwd_save_file = f"{self.dir_path}/{self.save_file}"
        return pwd_save_file

    def save_game(self):
        '''Save game'''
        while True:
            # Show player's current save file
            if self.show_save_files() and not self.new_game:
                print(f"Your current save file is: ({self.save_file})")
            else:
                print("Your current game does not have a save file! Save your game!")
            # Input for new save file name or current save name
            if self.new_game:
                file_name = input("Enter new file name (.pkl): ")
            else:
                file_name = input(
                    f"Enter file name (by default save to {self.save_file}): ")
                if not file_name:
                    file_name = self.save_file
            # Check if file_name ends with .pkl, else add .pkl extension
            if file_name[-4:] != ".pkl":
                file_name += ".pkl"
            # Check if player is overwriting another save file that is not his current loaded save file
            if path.exists(self.create_save_file_pwd(file_name)) and self.save_file_pwd != self.create_save_file_pwd(file_name):
                overwrite = input(
                    f"WARNING: {self.create_save_file_pwd(file_name)} already exists. Overwrite save file {self.save_file_pwd}? (y/n) ")
                if overwrite.lower() == "y":
                    # Confirm overwrite another save file
                    self.save_file_pwd = self.create_save_file_pwd(file_name)
                    break
                else:
                    # Prompt user to enter another file name
                    continue
            else:
                # Set current same save file pwd to that save file entered
                self.save_file_pwd = self.create_save_file_pwd(file_name)
            break
        # Use a pickle object to save player and map objects
        with open(self.save_file_pwd, 'wb') as new_save:
            pickle_list = [self.player, self.map]
            pickle.dump(pickle_list, new_save)

        if self.new_game:
            self.new_game = False  # Saved game means that currently its not a new game anymore
        print(f"Game has been saved as {self.save_file}.")

    # save_file_pwd property
    @ property
    def save_file_pwd(self):
        '''Returns pathway of current save file'''
        return self._save_file_pwd

    @ save_file_pwd.setter
    def save_file_pwd(self, pwd):
        '''Sets pathway directory (pwd) of save file'''
        self._save_file_pwd = pwd

    @ staticmethod
    def find_file_match_in_dir(string, path):
        ''' Finds files with (string) in script directory'''
        result = []
        for root, dirs, files in walk(path):
            for file in files:
                if string in file:
                    result.append(file)
        return result

    def load_game(self) -> bool:
        '''Returns True if the game is loaded successfully'''
        save_file_list = Ratventure.find_file_match_in_dir(
            ".pkl", path.dirname(path.realpath(__file__)))
        if not self.show_save_files():
            print("There are no save files found!")
        else:
            user_input = Menu.choose_choice(("", self.save_file_count))
            for key, value in enumerate(save_file_list, 1):
                if user_input == key:
                    file_name = value
            self.save_file_pwd = self.create_save_file_pwd(file_name)
            try:
                # Use a pickle object to load player and map objects from .pkl file
                with open(self.save_file_pwd, 'rb') as load_save:
                    self.player, self.map = pickle.load(load_save)
                print(f"Save file {file_name} loaded successfully!")

                self.new_game = False  # not a new game, loaded from save
                return True
            except:
                print(f"Error: No save game data ({file_name}) found!")
                return False

    def show_save_files(self):
        '''
        Return True if the save files are shown (i.e. There are save files).
        Sets self.save_file_count which represents number of save files.
        '''
        save_file_list = Ratventure.find_file_match_in_dir(
            ".pkl", path.dirname(path.realpath(__file__)))
        if save_file_list:
            print("Save Files List:")
            for index, save_file in enumerate(save_file_list, 1):
                print(f"{index}) {save_file}")
            self.save_file_count = len(save_file_list)
            return True
        else:
            return False

    # Quit Game
    def quit_game(self):
        exit(0)

    # Other functions
    @staticmethod
    def enter_to_continue(text="Enter to continue..."):
        '''clears teminal'''
        print()
        input(text)
        Ratventure.clear_output()

    @staticmethod
    def clear_output():
        system("clear")


def main():
    ratventure = Ratventure()
    ratventure.start_game()


if __name__ == "__main__":
    main()
