"""
Created on 15 10 2017

@author: zhenya.aka.john@gmail.com
"""
from random import shuffle, randint


class Player:
    """ Player container of animals. """
    player_id = 0

    def __init__(self, name='default name'):
        # self.first_hand = []
        # i.first_hand = take_cards(6)
        self.cards_hand = []
        self.animals = []  # list of animals = amimal()
        self.player_id = Player.player_id + 1
        Player.player_id += 1
        self.name = name

    def __str__(self):
        return f'Player {self.name}\ncard_hand = {self.cards_hand}\nanimals = {self.animals}\n'

    def __repr__(self):
        return f'{self.get_player_name()}'

    def get_player_name(self):
        """
        return player's name
        """
        return self.name

    def get_cards_hand(self):
        """
        return cards_hand list
        """
        return self.cards_hand

    def set_cards_hand(self, cards: list):
        """
        set cards_hand list
        """
        assert type(cards) == list, f'Player.set_cards_hand({cards}: cards not a list)'
        self.cards_hand = cards

    def make_first_hand(self, card_set: list):
        """take 6 random cards from card_set to each Player
        players - instances of Player()
        card set - deck"""
        assert type(card_set) == list, f'Player.make_first_hand({card_set}: card_set not a list)'
        assert len(card_set) >= 6, f'Player.make_first_hand({card_set}: not enough cards to make first 6 card hand)'
        self.cards_hand = functions.take_cards(6, card_set)
        return 1

    def take_handcard(self):
        """Take one card from <Player>'s hand and return it (Player - active_player). or return -1 if failure """
        if self.get_cards_hand():
            while 1:
                # Return number of card from Player's hand.
                try:
                    print("your hand is:", self.get_cards_hand())
                    card_num = int(input("choose card's number")) - 1
                    if 0 <= card_num < len(self.get_cards_hand()):
                        card = self.get_cards_hand().pop(card_num)
                        return card
                    else:
                        print("try again")
                except:
                    print("error, try again")
                    continue
        else:
            print("this Player hasn't any cards!")
            return -1

    def get_player_animals(self):
        """
        reteun player's animals list
        """
        return self.animals

    def set_player_animals(self, animals: list):
        """
        set Player's animals - for testing function
        animals: list - list of Animal instances
        return None
        """
        self.animals = animals

    def make_animal(self):
        """ append animal to player.animals. return 1 ir -1 if error"""
        print(f"Adding new Animal to you, {self.name}")
        self.animals.append(Animal())
        try:
            for number_animal, animal_instance in enumerate(self.animals):
                print(f"Animal {number_animal + 1}:, {animal_instance.property}")
            return 1
        except:
            print("Player.make_animal(): exception error")
            return -1

    def get_hungry_animals(self):
        """
        returns list of hungry animals in players hand
        """
        return [hungry_animal for hungry_animal in self.get_player_animals() if hungry_animal.get_hungry() > 0]

    def get_not_full_fat(self):
        """
        returns list of players animals witch fat_card_number > fat_number
        """
        return [not_full_fat for not_full_fat in self.get_player_animals() if not_full_fat.get_is_full_fat() > 0]

    def get_grazing_count(self):
        """
        returns number: int
        number of players animals with grazing property
        """
        return len([grazing_animal for grazing_animal in self.get_player_animals() if grazing_animal.is_grazing()])

    def get_carnivorous_to_hunt(self):
        """
        return list of carnivorous, that can hunt (are hungry or not enough fat)
        """
        return [animal for animal in self.get_player_animals() if (animal.get_hungry() > 0 or
                                                                   animal.get_is_full_fat() > 0) and
                animal.is_carnivorius()]

    def get_piracy(self):
        """
        return list of animals with piracy property
        """
        return [animal for animal in self.get_player_animals() if animal.is_piracy()]

    def get_to_hibernation(self):
        """
        returns list of animals - that can use hibernation ability on this turn
        (has hibernation property, are not in hibernate state yet, can use hibernation (it is not last turn of eating
        phase or animal use this property in last eating phase)
        """

        return [animal for animal in self.get_player_animals() if animal.can_hibernate()]

    def get_in_hibernation(self):
        """
        returns list of animals in hibernation status - so they can't hunt, piracy, etc
        """
        return [animal for animal in self.get_player_animals() if animal.is_hibernate()]


class Animal:
    def __init__(self):
        animal_id = 0
        self.animal_id = animal_id + 1
        self.property = []
        self.hungry = 1  # change to 1 0 - for test
        self.fat = 0  # zhir
        self.fat_cards_count = 0  # quantity of cards "zhir"
        self.swimming = False
        self.running = False
        self.mimicry = False
        self.mimicry_active = False
        self.scavenger = False
        self.simbiosys = []
        self.piracy = False
        self.can_piracy = False
        self.tail_loss = False
        self.communication = []
        self.grazing = False
        self.high_body_weight = False
        self.hibernation = False
        self.hibernation_active = False
        self.hibernation_ability = False
        self.poisonous = False
        self.poisoned = False
        self.cooperation = []
        self.burrowing = False
        self.camouflage = False
        self.sharp_vision = False
        self.carnivorous = False
        self.parasite = 0  # count of parasites
        self.alive = True
        self.simb_can_be_attacked = True
        self.simb_can_eat = True
        self.can_hunt = True

    def __str__(self):
        return f'{self.get_animal_properties()}, hungry={self.get_hungry()}, free fat={self.get_is_full_fat()}'

    def __repr__(self):
        return f'{self.get_animal_properties()}, hungry={self.get_hungry()}, free fat={self.get_is_full_fat()}'

    def get_animal_properties(self):
        """
        return property: list - list of animal properties
        """
        return self.property

    def get_hungry(self):
        """
        return how hungry is animal
        """
        return self.hungry

    def reduce_hungry(self, number=1):
        """
        reduce hungry on number
        return None
        """
        self.hungry -= number

    def get_fat(self):
        """
        returns: int - self.fat
        """
        return self.fat

    def increase_fat(self, number=1):
        """
        increase fat on number
        return: None
        """
        self.fat += number

    def get_is_full_fat(self):
        return self.fat_cards_count - self.fat

    def is_grazing(self):
        """
        returns True if animal.grazing = True, if not - False
        """
        return self.grazing

    def is_carnivorius(self):
        return self.carnivorous

    def is_piracy(self):
        return self.piracy

    def can_hibernate(self):
        """
        returns True: bool if animal can use hibernate property
        else returns False: bool
        """
        if self.hibernation and self.hibernation_ability and not self.hibernation_active:
            return True
        else:
            return False

    def is_hibernate(self):
        """
        return True if animal is in hibernation
        else return False
        """
        if self.hibernation_active:
            return True
        else:
            return False

    def add_symbiosys(self, animal):
        """
        animal: Animal
        add symbiont to current animal, append it to animal.symbiont list
        return: None
        """
        assert isinstance(animal, Animal), f'Animal.add_symbiosys(): {animal} is not instance of Animal class'
        self.simbiosys.append(animal)

    def get_symbiosys(self):
        """
        returns list of symbiosys
        """
        return self.simbiosys

    def add_communication(self, animal):
        """
        animal: Animal
        add communicate to current animal, append it to animal.communication list
        return: None
        """
        assert isinstance(animal, Animal), f'Animal.add_communication(): {animal} is not instance of Animal class'
        self.communication.append(animal)

    def get_communication(self):
        """
        returns lsit - list of animals (instances of Animal class) communication to current animal
        """
        return self.communication

    def add_cooperation(self, animal):
        """
        animal: Animal
        add cooperate to current animal, append it to animal.symbiont list
        return: None
        """
        assert isinstance(animal, Animal), f'Animal.add_cooperation(): {animal} is not instance of Animal class'
        self.cooperation.append(animal)

    def get_cooperation(self):
        """
        returns list of cooperation of current animal (instances of Animal class)
        """
        return self.cooperation


