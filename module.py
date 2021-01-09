"""
Created on 15 10 2017

@author: zhenya.aka.john@gmail.com
"""
from random import shuffle, randint


class Player:
    """ Player container of animals. """
    player_id = 0

    def __init__(self, name='default name'):
        self.cards_hand = []
        self.animals = []  # list of animals = amimal()
        self.player_id = Player.player_id + 1
        Player.player_id += 1
        self.name = name

    def __str__(self):
        return f'Player {self.name}\ncard_hand = {self.cards_hand}\nanimals = {self.animals}\n'

    def __repr__(self):
        return f'{self.get_player_name()}'

    def get_player_id(self):
        """
        return: int player_id
        """
        return self.player_id

    @staticmethod
    def set_player_name():
        """
        set player's name player.name
        return: str(name)
        """
        while True:
            try:
                name = str(input("input Player's name: "))
                break
            except ValueError:
                print("try to input another name")
        return name

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

    def make_animal(self):
        """ append animal to player.animals. return 1 ir -1 if error"""
        print(f"Adding new Animal to you, {self.name}")
        self.animals.append(Animal(self.player_id))
        try:
            for number_animal, animal_instance in enumerate(self.animals):
                print(f"Animal {number_animal + 1}:, {animal_instance.get_animal_properties()}")
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

    def get_can_eat_animals(self):
        """
        return list of animals from player hand which can eat
        """
        return [animal for animal in self.get_player_animals() if animal.can_eat()]