class functions:

    @staticmethod
    def make_deck(number_of_players: int):
        """ Return set_cards -
        cards - set of cards,
        number_of_players = len(plyers_list)
        """

        cards = [("ostr", "zhir"), ("topo", "zhir"), ("para", "hish"), ("para", "zhir"),
                 ("norn", "zhir"), (["sotr"], "hish"), (["sotr"], "zhir"), ("jado", "hish"),
                 ("komm", "zhir"), ("spac", "hish"), ("mimi",), (["simb"],),
                 ("pada",), ("pira",), ("otbr",), ("bist",), ("vodo",), ("vodo",),
                 (["vzai"], "hish"), ("bols", "zhir"), ("bols", "hish")]
        # Making set_cards from cards and shuffling it,
        # set twice 'set_cards' for 5 - 8 players.
        if number_of_players < 5:
            set_cards = cards * 4
        elif 5 <= number_of_players <= 8:
            set_cards = cards * 8
        else:
            print("looks like this is something wrong with number_players!")
            raise ValueError
        shuffle(set_cards)
        return set_cards

    @staticmethod
    def input_function(alternatives, greeting: str):
        """
        alternatives: list - list of chars - what you expect from input
        greeting: str - text to print in input
        return lowercase user input from alternative
        """
        for char in alternatives:
            assert type(
                char) == str, f'input_function(alternatives, greeting: str): alternatives ({char}) not from strings'
        assert type(greeting) == str, f'input_function(alternatives, greeting: str): greeting ({greeting})is not string'
        assert len(alternatives) >= 1, f'input_function(alternatives, greeting: str): len(alternatives)<1 ' \
                                       f'({len(alternatives)}'
        while True:
            result = input(greeting)
            if result in alternatives:
                return result.lower()
            print('error than input, please, try again')

    @staticmethod
    def set_player_name():
        """
        set player's name
        """
        while True:
            try:
                name = str(input("input Player's name: "))
                break
            except ValueError:
                print("try to input another name")
        return name

    @staticmethod
    def next_player(num: int, players: list):
        """Select next Player.
        num: int - index of current player in players list
        players: list - players list
        return next player num or -1 if failure"""
        assert type(num) == int, f'next_player({num},{players}): type of num ({type(num)}) is not int'
        assert type(players) == list, f'next_player({num},{players}): type of {players} is not list'
        assert 1 < len(players) <= 7, f'next_player({num},{players}): number of players ({len(players)}) ' \
                                      f'are not in range(2,7)'
        assert 0 <= num <= len(players) - 1, f'next_player({num},{players}): num = {num} not in len(players) range'
        try:
            result = (num + 1) % len(players)
            return result
        except:
            return -1

    @staticmethod
    def take_cards(number: int, card_set: list):
        """Take <number> of cards from <card_set> and return it and remove from <card_set>.
        number: int - number of cards to take from card_Set
        card_set: list - list of cards
        return number of cards (list) from card set or -1 if failure
        """
        assert type(number) == int, f'take_cards({number}, {card_set}): type of number ({type(number)} is not int'
        assert type(
            card_set) == list, f'take_cards({number}, {card_set}): type of card_set ({type(card_set)} is not list'
        assert number > 0, f'take_cards({number}, {card_set}): number({number}) <= 0'
        if number <= len(card_set):
            try:
                return [card_set.pop() for i in range(number)]
            except IndexError:
                print(f"take_cards({number}, {card_set}): number > card_set! end of cards!")
                return -1
        else:
            print(f'take_cards({number}, {card_set}): error with number in take_cards function')
            return -1

    @staticmethod
    def make_players_list():
        """Make players list = [instances of Player class] by default min 2 max 8.
        Return players_list: list  """
        result = []
        while True:
            try:
                number_of_players = int(input("input number of players (2...8)"))
                if (number_of_players >= 8) or (number_of_players < 2):
                    print("bad number, try again")
                else:
                    break
            except ValueError:
                print("value error! bad number of players, try again")
            except NameError:
                print("name error! bad number of players, try again")
        for i in range(number_of_players):
            result.append(Player(name=functions.set_player_name()))  # List of instances of Player class.
        return result

    @classmethod
    def make_property(cls, player, players_list):
        """ Defines the property for Player's Animal players_list and active_num -
            for function make_parasite.
        player: Player() - instance of Player class
        players_list: list - list of instances of Player()
        """
        assert isinstance(player,
                          Player), f'make_property(player, card, players_list): player is not instance of Player'
        active_num = players_list.index(player)
        card = player.take_handcard()

        def print_player_animals(player):
            assert isinstance(player, Player), f'print_player_animals(player): player is not instance of Player'
            for number, animal in enumerate(player.get_player_animals()):
                print(number + 1, ' ', animal.get_animal_properties())
            return 1

        # take property value from card
        if len(card) > 1:
            print("your card has more than one property ", card)
            choice = cls.input_function(['1', '2'], 'your card has more than one property - choose 1/2')
            if choice == '1':
                property_value = card[:][0]
            else:
                property_value = card[:][1]
        else:
            property_value = card[:][0]  # If only one property on the card.
        print("your property", property_value)

        lenght_player_animals = len(player.get_player_animals())

        if property_value not in [['vzai'], ['simb'], ['sotr'], "para", "zhir"]:
            # Property is single and not parasite, zhir.
            while 1:  # for single property.
                print_player_animals(player)
                choice = cls.input_function([str(animal_number + 1) for animal_number in
                                             range(lenght_player_animals)],
                                            'choose animals number to add property: ')
                current_animal = player.get_player_animals()[int(choice) - 1]
                if property_value in current_animal.get_animal_properties():
                    # Not doubles.
                    print("This Animal already has this property! choose another Animal!")
                    ret_card = cls.input_function(['y', 'n'], 'do you want to return your card \
                                         to your hand? y/n')
                    if ret_card == 'y':
                        player.get_cards_hand().append(card)
                        return 0
                    else:
                        continue  # Test for single properies loop.
                elif (property_value == "pada") and ("hish" in current_animal.get_animal_properties()):
                    print("Predator can't have scavenger property")
                    ret_card = cls.input_function(['y', 'n'], 'do you want to return your card to your hand? y/n')
                    if ret_card == 'y':
                        player.get_cards_hand().append(card)
                        return 0
                    else:
                        continue  # Test for single properies loop.
                elif (property_value == "hish") and ("pada" in current_animal.get_animal_properties()):
                    print("your Animal is scavenger - it can't be predator!")
                    ret_card = cls.input_function(['y', 'n'], 'do you want to return your card to your hand? y/n')
                    if ret_card == 'y':
                        player.get_cards_hand().append(card)
                        return 0
                    else:
                        continue  # Test for single properies loop.
                else:
                    current_animal.get_animal_properties().append(property_value)

                    if property_value == "vodo":
                        current_animal.swimming = True
                    elif property_value == "bist":
                        current_animal.running = True
                    elif property_value == "mimi":
                        current_animal.mimicry = True
                    elif property_value == "pada":
                        current_animal.scavenger = True
                    elif property_value == "pira":
                        current_animal.piracy = True
                        current_animal.can_piracy = True
                    elif property_value == "otbr":
                        current_animal.tail_loss = True
                    elif property_value == "topo":
                        current_animal.grazing = True
                    elif property_value == "bols":
                        current_animal.hungry += 1  # If big - +1 to eat.
                        current_animal.high_body_weight = True
                    elif property_value == "spac":
                        current_animal.hibernation = True
                        current_animal.hibernation_active = False
                        current_animal.hibernation_ability = True
                    elif property_value == "jado":
                        current_animal.poisonous = True
                    elif property_value == "norn":
                        current_animal.burrowing = True
                    elif property_value == "komm":
                        current_animal.camouflage = True
                    elif property_value == "ostr":
                        current_animal.sharp_vision = True
                    elif property_value == "hish":
                        current_animal.carnivorous = True
                        current_animal.can_hunt = True
                        current_animal.hungry += 1  # If carnivorous - +1 to eat.
                    break  # Test for single properties loop.
            return 1
        elif property_value == "para":
            if functions.make_parasite(players_list, active_num):
                return 1
            else:
                player.get_cards_hand().append(card)
                return 0
        elif property_value == "zhir":
            while 1:  # Zhir loop.
                print_player_animals(player)
                choice = int(input("choose animal's number to add property: ")) - 1

                if choice > lenght_player_animals - 1 or choice < 0:
                    print("error with choice number - please try again!")
                    continue  # Zhir loop.

                current_animal = player.get_player_animals()[choice]
                current_animal.fat_cards_count += 1
                current_animal.get_animal_properties().append("zhir")
                break  # Zhir loop.
            return 1
        else:  # If property is double.
            property_value = property_value.copy()
            if lenght_player_animals < 2:
                print("Error - you can't apply this property because you have only one Animal")
                player.get_cards_hand().append(card)
                return 0
            elif property_value == ["sotr"]:
                for number, animal in enumerate(player.get_player_animals()):
                    print(f'{number + 1}: {animal}')
                while 1:  # Choose sotr pair.
                    try:
                        choice = list(map(int, (input("choose pair of animals (example: 1,3)")).split(',')))
                        if len(choice) != 2:
                            print("you have to input a PAIR of numbers-animals (example: 1,2)")
                            continue  # Choose sotr loop.
                        elif ((0 < choice[0] <= lenght_player_animals) and
                              (0 < choice[1] <= lenght_player_animals) and
                              (choice[0] != choice[1])):
                            animal_1 = player.get_player_animals()[choice[0] - 1]
                            animal_2 = player.get_player_animals()[choice[1] - 1]
                            if animal_1 in animal_2.get_cooperation() or animal_2 in animal_1.get_cooperation():
                                print("This animals had been already cooperators! try another card!")
                                player.get_cards_hand().append(card)
                                return 0
                            else:
                                animal_1.add_cooperation(animal_2)
                                animal_1.get_animal_properties().append(
                                    [f'sotr {player.get_player_animals().index(animal_2)}'])
                                animal_2.add_cooperation(animal_1)
                                animal_2.get_animal_properties().append(
                                    [f'sotr {player.get_player_animals().index(animal_1)}'])
                                print(
                                    f'animal_1: {animal_1.get_cooperation()}\tanimal_2: {animal_2.get_cooperation()}')
                                break  # Choose sotr pair loop.
                    except:
                        print("exception choose pair animals! try again!")
                        continue  # Choose sotr pair loop.
                return 1
            elif property_value == ["simb"]:
                for number, animal in enumerate(player.get_player_animals()):
                    print(f'{number + 1}: {animal}')
                while 1:  # Choose simb pair loop
                    try:
                        choice = list(map(int, (input("choose pair of your animals animal/ "
                                                      "symbiont (1,3):")).split(',')))
                        if len(choice) != 2:
                            print("you have to input a PAIR of numbers-animals (example: 1,2)")
                            continue  # Choose simb pair loop.
                        elif ((0 < choice[0] <= lenght_player_animals) and
                              (0 < choice[1] <= lenght_player_animals) and
                              (choice[0] != choice[1])):
                            animal_1 = player.get_player_animals()[choice[0] - 1]
                            animal_2_symbiont = player.get_player_animals()[choice[1] - 1]
                            if animal_2_symbiont in animal_1.get_symbiosys():
                                print("This animals had been already symbiote! try another card!")
                                player.cards_hand.append(card)
                                return 0
                            elif animal_1 in animal_2_symbiont.get_symbiosys():
                                print("This animals are already in symbiosys. Try another card!")
                                player.cards_hand.append(card)
                                return 0
                            else:
                                animal_1.get_animal_properties().append(
                                    [f'symb {player.get_player_animals().index(animal_2_symbiont)}'])
                                animal_1.add_symbiosys(animal_2_symbiont)
                                print(f'animal_1: {animal_1.get_symbiosys()}')
                                break  # Choose simb pair loop.
                    except:
                        print("exception choosing simbiont/ ne simbiont! try again!")
                        continue  # Choose simb pair loop.
                return 1
            elif property_value == ["vzai"]:
                for number, animal in enumerate(player.get_player_animals()):
                    print(f'{number + 1}: {animal}')
                while 1:  # Choose vzai pair loop.
                    try:
                        choice = list(map(int, (input("choose pair of your animals (1,3):")).split(',')))
                        if len(choice) != 2:
                            print("you have to input a PAIR of numbers-animals (example: 1,2)")
                            continue  # Choose vzai pair loop.
                        elif ((0 < choice[0] <= lenght_player_animals) and
                              (0 < choice[1] <= lenght_player_animals) and
                              (choice[0] != choice[1])):
                            animal_1 = player.get_player_animals()[choice[0] - 1]
                            animal_2 = player.get_player_animals()[choice[1] - 1]
                            if animal_1 in animal_2.get_communication() or animal_2 in animal_1.get_communication():
                                print("This animals had been already vzaimod! try another card!")
                                player.get_cards_hand().append(card)
                                return 0
                            else:
                                animal_1.add_communication(animal_2)
                                animal_1.get_animal_properties().append(
                                    [f'vzai {player.get_player_animals().index(animal_2)}'])
                                animal_2.add_communication(animal_1)
                                animal_2.get_animal_properties().append(
                                    [f'vzai {player.get_player_animals().index(animal_1)}'])
                                print(f'animal_1: {animal_1.get_communication()}\t'
                                      f'animal_2: {animal_2.get_communication()}')
                                break  # Choose vzai pair loop.
                    except:
                        print("exception choosing animals for vzai! try again!")
                        continue  # Choose vzai pair loop.
                return 1

    @staticmethod
    def make_parasite(players_list, active_num):
        """ set parasite property to another player's animal
        players: list - players list"""
        assert type(players_list) == list, f'make_parasite({players_list}: list): players are not list'
        assert len(players_list) > 0, f'make_parasite({players_list}: list): players list is empty'
        for i in range(len(players_list)):
            print(i + 1, " ", players_list[i].get_player_name(), '\n', "animals:\n")
            for number, animal in enumerate(players_list[i].get_player_animals()):
                print(f"Animal {number + 1} {animal.get_animal_properties()}")
        print("this property you can set only to another Player's Animal")
        while 1:  # Main loop.
            try:
                want_next_loop = 0
                player = int(input("input number of Player")) - 1
                if player == active_num:
                    print("you can't set 'parasite' property to your own animals! try again!")
                    continue  # Main loop.
                elif player < 0 or player >= len(players_list):
                    print("wrong number, please try again!")
                    continue  # Main loop.
                else:
                    while 1:  # Choose Animal loop.
                        animal = int(input("input number of Animal")) - 1
                        if 0 <= animal < len(players_list[player].get_player_animals()):
                            if players_list[player].get_player_animals()[animal].parasite == 0:
                                players_list[player].get_player_animals()[animal].get_animal_properties().append("para")
                                players_list[player].get_player_animals()[animal].parasite += 1
                                players_list[player].get_player_animals()[animal].hungry += 2
                                print(players_list[player].get_player_animals()[animal].get_animal_properties())
                                break  # Choose Animal loop.
                            else:
                                print("error - each Animal has only one parasite")
                                ret_card = functions.input_function(['y', 'Y', 'n', 'N'], "do you want to return "
                                                                                          "your card to your hand?"
                                                                                          " y/n")
                                if ret_card == 'y':
                                    return 0
                                elif ret_card == 'n':
                                    want_next_loop = 1
                            break  # Choose Animal loop.
                        print("something wrong with animals number, try again!")
                        continue  # Choose Animal loop.
                    if want_next_loop == 1:
                        # print("want_next_loop")# for test.py
                        continue  # Main loop.
                break  # Main loop.
            except:
                print("exception input number of players or Animal! try again")
                continue  # Main loop.
        return 1

    @staticmethod
    def are_hungry_animals(list_of_animals: list):
        """
        list_of_animals: list of Animal() instances
        return True if there are hungry animals in this list, else return False
        """
        assert type(list_of_animals) == list, f'Functions.are_hungry_animals(): list of animals is not list type'
        for animal in list_of_animals:
            assert isinstance(animal, Animal), f'Functions.are_hungry_animals(): animal is not Animal() instance'
            if animal.get_hungry() > 0:
                return True
        return False


    @staticmethod
    def are_not_full_fat_animals(list_of_animals: list):
        """
        list_of_animals: list of Animal() instances
        return True if there are not full fat animals in this list, else return False
        """
        assert type(list_of_animals) == list, f'Functions.are_not_full_fat_animals(): list of animals is not list type'
        for animal in list_of_animals:
            assert isinstance(animal, Animal), f'Functions.are_not_ful_fat_animals(): animal is not Animal() instance'
            if animal.get_is_full_fat() > 0:
                return True
        return False