class Animal:
    animal_id = 0

    def __init__(self, player_id=-1):
        self.belong_to_player = player_id
        self.animal_id = Animal.animal_id
        Animal.animal_id += 1
        self.red_fish_count = 0
        self.blue_fish_count = 0
        self.single_properties = []
        self.symbiosys = []
        self.communication = []
        self.cooperation = []
        self.fat = 0
        self.fat_cards_count = 0  # quantity of cards "fat"
        self.hibernation_active = False
        self.hibernation_possibility = False
        self.poisoned = False
        self.parasite = 0  # count of parasites
        self.alive = True

    def __str__(self):
        return f'id={self.animal_id}, {self.get_animal_properties()}, ' \
               f'free fat={self.get_is_full_fat()}'

    def __repr__(self):
        return f'id={self.animal_id}, {self.get_animal_properties()}, ' \
               f'free fat={self.get_is_full_fat()}'

    def get_animal_id(self):
        """
        return int: animal id
        """
        return self.animal_id

    def increase_red_fish(self, number=1):
        """
        increase red fish count on number - 1 by default
        """
        self.red_fish_count += number

    def increase_blue_fish(self, number=1):
        """
        increase blue fish count on number - 1 by default
        """
        self.blue_fish_count += number

    def add_single_animal_property(self, property: str):
        """
        Adds single property from deck to current animal
        property: str - string of property
        assume property is property from deck
        return None
        """
        assert property in ['high_body_weight', 'swimming', 'sharp_vision', 'burrowing', 'carnivorous',
                            'hibernation_ability', 'tail_loss', 'mimicry',  'running', 'poisonous', 'grazing',
                            'scavenger', 'camouflage', 'piracy'], f'Animal.add_single_animal_property(): ' \
                                                                  f'property is not from deck single properties'

        self.single_properties.append(property)

    def get_single_animal_properties(self):
        """
        return property: list - list of animal properties
        """
        return self.single_properties.copy()

    def get_animal_properties(self):
        """
        combine animal properties to print state
        """
        single_properties = self.get_single_animal_properties()
        list_of_symbiosys = self.get_symbiosys()
        list_of_communications = self.get_communication()
        list_of_cooperations = self.get_cooperation()
        fat_count = self.get_fat()
        hibernation_state = self.is_hibernate()
        poisoned = self.poisoned
        hungry = self.get_hungry()
        properties = []
        properties.extend(single_properties)
        properties.append('\ncommunications:')
        properties.extend(list_of_communications)
        properties.append('\ncooperations:')
        properties.extend(list_of_cooperations)
        properties.append('\nsymbiosys')
        properties.extend(list_of_symbiosys)
        properties.append(f'\nfat={fat_count}, hibernation state={hibernation_state}, poisoned={poisoned},'
                          f' hungry={hungry}')

        return properties

    def get_hungry(self):
        """
        return how hungry is animal
        """
        # return self.hungry
        hungry = 1
        if self.is_high_body_weight():
            hungry += 1
        if self.is_carnivorous():
            hungry += 1
        if self.parasite:
            hungry += 2 * self.parasite

        return hungry - self.red_fish_count - self.blue_fish_count

    def get_fat(self):
        """
        returns: int - self.fat
        """
        return self.fat

    def increase_fat(self, number=1):
        """
        increase fat on number
        number: int
        assume fat <= fat cars count
        return: None
        """
        assert type(number) == int, f'Animal.increase_fat(): number is not integer'
        assert number <= self.get_is_full_fat(), f'Animal.increase_fat(): number > free fat_cards'
        self.fat += number

    def reduce_fat(self, number=1):
        """
        decreases fat on number
        assume number: int
        assume number < fat
        return: None
        """
        assert type(number) == int, f'Animal.reduce_fat(): number is not integer'
        assert number <= self.get_fat(), f'Animal.reduce_fat(): number > fat'
        self.fat -= number

    def get_is_full_fat(self):
        """
        return int - number of yellow (fat) fish animal can take
        """
        not_full_fat = self.fat_cards_count - self.fat
        assert not_full_fat >= 0, f'Animal.get_is_full_fat(): fat > fat_cards'
        return not_full_fat

    def is_tail_loss(self):
        """
        return True if animal has tail loss property else return False
        """
        if 'tail_loss' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_swimming(self):
        """
        return True if animal has swimming property else return False
        """
        if 'swimming' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_running(self):
        """
        return True if animal is running, else return False
        """
        if 'running' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_mimicry(self):
        """
        return True if animal is mimicry, else return False
        """
        if 'mimicry' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_scavenger(self):
        """
        return True if animal is scavenger, else return False
        """
        if 'scavenger' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_grazing(self):
        """
        returns True if animal has grazing property, if not - False
        """
        if 'grazing' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_carnivorous(self):
        """
        returns True if animal has carnivorous property, if not - False
        """
        if 'carnivorous' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_piracy(self):
        """
        return: Bool - if animal has piracy property
        """
        if 'piracy' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_high_body_weight(self):
        """
        return: Bool - if animal has high body weight property
        """
        if 'high_body_weight' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_hibernation_ability(self):
        """
        return: Bool - if animal has hibernation ability property
        """
        if 'hibernation_ability' in self.get_single_animal_properties():
            return True
        else:
            return False

    def can_hibernate(self):
        """
        returns True: bool if animal can use hibernate property
        else returns False: bool
        """
        if self.is_hibernation_ability() and self.hibernation_possibility and not self.hibernation_active:
            return True
        else:
            return False

    def is_hibernate(self):
        """
        return True if animal is in hibernation state
        else return False
        """
        if self.hibernation_active:
            return True
        else:
            return False

    def to_hibernate(self):
        """
        Put animal to hibernate state
        return: None
        """
        self.hibernation_active = True

    def hibernation_possibility_False(self):
        """
        change hibernation ability state - False
        return: None
        """
        self.hibernation_possibility = False

    def hibernation_possibility_True(self):
        """
        change hibernation ability state - True
        return: None
        """
        self.hibernation_possibility = True

    def is_poisonous(self):
        """
        return: Bool - if animal has poisonous  property
        """
        if 'poisonous' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_burrowing(self):
        """
        return: Bool - if animal has burrowing  property
        """
        if 'burrowing' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_camouflage(self):
        """
        return: Bool - if animal has camouflage  property
        """
        if 'camouflage' in self.get_single_animal_properties():
            return True
        else:
            return False

    def is_sharp_vision(self):
        """
        return: Bool - if animal has sharp_vision  property
        """
        if 'sharp_vision' in self.get_single_animal_properties():
            return True
        else:
            return False

    def add_symbiosys(self, animal):
        """
        animal: Animal() instance
        add symbiont to current animal, append it to animal.symbiont list
        return: None
        """
        assert isinstance(animal, Animal), f'Animal.add_symbiosys(): {animal} is not instance of Animal class'
        assert animal not in self.get_symbiosys(), f'Animal.add_symbiosys(): {animal} is not already symbiont'
        self.symbiosys.append(animal)

    def get_symbiosys(self):
        """
        returns list of symbiosys
        """
        return self.symbiosys.copy()

    def exist_hungry_symbiosys(self):
        """
        return True if there are hungry symbionts (then animal can't eat), else return False
        """

        symbiosys_list = self.get_symbiosys()
        for symbiont in symbiosys_list:
            if symbiont.get_hungry() > 0:
                return True
        return False

    def add_communication(self, animal):
        """
        animal: Animal() instance
        add communicate to current animal, append it to animal.communication list
        warning - it is dual property, but here we adds this property only to one animal!
        return: None
        """
        assert isinstance(animal, Animal), f'Animal.add_communication(): {animal} is not instance of Animal class'
        assert animal not in self.get_communication(), f'Animal.add_communication(): {animal} is already in ' \
                                                       f'communication list'
        self.communication.append(animal)

    def get_communication(self):
        """
        returns lsit - list of animals (instances of Animal class) communication to current animal
        """
        return self.communication.copy()

    def add_cooperation(self, animal):
        """
        animal: Animal() instance
        add cooperate to current animal, append it to animal.symbiont list
        return: None
        """
        assert isinstance(animal, Animal), f'Animal.add_cooperation(): {animal} is not instance of Animal class'
        assert animal not in self.get_cooperation(), f'Animal.add_cooperation(): {animal} is already in cooperation ' \
                                                     f'list'
        self.cooperation.append(animal)

    def get_cooperation(self):
        """
        returns list of cooperation of current animal (instances of Animal class)
        """
        return self.cooperation.copy()

    def can_eat(self):
        """
        Returns True if animal is hungry, or is free fat slots, and it's symbionts are not hungry,
                     and it is not in hibernation status
        else:: returns False
        """
        if (self.get_hungry() > 0 or self.get_is_full_fat() > 0) \
                and not self.is_hibernate() \
                and not self.exist_hungry_symbiosys():
            return True
        return False

    def can_hunt(self):
        """
        return True if animal can hunt (is carnivorous, can eat)
        else return False
        """
        if self.is_carnivorous() and self.can_eat():
            return True
        return False

    def can_attack(self, animal, print_msg=True):
        """
        return True if <self> (animal - carnivorous) can attack in hunting process <animal>
        else return False
        print_msg - flag to not print message why currant animal can not attackcurrent victim
        (in functions.exist_animals_to_hunt() don't want to print this msg)
        assume self animal can hunt
        """

        assert self.can_hunt(), f"Animal.can_attack(): self animal can't hunt"
        assert isinstance(animal, Animal), f"Animal.can_attack(self, animal): animal is not Animal() instance"

        if animal == self:
            if print_msg:
                print(f'You can not attack yourself')
            return False

        if animal.is_swimming() and not self.is_swimming():
            if print_msg:
                print('Your carnivorous is not swimming')
            return False

        elif animal.get_symbiosys():
            if print_msg:
                print('Your carnivorous can not attack animal, which symbiont is alive')
            return False

        elif animal.is_high_body_weight() and not self.is_high_body_weight():
            if print_msg:
                print('Your carnivorous can not attack animal with high body weight')
            return False

        elif animal.is_burrowing() and animal.get_hungry() == 0:
            if print_msg:
                print('Your carnivorous can not attack burrowing animal')
            return False

        elif animal.is_camouflage() and not self.is_sharp_vision():
            if print_msg:
                print('Your carnivorous can not attack animal with camouflage')
            return False

        return True