class Faza_Razvitija:
    """
    faza razvitija
    players: list - list of instances Player
    number: int - number of first player
    """

    def __init__(self, players: list, number: int):
        self.players = players
        self.number = number
        self.list_of_pass = []
        self.active_player = self.players[self.number]
        self.test = False  # to print test information
        assert type(players) == list, f'faza_razvitija(players, number): type(players) is {type(players)} not list'
        assert type(number) == int, f'faza_razvitija(players, number): type(number) is {type(number)} not int'
        assert number < len(players), f'faza_razvitija(players, number): number {number} > len(players) {len(players)}'
        for item in players:
            assert isinstance(item, Player), f'faza_razvitija(players, number): {item} from players is not instance of ' \
                                             f'Player'

    def test_print(self):
        if self.test:
            print(f'TEST:{self.active_player}')

    def faza_rezvitija_function(self):
        while 1:
            # Main loop.
            if len(self.list_of_pass) == len(self.players):
                print("All players said PASS")
                break  # Exit from main loop.
            elif self.number in self.list_of_pass:  # If active Player said PASS.
                self.number = functions.next_player(self.number, self.players)
                self.active_player = self.players[self.number]
                continue  # Continue main loop with next active Player.
            else:  # If active Player don't say PASS.
                if not self.active_player.get_cards_hand():
                    # If Player hasn't cards in his hand - automatic PASS.
                    self.list_of_pass.append(self.number)
                    self.number = functions.next_player(self.number, self.players)
                    self.active_player = self.players[self.number]
                    continue  # Continue main loop with next active Player.
            print("active Player ", self.active_player.get_player_name(), "=" * 20, "\n")
            print("Player's hand: ", self.active_player.get_cards_hand())
            if self.active_player.get_player_animals():
                for number, i in enumerate(self.active_player.get_player_animals()):
                    print(f'{number} Animal:', i.get_animal_properties())
            else:
                print("you haven't animals yet")
            while 1:  # Loop for unsuitable properties -
                #  to possibility of returning card to deck.
                # animal_id = 0
                if self.active_player.get_player_animals():
                    pass_phrase = functions.input_function(['Y', 'y', 'n', 'N'], "do you want to say Pass (y/n)")
                    if pass_phrase == 'y':
                        self.list_of_pass.append(self.number)
                        break  # Exit from loop 'suitable'.
                    while 1:  # Loop of choose Animal/property.
                        flag_suit = 0
                        choice = functions.input_function(['A', 'a', 'P', 'p', 'pass'], "do you want to make new Animal"
                                                                                        " or new property or say pass? "
                                                                                        "(a/p/pass)")
                        if choice == 'a':
                            self.active_player.take_handcard()
                            self.active_player.make_animal()
                            flag_suit = 1
                            break  # Exit from loop of choose Animal/property.
                        elif choice == 'p':
                            # If you can set property to the Animal:
                            flag_suit = functions.make_property(self.active_player, self.players)
                            break  # Exit from loop of choose Animal/property.
                        elif choice == 'pass':
                            self.list_of_pass.append(self.number)
                            flag_suit = 1
                            break  # Exit from loop of choose Animal/property.
                    if flag_suit == 1:
                        break  # Exit from loop 'suitable'.
                    else:
                        continue  # Loop 'suitable'  return unsuitable card to
                        #  hand in function make_property.

                else:  # If you don't have any animals.
                    print("now you have to make your first Animal from your hand")
                    self.test_print()
                    self.active_player.take_handcard()
                    self.test_print()
                    self.active_player.make_animal()
                    self.test_print()
                    break  # Exit from loop 'suitable'.
            self.number = functions.next_player(self.number, self.players)
            self.active_player = self.players[self.number]
            continue  # Loop 'mainloop'.

        for i in range(len(self.players)):
            print(self.players[i].get_player_name(), '\n', "animals:\n")
            for item in range(len(self.players[i].get_player_animals())):
                print("Animal", item + 1, self.players[i].get_player_animals()[item].get_animal_properties(),
                      "hungry=", self.players[i].get_player_animals()[item].get_hungry())
            print("=" * 20, "\n")
        print("end of faza razvitije")
        return 1