class functions:

    @staticmethod
    def make_deck(number_of_players: int):
        """ Return set_cards -
        cards - set of cards,
        number_of_players = len(plyers_list)
        parasite
        """

        cards = [("sharp_vision", "fat"), ("grazing", "fat"), ("parasite", "carnivorous"), ("parasite", "fat"),
                 ("burrowing", "fat"), ("cooperation", "carnivorous"), ("cooperation", "fat"),
                 ("poisonous", "carnivorous"),
                 ("camouflage", "fat"), ("hibernation_ability", "carnivorous"), ("mimicry",), ("symbiosys",),
                 ("scavenger",), ("piracy",), ("tail_loss",), ("running",), ("swimming",), ("swimming",),
                 ("communication", "carnivorous"), ("high_body_weight", "fat"), ("high_body_weight", "carnivorous")]
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
    def next_player(num: int, players: list):
        """Select next Player.
        num: int - index of current player in players list
        players: list - players list
        return: int - next player num or -1 if failure"""
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
        return: list -  number of cards (list) from card set or -1 if failure
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
            result.append(Player(name=Player.set_player_name()))  # List of instances of Player class.
        return result

    # todo rewrite classmethod make property and make parasite to static methos of Animal class
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

        if property_value not in ['communication', 'symbiosys', 'cooperation', "parasite", "fat"]:
            # Property is single and not parasite, fat.
            while 1:  # for single property.
                print_player_animals(player)
                choice = cls.input_function([str(animal_number + 1) for animal_number in
                                             range(lenght_player_animals)],
                                            'choose animals number to add property: ')
                current_animal = player.get_player_animals()[int(choice) - 1]
                if property_value in current_animal.get_single_animal_properties():
                    # Not doubles.
                    print("This Animal already has this property! choose another Animal!")
                    ret_card = cls.input_function(['y', 'n'], 'do you want to return your card \
                                         to your hand? y/n')
                    if ret_card == 'y':
                        player.get_cards_hand().append(card)
                        return 0
                    else:
                        continue  # Test for single properies loop.
                elif (property_value == "scavenger") and (current_animal.is_carnivorous()):
                    print("Predator can't have scavenger property")
                    ret_card = cls.input_function(['y', 'n'], 'do you want to return your card to your hand? y/n')
                    if ret_card == 'y':
                        player.get_cards_hand().append(card)
                        return 0
                    else:
                        continue  # Test for single properies loop.
                elif (property_value == "carnivorous") and (current_animal.is_scavenger()):
                    print("your Animal is scavenger - it can't be predator!")
                    ret_card = cls.input_function(['y', 'n'], 'do you want to return your card to your hand? y/n')
                    if ret_card == 'y':
                        player.get_cards_hand().append(card)
                        return 0
                    else:
                        continue  # Test for single properties loop.
                else:
                    current_animal.add_single_animal_property(property_value)

                    break  # Test for single properties loop.
            return 1
        elif property_value == "parasite":
            if functions.make_parasite(players_list, active_num):
                return 1
            else:
                player.get_cards_hand().append(card)
                return 0
        elif property_value == "fat":
            while 1:  # fat loop.
                print_player_animals(player)
                choice = int(input("choose animal's number to add property: ")) - 1

                if choice > lenght_player_animals - 1 or choice < 0:
                    print("error with choice number - please try again!")
                    continue  # fat loop.

                current_animal = player.get_player_animals()[choice]
                current_animal.fat_cards_count += 1
                break  # fat loop.
            return 1
        else:  # If property is double.
            property_value = property_value.copy()
            if lenght_player_animals < 2:
                print("Error - you can't apply this property because you have only one Animal")
                player.get_cards_hand().append(card)
                return 0
            elif property_value == "cooperation":
                for number, animal in enumerate(player.get_player_animals()):
                    print(f'{number + 1}: {animal}')
                while 1:  # Choose cooperation pair.
                    try:
                        choice = list(map(int, (input("choose pair of animals (example: 1,3)")).split(',')))
                        if len(choice) != 2:
                            print("you have to input a PAIR of numbers-animals (example: 1,2)")
                            continue  # Choose cooperation loop.
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
                                animal_2.add_cooperation(animal_1)
                                print(
                                    f'animal_1: {animal_1.get_cooperation()}\tanimal_2: {animal_2.get_cooperation()}')
                                break  # Choose cooperation pair loop.
                    except:
                        print("exception choose pair animals! try again!")
                        continue  # Choose cooperation pair loop.
                return 1
            elif property_value == "symbiosys":
                for number, animal in enumerate(player.get_player_animals()):
                    print(f'{number + 1}: {animal}')
                while 1:  # Choose symbiosys pair loop
                    try:
                        choice = list(map(int, (input("choose pair of your animals animal/ "
                                                      "symbiont (1,3):")).split(',')))
                        if len(choice) != 2:
                            print("you have to input a PAIR of numbers-animals (example: 1,2)")
                            continue  # Choose symbiosys pair loop.
                        elif ((0 < choice[0] <= lenght_player_animals) and
                              (0 < choice[1] <= lenght_player_animals) and
                              (choice[0] != choice[1])):
                            animal_1 = player.get_player_animals()[choice[0] - 1]
                            animal_2_symbiont = player.get_player_animals()[choice[1] - 1]
                            if animal_2_symbiont in animal_1.get_symbiosys():
                                print("This animals had been already symbiote! try another card!")
                                player.cards_hand.append(card)
                                return 0
                            else:
                                animal_1.add_symbiosys(animal_2_symbiont)
                                print(f'animal_1: {animal_1.get_symbiosys()}')
                                break  # Choose symbiosys pair loop.
                    except:
                        print("exception choosing simbiont/ not simbiont! try again!")
                        continue  # Choose symbiosys pair loop.
                return 1
            elif property_value == "communication":
                for number, animal in enumerate(player.get_player_animals()):
                    print(f'{number + 1}: {animal}')
                while 1:  # Choose communication pair loop.
                    try:
                        choice = list(map(int, (input("choose pair of your animals (1,3):")).split(',')))
                        if len(choice) != 2:
                            print("you have to input a PAIR of numbers-animals (example: 1,2)")
                            continue  # Choose communication pair loop.
                        elif ((0 < choice[0] <= lenght_player_animals) and
                              (0 < choice[1] <= lenght_player_animals) and
                              (choice[0] != choice[1])):
                            animal_1 = player.get_player_animals()[choice[0] - 1]
                            animal_2 = player.get_player_animals()[choice[1] - 1]
                            if animal_1 in animal_2.get_communication() or animal_2 in animal_1.get_communication():
                                print("This animals had been already communicative! try another card!")
                                player.get_cards_hand().append(card)
                                return 0
                            else:
                                animal_1.add_communication(animal_2)
                                animal_2.add_communication(animal_1)
                                print(f'animal_1: {animal_1.get_communication()}\t'
                                      f'animal_2: {animal_2.get_communication()}')
                                break  # Choose communication pair loop.
                    except:
                        print("exception choosing animals for communication! try again!")
                        continue  # Choose communication pair loop.
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
                                players_list[player].get_player_animals()[animal].parasite += 1
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
    def exist_animals_to_hunt(animal: Animal, player_list: list):
        """
        return True if there are animals which it can hunt
        else: return False
        animal: Animal() instance - carnivorous
        player_list - list of Player() instances (to get animals)
        assume animal can hunt
        """

        assert isinstance(animal, Animal), f'exist_animals_to_hunt(): animal is not Animal() instance'
        assert animal.can_hunt(), f"exist_animals_to_hunt(): animal can't hunt!"
        for player in player_list:
            assert isinstance(player, Player), f'exist_animals_to_hunt(): {player} in player_list is not Player() ' \
                                               f'instance'

        for player in player_list:
            for victim in player.get_player_animals():
                if victim != animal:  # can not attack itself
                    if animal.can_attack(victim, False):
                        return True
        return False