class Define_Eating_Base_Phase:

    def __init__(self, players: list):
        assert type(players) == list
        for player in players:
            assert isinstance(player, Player)
        length_player_list = len(players)
        assert 2 <= length_player_list <= 8, f'Define_Eating_Base_Phase.__init__(): length of players error ' \
                                             f'(2 <= {length_player_list} <= 8)'
        if length_player_list == 2:
            self.red_fish = randint(1, 6) + 2
        elif length_player_list == 3:
            self.red_fish = randint(1, 6) + randint(1, 6)
        elif length_player_list == 4:
            self.red_fish = randint(1, 6) + randint(1, 6) + 2
        elif length_player_list == 5:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + 2
        elif length_player_list == 6:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + 4
        elif length_player_list == 7:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + randint(1, 6) + 2
        elif length_player_list == 8:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + randint(1, 6) + 4

    def get_food_count(self):
        """
        return number of red fish
        """
        return self.red_fish

    def get_text_of_phase(self):
        return f'End of Define eating base phase. Food count (red fish) = {self.red_fish}'

    def __str__(self):
        return f'Food = {self.red_fish}'


class Eating_Phase:

    def __init__(self, players: list, first_number_player: int, eating_base: int):
        """
        players: list - list of Players instances
        first_number_player: int - number of first player (from main)
        eating_base: int - number of red fish from Define_Eating_Base_Phase
        """
        assert type(players) == list, f'Eating_Phase.__init__(): type of players ({type(players)}) not list'
        assert 1 < len(players) <= 8, f'Eating_Phase.__init__(): len of players not 1 < ({len(players)} <= 8)'
        for player in players:
            assert isinstance(player, Player), f'Eating_Phase.__init__(): {player} not instance of Player class'
        assert type(first_number_player) == int, f'Eating_Phase.__init__(): {first_number_player} not integer'
        assert 0 <= first_number_player <= len(players) - 1, f'Eating_Phase.__init__(): not 0 <= {first_number_player}' \
                                                             f'<= len(players_list'
        assert type(eating_base) == int, f'Eating_Phase.__init__(): {eating_base} not integer'
        assert eating_base >= 0, f'Eating_Phase.__init__(): {eating_base} < 0'
        self.players = players
        self.first_player = first_number_player
        self.eating_base = eating_base

    def grazing_function(self, player: Player, user_input=functions.input_function):
        """
        player: Player instance
        change self.eating_base: int
        user_input - added to unit tst - to change user input in test.py
        return None
        """

        number = player.get_grazing_count()
        assert self.eating_base > 0, f'Eating_Phase.grazing_function() - self.eating base <= 0'
        assert number > 0, f'Eating_Phase.grazing_function() - number of animals with grazing property - 0'
        if number < self.eating_base:
            end_number = number
        else:
            end_number = self.eating_base
        destroy_number = user_input([str(number) for number in range(1, end_number + 1)],
                                    f'You are using grazing property to destroy eating base. Input number'
                                    f'to delay from eating base (1-{end_number})')
        if self.eating_base - int(destroy_number) > 0:
            self.eating_base = self.eating_base - int(destroy_number)
        else:
            print(f'Eating_phase.grazing_function(): destroy number > eating base')
            raise AssertionError
        print(f'new eating base = {self.eating_base}')
    # todo player choose what first - communication or cooperation
    @staticmethod
    def communication(animal: Animal, eating_base: int):
        """
        Realize communication function - to realize ring of communication properties
        (communication property works only with red fish taking)
        assume: eating_base > 0
        assume: animal has communications relationships with other animals
        animal: Animal() instance
        eating_base: int - number of red fish in eating base
        return: new eating_base
        """
        assert type(eating_base) == int, f'Eating_Phase.communication(animal, eating base):, ' \
                                         f'eating_base is not integer'
        assert isinstance(animal, Animal), f'Eating_Phase.communication(animal):, animal is not Animal() instance'
        assert animal.get_communication(), f'Eating_Phase.communication(animal):, animal has not communications'
        communicative_relationships = []
        #  initialize for first animal with hungry/ not full fat communicative animals
        for item in animal.get_communication():
            if item.get_hungry() > 0 or item.get_is_full_fat() > 0:
                if item not in communicative_relationships:
                    communicative_relationships.append(item)
        took_red_fish = []
        def recursive_find_communicate(animal: Animal, eating_base: int):
            # base case:
            if eating_base == 0 or not functions.are_not_full_fat_animals(communicative_relationships) or (
               not functions.are_hungry_animals(communicative_relationships)) or(
               len(took_red_fish) == len(communicative_relationships)):
               return eating_base
            else:
                # only one animal has communication property
                if len(communicative_relationships) == 1:
                    choose = 1
                else:
                    # 2. ask player what animal should take  the red fish
                    to_choose_list = [x for x in communicative_relationships if x not in took_red_fish]
                    for number, _ in enumerate(to_choose_list):
                        print(f'{number+1}: = {_}')

                    choose = functions.input_function([str(_ + 1) for _ in range(len(to_choose_list))],
                                                              f'please, select number of animal from communication list to '
                                                              f'take red fish from eating base: ')
                animal_to_take = communicative_relationships[int(choose)-1]
                if animal_to_take.get_communication():
                    for item in animal_to_take.get_communication():
                        if item.get_hungry() > 0 or item.get_is_full_fat() > 0:
                            if item not in communicative_relationships:
                                communicative_relationships.append(item)
                eating_base -= 1
                if animal_to_take.get_hungry() > 0:
                    animal_to_take.reduce_hungry()
                    print(f'animal {animal_to_take} reduce hungry to {animal_to_take.get_hungry()}')
                elif animal_to_take.get_is_full_fat() > 0:
                    animal_to_take.increase_fat()
                    print(f'animal {animal_to_take} reduce fat to {animal_to_take.get_fat()}')
                else:
                    raise ValueError
                took_red_fish.append(animal_to_take)
                return recursive_find_communicate(animal_to_take, eating_base)

        return eating_base

    @staticmethod
    def cooperation(animal: Animal):
        """
        Realize cooperation function - to realize ring of cooperation properties
        (cooperation property works only with blue fish taking)
        assume: animal has cooperation relationships with other animals
        animal: Animal() instance
        eating_base: int - number of red fish in eating base
        return: None
        """
        assert isinstance(animal, Animal), f'Eating_Phase.cooperation(animal):, animal is not Animal() instance'
        assert animal.get_cooperation(), f'Eating_Phase.cooperation(animal):, animal has not cooperations'
        cooperative_relationships = []
        #  initialize for first animal with hungry/ not full fat cooperative animals
        for item in animal.get_cooperation():
            if item.get_hungry() > 0 or item.get_is_full_fat() > 0:
                if item not in cooperative_relationships:
                    cooperative_relationships.append(item)
        took_blue_fish = []

        def recursive_find_cooperate(animal: Animal):
            # base case:
            if not functions.are_not_full_fat_animals(cooperative_relationships) or (
               not functions.are_hungry_animals(cooperative_relationships)) or(
               len(cooperative_relationships) == len(took_blue_fish)):
                    return None
            else:
                # only one animal has cooperation property
                if len(cooperative_relationships) == 1:
                    choose = 1
                else:
                    # 2. ask player what animal should take  the blue fish
                    to_choose_list = [x for x in cooperative_relationships if x not in took_blue_fish]
                    for number, _ in enumerate(to_choose_list):
                        print(f'{number + 1}: = {_}')

                    choose = functions.input_function([str(_ + 1) for _ in range(len(to_choose_list))],
                                                      f'please, select number of animal from cooperation list to '
                                                      f'take blue fish: ')
                animal_to_take = cooperative_relationships[int(choose) - 1]
                if animal_to_take.get_cooperation():
                    for item in animal_to_take.get_cooperation():
                        if item.get_hungry() > 0 or item.get_is_full_fat() > 0:
                            if item not in cooperative_relationships:
                                cooperative_relationships.append(item)
                if animal_to_take.get_hungry() > 0:
                    animal_to_take.reduce_hungry()
                    print(f'animal {animal_to_take} reduce hungry to {animal_to_take.get_hungry()}')
                elif animal_to_take.get_is_full_fat() > 0:
                    animal_to_take.increase_fat()
                    print(f'animal {animal_to_take} reduce fat to {animal_to_take.get_fat()}')
                else:
                    raise ValueError
                took_blue_fish.append(animal_to_take)
                return recursive_find_cooperate(animal_to_take)

        return None


    def take_red_fish(self, player: Player, user_input=functions.input_function):
        """
        player: Player - active player
        eating base : int
        take red fish from eating base (if it exist), reduce hungry
        make pair properties
        assume that there are hungry or not full fat animals in player hand
        assume that eating base is not emtpy
        return None
        """
        # todo wrong with communicaton and cooperation - they may be in  a ring - see FAQ
        assert isinstance(player, Player), f'Eating_phase.take_red_fish(): {player} is no Player instance'
        assert type(self.eating_base) == int, f'Eating_phase.take_red_fish(): {self.eating_base} is not integer'
        assert self.eating_base > 0, f'Eating_phase.take_red_fish(): {self.eating_base} <= 0'
        animals = player.get_player_animals()
        while True:  # choose loop
            animal_num = user_input([str(x) for x in range(1, len(animals) + 1)],
                                    f'Please, select animal to take red fish from eating base: ')
            animal = animals[int(animal_num) - 1]
            if animal.get_hungry() == 0 and animal.get_is_full_fat() == 0:
                print('this animal is not hungry and is enough fat! Choose another animal!')
                continue  # choose loop
            # if animal has symbiont
            if animal.get_symbiosys():
                hungry_symbiont = False
                for symbiont in animal.get_symbiosys():
                    if symbiont.get_hungry() > 0:
                        print(f'one of its symbionts is hungry: {symbiont} - this animal cant eat')
                        hungry_symbiont = True
                        break  # for symbiont loop
                if hungry_symbiont:
                    continue  # choose loop

            # if animal is hungry
            if animal.get_hungry() > 0:
                animal.reduce_hungry()
                self.eating_base -= 1
                break  # choose loop
            # if animal has free fat
            elif animal.get_is_full_fat() > 0:
                self.eating_base -= 1
                animal.increase_fat()
                break  # choose loop
        # if animal communication
        if animal.get_communication() and self.eating_base > 0:
            self.eating_base = Eating_Phase.communication(animal, self.eating_base)
        # if animal cooperation
        if animal.get_cooperation():
            Eating_Phase.cooperation(animal)

    def single_turn(self, player):
        """
        realize single turn for player - Player() of eating phaze
        """
        assert isinstance(player, Player)
        print(f'{"-" * 10}active player - {player.get_player_name()} {"-" * 10}')
        active_player_hungry_animals = player.get_hungry_animals()
        active_player_not_full_fat = player.get_not_full_fat()
        active_player_grazing_number = player.get_grazing_count()
        active_player_piracy_animals = 


    def single_round_eating(self, players, active_player):
        """
        realize single round of eating phaze
        players: list - list of Players()
        active_player - Player() instance of first player
        """
        assert type(players) == list, f'Eating_Phase.single_round_eating(): players are not list'
        for player in players:
            assert isinstance(player, Player), f'Eating_Phase.single_round_eating(): {player} is not Player() instance'
        assert isinstance(active_player, Player), f'Eating_Phase.single_round_eating(): ' \
                                                  f'{active_player} is not Player() instance'
        assert active_player in players, f'Eating_Phase.single_round_eating(): {active_player} is not players list'
        list_of_round_pass = []
        list_of_hungry_to_piracy = []  # list of animals, who take food in this turn but still are hungry

    def eating_phase(self, user_input=functions.input_function):
        """
        return None
        """
        active_player = self.players[self.first_player]
        list_of_pass = []  # list of players who say pass
        l
        # todo try to realize single round (whitout while main loop)
        while True:  # main loop
            # print(f'TEST list of pass = {list_of_pass}')
            if len(list_of_pass) == len(self.players):
                # todo make text end of this phase
                print('TEST - end of phaza eating')
                break  # main loop
            if active_player in list_of_pass:
                continue  # main loop
            print(f'{"-" * 10}active player - {active_player.get_player_name()} {"-" * 10}')
            active_player_hungry_animals = active_player.get_hungry_animals()
            active_player_not_full_fat = active_player.get_not_full_fat()
            active_player_grazing_number = active_player.get_grazing_count()
            active_player_in_hibernation = active_player.get_in_hibernation()
            # if all of his animals are not hungry or fat (if yes - grazing function and active_player = next_player)
            if len(active_player_hungry_animals) == 0 and len(active_player_not_full_fat) == 0:
                if active_player_grazing_number > 0 and self.eating_base > 0:
                    answer = user_input(['y', 'Y', 'n', 'N'], f'All of your animals are not hungry and '
                                                              f'full of fat. Do you want to use grazing '
                                                              f'property of your animals to destroy eating'
                                                              f' base {self.eating_base}? y/n ')
                    if answer == 'y':
                        self.grazing_function(active_player, user_input)
                        active_player = self.players[functions.next_player(self.players.index(active_player),
                                                                           self.players)]
                        continue  # main loop
                    else:
                        active_player = self.players[functions.next_player(self.players.index(active_player),
                                                                           self.players)]
                        continue  # main loop
                else:  # if not grazing animals on players hand or eating base = 0 - next player, automatic pass
                    list_of_pass.append(active_player)
                    active_player = self.players[functions.next_player(self.players.index(active_player), self.players)]
                    continue  # main loop
            else:
                # not all animals are not hungry or enough fat
                # 1. take red fish
                # 2. hunting
                # 3. piracy
                # 4. hibernation
                # 5. say pass
                print(f'This animals are hungry or have free fat slots:')
                active_player_can_eat = set(active_player_hungry_animals + active_player_not_full_fat)
                for animal in active_player_can_eat:
                    print(f'{active_player.get_player_animals().index(animal) + 1} {animal}')
                # if player want to take red fish from eating base or say pass or play property
                choose_list = ['take', 'pass']
                if active_player.get_carnivorous_to_hunt():
                    choose_list.append('hunt')
                if list_of_hungry_to_piracy and active_player.get_piracy():
                    choose_list.append('piracy')
                if active_player.get_to_hibernation():
                    choose_list.append('hibernation')

                answer = user_input(choose_list, f'Now you have to take red fish from eating base '
                                                 f'({self.eating_base} or do else functions, depending of'
                                                 f" your animals property: {', '.join(choose_list)}")
                if answer == 'take':
                    self.take_red_fish(active_player)
                    if active_player_grazing_number > 0 and self.eating_base > 0:
                        answer = user_input(['y', 'Y', 'n', 'N'],
                                            'Do you want to use grazing property of your animals to '
                                            f'destroy eating base {self.eating_base}? y/n ')
                        if answer == 'y':
                            self.grazing_function(active_player)
                    active_player = self.players[functions.next_player(self.players.index(active_player), self.players)]
                    continue  # main loop
                if answer == 'pass':
                    list_of_pass.append(active_player)
                    active_player = self.players[functions.next_player(self.players.index(active_player), self.players)]
                    continue  # main loop

                # todo adding simb to property list vzai - id symb id + 1

        # if all
        # animals of all players - or end of red fish and and hunting, piracy, hibernation or all said pass
        # end of this phase

        # 1. grazing (+) take red fish
        # hunting without taking red fish
        # check if scavenger is present
        # piracy without taking red fish
        # hibernation - without taking red fish
        # choose animal to take red fish
        # hunting
        # grazing function
        # twice properties -


#  it global variable + I change name of thi function + I think that it is poor design to pass argument with the same
#  name... OMG - really shitcode...


def carnivorous_eating_process(carnivore):
    """" here carnivore eating process"""
    # TODO write tthis function
    pass


def phase_eating(players, first_player_number, red_fish_count):
    """ realize eating phase players - players with animals"""
    player_number = first_player_number
    if players and isinstance(players, list):
        if not players[player_number].animals:
            print(f"error - this player ({players[player_number].name}) has not any animals")
            return -1
        else:
            stop_this_round_list = []  # for exit from below while 1 - if len of this list == len players_list
            while 1:  # main loop
                if len(stop_this_round_list) == len(players):
                    break
                # make list of hungry animals of active player
                hungry_animal = [hungry_animal for hungry_animal in players[player_number].animals if
                                 hungry_animal.hungry > 0]
                # make list of fat and hungry animal
                not_enough_fat_animal = [animal for animal in players[player_number] if
                                         animal.fat_cards_count - animal.fat > 0]
                # make list of carnivorous
                carnivorous = [animal for animal in players[player_number] if animal.carnivorous]
                if hungry_animal or not_enough_fat_animal:
                    print(f"active player - {players[player_number].name}")
                    print("you have hungry animals")
                    print(f"your hungry animals:")
                    hungry_not_en_fat_set = list(set(hungry_animal + not_enough_fat_animal))
                    for number, animal in enumerate(hungry_not_en_fat_set):
                        print(f"{number + 1} animal, property: {animal.property}, hungry = {animal.hungry} "
                              f"fat = {animal.fat} fat cards = {animal.fat_cards_count})")
                    print(f"food base = {red_fish_count}")
                    # if so bad - neither carnivorous nor grazing - actually nothing to do on this turn

                    if not carnivorous and players[player_number].grazing_count == 0 and red_fish_count == 0:
                        # if there are hungry or not enough fat and red fih doesn't exist
                        print(f"ou, you have hungry animals, but they can't eat...")
                        stop_this_round_list.append(players[player_number])
                        player_number = next_player
                        continue
                    # do you want to use grazing property
                    elif players[player_number].grazing_count > 0:
                        print(f"you have grazing property and can destroy {players[player_number].grazing_count} red "
                              f"fishes from red fish base ({red_fish_count})")
                        while 1:
                            choose = input(f"you have animals with grazing property - do you want to use this\n"
                                           f"property to destroy red fish in food base={red_fish_count} y/n?")
                            if choose == 'y' or 'Y':
                                grazing_process()
                                break
                            elif choose == 'n' or 'N':
                                break
                            else:
                                print("please, type only n or y - try again")
                                continue

                    # choose hungry animal or say pass
                    print("now you can choose your hungry animal or say PASS")
                    while 1:
                        choose = input(f"please choose what animal do you want to give food? or type 'p' - say pass")
                        if choose == 'p' or 'P':
                            player_number = next_player(player_number)
                            break
                        else:
                            animal_id = int(choose) - 1
                            # TODO STAY HERE
                            if isinstance(animal_id, int) and 0 <= animal_id < len(hungry_not_en_fat_set):
                                current_animal = hungry_not_en_fat_set[animal_id]
                                break
                            else:
                                print("something wrong with animal number - try again")
                                continue
                    # to say PASS
                    if choose == 'p' or 'P':
                        continue  # main loop
                    # if current animal is carnivores and there are red fish
                    if current_animal.carnivores and red_fish_count > 0:
                        print(f"your animal is carnivores. Do you want to use this property and try to kill or you want"
                              f"to take red fish from red fish base = {red_fish_count}? C/R?")
                        while 1:
                            choose = input()
                            if choose == 'C' or 'c':
                                carnivorous_eating_process(current_animal)
                                break
                            elif choose == "r" or "R":
                                eating_from_red_fih_base()
                            else:
                                print("something wrong with your input. please try r or c")
                                continue



                else:
                    # all animals of this active player are not hungry and are enough fat
                    # TODO make here posobility of topotun proprety
                    stop_this_round_list.append(players_list(player_number))
                    player_number = next_player(player_number)
            print(f"end of eating phase")



    else:
        print(f"error! trouble with players_list in faza pit function")
        return -1


if __name__ == "__main__":

    players_list = functions.make_players_list()
    # players_list - list of instances of class "Player"
    deck = functions.make_deck(len(players_list))
    for player in players_list:
        assert isinstance(player, Player), f'main: player {player} is not instance of Player class'
        assert len(deck) >= 6 * len(
            players_list), f'main: len(deck) < len(players)*6. Not enough cards to make first hand'
        player.make_first_hand(deck)
    first_number_player = randint(0, len(players_list) - 1)
    razvitie = Faza_Razvitija(players_list, first_number_player)
    razvitie.faza_rezvitija_function()
    define_eating_base_phase = Define_Eating_Base_Phase(players_list)
    food = define_eating_base_phase.get_food_count()
    print(define_eating_base_phase.get_text_of_phase())
    eating = Eating_Phase(players_list, first_number_player, food)
    eating.eating_phase()