class Development_Phase:
    """
    development phase
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

    def development_phase_function(self):
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
        return int -  number of red fish
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

    @staticmethod
    def grazing_function(player: Player, eating_base: int, user_input=functions.input_function):
        """
        player: Player instance
        change eating_base: int
        user_input - added to unit tst - to change user input in test.py
        return: int - new eating base
        """

        number = player.get_grazing_count()
        assert eating_base > 0, f'Eating_Phase.grazing_function() - self.eating base <= 0'
        assert number > 0, f'Eating_Phase.grazing_function() - number of animals with grazing property - 0'
        if number < eating_base:
            end_number = number
        else:
            end_number = eating_base
        destroy_number = user_input([str(number) for number in range(1, end_number + 1)],
                                    f'You are using grazing property to destroy eating base. Input number'
                                    f'to delay from eating base (1-{end_number})')
        if eating_base - int(destroy_number) > 0:
            eating_base = eating_base - int(destroy_number)
        else:
            print(f'Eating_phase.grazing_function(): destroy number > eating base')
            raise AssertionError
        print(f'new eating base = {eating_base}')
        return eating_base

    @staticmethod
    def communication(player: Player, animal: Animal, eating_base: int, user_input=functions.input_function):
        """
        Realize communication function - to realize ring of communication properties
        (communication property works only with red fish taking)
        player: Player() instance
        animal: Animal() instance
        eating_base: int - count of red fish
        user_input - function for user input (for test)
        assume animal in player.get_animals list
        assume: eating_base > 0
        assume: animal has communications relationships with other animals
        animal: Animal() instance
        eating_base: int - number of red fish in eating base
        user_input - to test to emulate user input
        return: int - new eating_base
        """
        assert isinstance(player, Player), f'Eating_Phase.communication(): player is not Player instance'
        assert type(eating_base) == int, f'Eating_Phase.communication(animal, eating base):, ' \
                                         f'eating_base is not integer'
        assert eating_base > 0, f'Eating_Phase.communication(animal, eating base):, ' \
                                f'eating_base < 0'
        assert isinstance(animal, Animal), f'Eating_Phase.communication(animal):, animal is not Animal() instance'
        assert animal in player.get_player_animals(), f'Eating_Phase.communication(): animal is not in players hand'
        assert animal.get_communication(), f'Eating_Phase.communication(animal):, animal has not communications'

        communicative_relationships = []
        #  initialize for first animal with hungry/ not full fat communicative animals
        for item in animal.get_communication():
            if item.can_eat():
                if item not in communicative_relationships:
                    communicative_relationships.append(item)
        took_red_fish = []
        first_animal = animal

        def recursive_find_communicate(animal: Animal, eating_base: int, user_input):
            # base case:

            if eating_base == 0 \
                    or not (set(communicative_relationships) - set(took_red_fish)) <= set(player.get_can_eat_animals()) \
                    or (len(took_red_fish) == len(communicative_relationships)):
                return eating_base
            else:
                # only one animal has communication property
                if len(communicative_relationships) - len(took_red_fish) == 1:
                    animal_to_take = (set(communicative_relationships) - set(took_red_fish)).pop()
                else:
                    # 2. ask player what animal should take  the red fish
                    to_choose_list = [x for x in communicative_relationships if (x not in took_red_fish) and (
                        x.can_eat())]
                    for number, _ in enumerate(to_choose_list):
                        print(f'{number + 1}: = {_}')

                    choose = user_input([str(_ + 1) for _ in range(len(to_choose_list))],
                                        f'please, select number of animal from communication list to '
                                        f'take red fish from eating base: ')

                    animal_to_take = to_choose_list[int(choose) - 1]

                eating_base -= 1

                if animal_to_take.get_hungry() > 0:
                    animal_to_take.increase_red_fish()
                    print(f'animal {animal_to_take} reduce hungry to {animal_to_take.get_hungry()}')
                elif animal_to_take.get_is_full_fat() > 0:
                    animal_to_take.increase_fat()
                    print(f'animal {animal_to_take} reduce fat to {animal_to_take.get_fat()}')
                else:
                    raise ValueError

                took_red_fish.append(animal_to_take)

                if animal_to_take.get_communication():
                    for item in animal_to_take.get_communication():
                        if item.can_eat():
                            if item not in communicative_relationships:
                                if item == first_animal and len(took_red_fish) == 1:
                                    continue
                                else:
                                    communicative_relationships.append(item)

                return recursive_find_communicate(animal_to_take, eating_base, user_input)

        eating_base = recursive_find_communicate(animal, eating_base, user_input)

        return eating_base

    @staticmethod
    def cooperation(player: Player, animal: Animal, user_input=functions.input_function):
        """
        Realize cooperation function - to realize ring of cooperation properties
        (cooperation property works only with blue fish taking)
        player: Player() instance
        animal: Animal() instance
        assume: animal has cooperation relationships with other animals
        animal: Animal() instance
        return: None
        """
        assert isinstance(player, Player), f'Eating_Phase.cooperation(animal):, player is not Player() instance'
        assert isinstance(animal, Animal), f'Eating_Phase.cooperation(animal):, animal is not Animal() instance'
        assert animal in player.get_player_animals(), f'Eating_Phase.cooperation(): animal is not in plyers animals'
        assert animal.get_cooperation(), f'Eating_Phase.cooperation(animal):, animal has not cooperations'
        cooperative_relationships = []
        #  initialize for first animal with hungry/ not full fat / not hungry symbiosys cooperative animals
        for item in animal.get_cooperation():
            if item.can_eat():
                if item not in cooperative_relationships:
                    cooperative_relationships.append(item)
        took_blue_fish = []
        first_animal = animal

        def recursive_find_cooperate(animal: Animal, user_input):
            # base case:

            if not (set(cooperative_relationships) - set(took_blue_fish)) <= set(player.get_can_eat_animals()) \
                    or (len(took_blue_fish) == len(cooperative_relationships)):
                return None

            else:

                if len(cooperative_relationships) - len(took_blue_fish) == 1:
                    # only one animal has communication property
                    animal_to_take = (set(cooperative_relationships) - set(took_blue_fish)).pop()
                else:
                    # 2. ask player what animal should take  the red fish
                    to_choose_list = [x for x in cooperative_relationships if (x not in took_blue_fish) and (
                        x.can_eat())]
                    for number, _ in enumerate(to_choose_list):
                        print(f'{number + 1}: = {_}')

                    choose = user_input([str(_ + 1) for _ in range(len(to_choose_list))],
                                        f'please, select number of animal from communication list to '
                                        f'take red fish from eating base: ')

                    animal_to_take = to_choose_list[int(choose) - 1]

                if animal_to_take.get_hungry() > 0:
                    animal_to_take.increase_blue_fish()
                    print(f'animal {animal_to_take} reduce hungry to {animal_to_take.get_hungry()}')
                elif animal_to_take.get_is_full_fat() > 0:
                    animal_to_take.increase_fat()
                    print(f'animal {animal_to_take} reduce fat to {animal_to_take.get_fat()}')
                else:
                    raise ValueError

                took_blue_fish.append(animal_to_take)

                if animal_to_take.get_cooperation():
                    for item in animal_to_take.get_cooperation():
                        if item.can_eat():
                            if item not in cooperative_relationships:
                                if item == first_animal and len(took_blue_fish) == 1:
                                    continue
                                else:
                                    cooperative_relationships.append(item)

                return recursive_find_cooperate(animal_to_take, user_input)

        recursive_find_cooperate(animal, user_input)

        return None

    @staticmethod
    def take_red_fish(player: Player, animal: Animal, eating_base):
        """
        player: Player() instance
        animal: Animal instance
        eating_base: int - self.eating base (red fish count)
        take red fish from eating base (if it exist - else raise error), reduce hungry or increase fat
        make pair properties
        assume animal can eat
        assume that eating base is not emtpy
        return int new eating base
        """

        assert isinstance(player, Player), f'Eating_phase.take_red_fish(): {player} is not Player instance'
        assert isinstance(animal, Animal), f'Eating_phase.take_red_fish(): {animal} is not Animal instance'
        assert animal in player.get_player_animals(), f'Eating_phase.take_red_fish(): {animal} is not in players hand'
        assert type(eating_base) == int, f'Eating_phase.take_red_fish(): {eating_base} is not integer'
        assert eating_base > 0, f'Eating_phase.take_red_fish(): {eating_base} <= 0'
        assert animal.can_eat(), f'Eating_phase.take_red_fish(): {animal} can not eat ' \
                                 f'(hungry={animal.get_hungry()}, free_Fat={animal.get_is_full_fat()},' \
                                 f'hungry_symbiosys={animal.exist_hungry_symbiosys()}))'

        eating_base -= 1
        # if animal is hungry
        if animal.get_hungry() > 0:
            animal.increase_red_fish()

        # if animal has free fat
        elif animal.get_is_full_fat() > 0:
            animal.increase_fat()

        # if animal communication
        if animal.get_communication() and eating_base > 0:
            eating_base = Eating_Phase.communication(player, animal, eating_base)
        # if animal cooperation
        if animal.get_cooperation():
            Eating_Phase.cooperation(player, animal)
        return eating_base

    @staticmethod
    def take_blue_fish(player: Player, animal: Animal):
        """
        player: Player() instance
        animal: Animal instance
        take blue fish reduce hungry or increase fat
        make pair properties
        assume animal can eat
        return None
        """
        assert isinstance(player, Player), f'Eating_phase.take_blue_fish(): {player} is not Player instance'
        assert isinstance(animal, Animal), f'Eating_phase.take_blue_fish(): {animal} is not Animal instance'
        assert animal in player.get_player_animals(), f'Eating_phase.take_blue_fish(): {animal} is not in players hand'
        assert animal.can_eat(), f'Eating_phase.take_blue_fish(): {animal} can not eat ' \
                                 f'(hungry={animal.get_hungry()}, free_Fat={animal.get_is_full_fat()},' \
                                 f'hungry_symbiosys={animal.exist_hungry_symbiosys()}))'

        # if animal is hungry
        if animal.get_hungry() > 0:
            animal.increase_blue_fish()

        # if animal has free fat
        elif animal.get_is_full_fat() > 0:
            animal.increase_fat()

        # if animal cooperation
        if animal.get_cooperation():
            Eating_Phase.cooperation(player, animal)

    @staticmethod
    def fat_to_blue_fish(animal: Animal, user_input=functions.input_function):
        """
        change fat cards to blue fish cards, decrease hungry
        animal: Animal instance
        user_input - function to user input
        assume Animal has fat cards
        assume animal is hungry
        return None
        """
        assert isinstance(animal, Animal), f'EatingPhase.fat_to_blue_fish(): animal is not Animal instance'
        assert animal.get_fat() > 0, f'EatingPhase.fat_to_blue_fish(): animal is not fat cards'
        assert animal.get_hungry() > 0, f'EatingPhase.fat_to_blue_fish(): animal is not hungry'

        number = user_input([str(x + 1) for x in range(animal.get_fat()) if x + 1 <= animal.get_hungry()],
                            f'choose number of fat to change to blue fish:')

        assert int(number) <= animal.get_fat(), f'Eating_Phase.fat_to_blue_fish() - number > fat cards'
        animal.reduce_fat(int(number))
        animal.increase_blue_fish(int(number))
        assert animal.get_hungry() >= 0, f'Eating_Phase.fat_to_blue_fish() - hungry reduced to negative'
        assert animal.get_fat() >= 0, f'Eating_Phase.fat_to_blue_fish() - fat reduced to negative'
        print(f'animal {animal} change {number} fat to blue cards: hungry={animal.get_hungry()}')

    @staticmethod
    def hibernation(animal: Animal):
        """
        Put animal in hibernation state, change hibernation ability to False
        animal: Animal instance
        assume animal has hibernation ability
        assume animal is not in hibernation state
        assume it is not last turn
        assume it is not used twice
        return: None
        """

        assert isinstance(animal, Animal), f'EatingPhase.hibernation(): animal is not Animal instance'
        assert animal.can_hibernate(), f'EatingPhase.hibernate(): animal can not hibernate now'

        animal.to_hibernate()
        animal.hibernation_possibility_False()

    @staticmethod
    def choose_animal_to_attack(animal: Animal, player_list: list, user_input=functions.input_function):
        """
        choose animal to attack in hunting process
        animal - Animal() instance - carnivorous
        player_list : list - list of Player() instances
        assume animal can hunt
        return animal - victim of hunting if animal can attack it
        else return False
        """
        assert isinstance(animal, Animal), f'Eating_Phase.choose_animal_to_attack(): animal is not Animal() instance'
        assert type(player_list) == list, f'Eating_Phase.choose_animal_to_attack(): player_list is not list'
        for player in player_list:
            assert isinstance(player, Player), f'Eating_Phase.choose_animal_to_attack(): {player} is not Player() ' \
                                               f'instnse'
        assert animal.can_hunt(), f'Eating_Phase.choose_animal_to_attack(): animal can not hunt'
        assert functions.exist_animals_to_hunt(animal, player_list), f'Eating_Phase.choose_animal_to_attack(): ' \
                                                                     f'there are not animals to attack'

        # print players and their animals
        for p_n, player in enumerate(player_list):
            print('*' * 10)
            print(f'{p_n + 1} {player.get_player_name()}\n')
            for n, a in enumerate(player.get_player_animals()):
                print(f'{n} {a}')

        # choose player - animal pair to attack
        choose_player = user_input([str(x + 1) for x in range(len(player_list))], f'choose number of player')
        player = player_list[int(choose_player)]
        choose_animal = user_input([str(x + 1) for x in range(len(player.get_player_animals()))],
                                   f'choose animal number to kill')
        victim = player.get_player_animals()[int(choose_animal)]

        # if animal can kill victim - return victim, else return false
        if animal.can_attack(victim):
            return victim
        else:
            return False

    @staticmethod
    def running_property(animal: Animal):
        """
        if attacked by carnivorous animal is running - roll the dice 4,5,6 - survive
        animal - Animal() instance
        assume animal has running property
        return True if victim survive, else - return False
        """

        assert isinstance(animal, Animal), f'Eating_Phase.running_property(): animal is not animal instance'
        assert animal.is_running(), f'Eating_Phase.running_property(): animal has not running property'

        dice = randint(1, 6)
        print(f'you roll the dice - number is {dice}')

        if dice in [4, 5, 6]:
            return True
        else:
            return False

    @staticmethod
    def tail_loss_property(animal: Animal):
        """
        if attacked by carnivorous animal is tail loss - it remove one of its properties
        animal - Animal() instance
        assume animal has tail loss property
        return True if victim loss tail, else - return False
        """

        assert isinstance(animal, Animal), f'Eating_Phase.running_property(): animal is not animal instance'
        assert animal.is_tail_loss(), f'Eating_Phase.running_property(): animal has not tail_loss property'

        # 1 take list of animal properties - if it is empty return false

        # 2 choose property to remove
        # 3 change single and pair properties

    @staticmethod
    def hunting(animal: Animal, player_list: list):
        """
        hunting process
        animal: Animal instance
        player_list - list of Player() instances
        assume animal is carnivorous
        assume animal can hunt
        assume there are animals to hunt
        return: None
        """
        assert isinstance(animal, Animal), f'EatingPhase.hunting(): animal is not Animal instance'
        assert type(player_list) == list, f'EatingPhase.hunting(): player_list is not list is {type(player_list)}'
        for player in player_list:
            assert isinstance(player, Player), f'Eating_Phase.hunting(): {player} is no Player() instance'
        assert animal.can_hunt(), f'EatingPhase.hunting(): animal can not hunt'
        assert functions.exist_animals_to_hunt(animal, player_list), f'EatingPhase.hunting(): there are not animals ' \
                                                                     f'to hunt'


'''

    def single_turn_eat(self, player, user_input=functions.input_function):
        """
        realize single turn of eating for player - Player() of eating phaze
        assume: Player has animals that can eat
        player: Player() instance
        user_input - function (for test, by default - function.input_function)
        """
        assert isinstance(player, Player)
        assert functions.exist_can_eat_animals(player.get_player_animals()), f'Eating_Phase.single_turn():' \
                                                                             f'there are not animals witch can eat ' \
                                                                             f'from these player (assume they would be)'
        print(f'{"-" * 10}active player - {player.get_player_name()} {"-" * 10}')

        active_player_hungry_animals = player.get_hungry_animals()
        active_player_not_full_fat = player.get_not_full_fat()
        active_player_piracy_animals = player.get_piracy()
        active_player_hubernation_ability = player.get_to_hibernation()
        active_player_in_hiberantion = player.get_in_hibernation()


        animals = player.get_player_animals()
        for number, animal in enumerate(animals):
            print(f'{number + 1}: {animal}')
        while True:  # choose loop
            animal_num = user_input([str(x + 1) for x in range(len(animals))],
                                    f'Please, select animal to take red fish from eating base: ')
            animal = animals[int(animal_num) - 1]
            if not animal.can_eat():
                print('this animal can not eat, please, choose another animal')
                continue  # choose loop
            else:
                break # choose loop




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
        # todo try to realize single round (whitout while main loop) realize function can eat - for animal with fat hungry symbiosys, not hebirnate
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
            active_player_symbiosus =
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
                # don't forget about symbiosysy!
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
        # fat card - to eat (it is not red or blue fish)

#  it global variable + I change name of thi function + I think that it is poor design to pass argument with the same
#  name... OMG - really shitcode...





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
'''

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
    razvitie = Development_Phase(players_list, first_number_player)
    razvitie.development_phase_function()
    define_eating_base_phase = Define_Eating_Base_Phase(players_list)
    food = define_eating_base_phase.get_food_count()
    print(define_eating_base_phase.get_text_of_phase())
