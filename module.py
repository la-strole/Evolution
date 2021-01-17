"""
Created on 15 10 2017

@author: zhenya.aka.john@gmail.com
"""
from random import shuffle, randint, choice


class Functions:

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
    def exist_animals_to_hunt(carnivorous, player_list: list):
        """
        return True if there are animals which <animal> can hunt
        else: return False
        assume animal: Animal() instance - carnivorous
        player_list - list of Player() instances (to get animals)
        assume animal can hunt
        """

        assert isinstance(carnivorous, Animal), f'exist_animals_to_hunt(): animal is not Animal() instance'
        assert carnivorous.can_hunt(), f"exist_animals_to_hunt(): animal can't hunt!"
        for player in player_list:
            assert isinstance(player, Player), f'exist_animals_to_hunt(): {player} in player_list is not Player() ' \
                                               f'instance'

        for player in player_list:
            for victim in player.get_player_animals():
                if victim != carnivorous:  # can not attack itself
                    if carnivorous.can_attack(victim, False):
                        return True
        return False

    @staticmethod
    def any_in(a: list, b: list):
        """
        return True if any element from list a are in list b
        assume a, b - lists
        return bool
        """""
        assert type(a) == list
        assert type(b) == list
        return any(i in b for i in a)


class Players:
    """
    Players of evolution game
    """

    players_list = []
    first_number_player = False

    def __init__(self, user_input=Functions.input_function):
        Players.players_list = []
        self.make_players_list(user_input)
        Players.first_number_player = self.define_first_player(Players.get_player_list())

    @staticmethod
    def get_players_number():
        """
        return int - number of players
        """
        return len(Players.players_list)

    def make_players_list(self, user_input=Functions.input_function):
        """
        Make players list = [instances of Player class] by default min 2 max 8.
        Return None
        """

        choose = user_input([str(x + 1) for x in range(1, 8)], 'number of players (2-8): ')
        assert 2 <= int(choose) <= 8
        for i in range(int(choose)):
            Players.players_list.append(Player())  # List of instances of Player class.

    @staticmethod
    def next_player(player):
        """
        Select next Player.
        return: next player
        """
        assert isinstance(player, Player), f'player is not Player instance'

        # find player in players list
        number = Players.players_list.index(player)

        next_number = (number + 1) % Players.get_players_number()

        return Players.players_list[next_number]

    @staticmethod
    def get_player_list():
        """
        return copy of players_list
        """
        return Players.players_list.copy()

    def define_first_player(self, players_list):
        """
        return first player randomly from Players.players_list
        """
        first_player = choice(players_list)
        print(f'first player is {first_player.get_player_name()}')
        return first_player

    @staticmethod
    def get_player_from_list(players, user_input=Functions.input_function):
        """
        return player from players list, if list is empty - return False
        """
        assert type(players) == list
        for player in players:
            assert isinstance(player, Player)

        if not players:
            print('there are not players in list')
            return False

        for number, player in enumerate(players):
            print(f'{number + 1} {player}')

        choose = user_input([str(x + 1) for x in range(len(players))], 'choose player:')

        return players[int(choose) - 1]


class Player:
    """ Player container of animals. """
    player_id = 0

    def __init__(self):
        self.cards_hand = []
        self.animals = []  # list of animals = animal()
        self.player_id = Player.player_id
        self.name = Player.player_id  # by default
        Player.player_id += 1

    def __str__(self):
        return f'Player {self.name}'

    def __repr__(self):
        return f'{self.get_player_name()}'

    def get_player_id(self):
        """
        return: int player_id
        """
        return self.player_id

    def set_player_name(self):
        """
        set player's name player.name
        return: None
        """
        while True:
            try:
                name = str(input("input Player's name: "))
                break
            except ValueError:
                print("try to input another name")
        self.name = name

    def get_player_name(self):
        """
        return player's name
        """
        return self.name

    def get_handcards(self):
        """
        return cards_hand list
        """
        return self.cards_hand.copy()

    def take_handcard(self, user_input=Functions.input_function):
        """
        Take one card from <Player>'s hand and !remove! it from handcards
        return card
        """
        assert self.get_handcards()

        print('choose your card from hand:')
        for num, _ in enumerate(self.get_handcards()):
            print(f'{num + 1} {_}')

        card_num = user_input([(str(x + 1)) for x in range(len(self.get_handcards()))], 'select card number:')

        card = self.cards_hand.pop(int(card_num) - 1)

        return card

    def put_handcard(self, card):
        """
        add card to players hand
        return None
        """
        assert card in Deck.get_cards()
        self.cards_hand.append(card)

    def get_player_animals(self):
        """
        return player's animals list
        """
        for animal in self.animals.copy():
            assert animal.is_alive()

        return self.animals.copy()

    @staticmethod
    def get_player_animal(player, user_input=Functions.input_function, list_of_animals=None):
        """
        get animals from list of animals - by default - player.get_player_animals()
        player - Player instance
        assume player has animals
        user_input - function for test for test
        return: animal from player
        """

        if list_of_animals is None:
            list_of_animals = []
        assert isinstance(player, Player), f'Player.get_player_animal(): player is not Player instance'
        assert player.get_player_animals(), f'Player.get_player_animal(): player has not animals'
        assert type(list_of_animals) == list
        if list_of_animals:
            for animal in list_of_animals:
                assert isinstance(animal, Animal)
                assert animal in player.get_player_animals()

        print(f'choose animal from player {player.get_player_name()}')

        if not list_of_animals:
            list_of_animals = player.get_player_animals()

        for number, animal in enumerate(list_of_animals):
            print(f'{number + 1} {animal.get_animal_properties()}')

        choose = user_input([str(x + 1) for x in range(len(list_of_animals))],
                            'choose animal number')

        animal = list_of_animals[int(choose) - 1]
        assert animal.is_alive()
        return animal

    def make_animal(self):
        """
        append Animal() to player.animals.
        return None
        """
        print(f"Adding new Animal to you, {self.name}")

        self.animals.append(Animal(self.player_id))

        for number_animal, animal_instance in enumerate(self.get_player_animals()):
            print(f"Animal {number_animal + 1}:, {animal_instance.get_animal_properties()}")

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

    def get_scavenger_animals(self):
        """
        return list of animals which are scavengers
        """
        result = [animal for animal in self.get_player_animals() if animal.is_scavenger()]
        return result

    def get_animals_to_attack(self, carnivorous):
        """
        return list of animals from player hand, wich carnivorous can attack (without carnivorous)
        carnivorous - Animal()
        """
        assert isinstance(carnivorous, Animal)
        assert carnivorous.can_hunt()

        result = [victim for victim in self.get_player_animals() if carnivorous.can_attack(victim, False)]

        return result


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
        self.alive = True

    def __str__(self):
        return f'id={self.get_animal_id()}, {self.get_animal_properties()}, ' \
               f'free fat={self.get_is_full_fat()}'

    def __repr__(self):
        return f'id={self.animal_id}, free fat={self.get_is_full_fat()}, hungry={self.get_hungry()}'

    def get_animal_id(self):
        """
        return int: animal id
        """
        return self.animal_id

    def get_belong_to_player_id(self):
        """
        return player_id to which animal belongs: int
        """
        return self.belong_to_player

    def is_alive(self):
        """
        return True if animal is alive (animal.alive == True) else - False
        """
        return self.alive

    def animal_death(self, player):
        """
        process of animals death
        return None
        """
        assert isinstance(self, Animal)
        assert isinstance(player, Player)
        assert self in player.get_player_animals()

        self.alive = False
        player.animals.remove(self)
        print(f'animal {self}, died...')

        # delete all pair properties

        if self.get_communication():
            for communicator in self.get_communication():
                communicator.remove_communication(self)
            self.communication = []

        if self.get_cooperation():
            for cooperator in self.get_cooperation():
                cooperator.remove_cooperation(self)
            self.cooperation = []

        for item in player.get_player_animals():
            if self in item.get_symbiosys():
                item.remove_symbiosys(self)

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
        assert property in ['high_body_weight', 'swimming', 'sharp_vision', 'burrowing', 'carnivorous', 'parasite',
                            'hibernation_ability', 'tail_loss', 'mimicry', 'running', 'poisonous', 'grazing',
                            'scavenger', 'camouflage', 'piracy'], f'Animal.add_single_animal_property(): ' \
                                                                  f'property is not from deck single properties'

        assert property not in self.get_single_animal_properties()
        if property == 'scavenger':
            assert 'carnivorous' not in self.get_single_animal_properties()
        elif property == 'carnivorous':
            assert 'scavenger' not in self.get_single_animal_properties()

        self.single_properties.append(property)

    def remove_single_animal_property(self, property):
        """
        remove single animal property from animal properties (for tail loss function)
        assume property in animal properties
        return none
        """
        assert property in self.get_single_animal_properties()

        self.single_properties.remove(property)

        if property == 'hibernation_ability':
            self.hibernation_possibility_False()
            self.hibernation_active = False

        hungry = 1
        if 'high_body_weight' in self.get_single_animal_properties():
            hungry += 1
        if 'carnivorous' in self.get_single_animal_properties():
            hungry += 1
        if 'parasite' in self.get_single_animal_properties():
            hungry += 2

        while (hungry - self.red_fish_count - self.blue_fish_count) < 0:
            if self.red_fish_count > 0:
                self.red_fish_count -= 1
            else:
                self.blue_fish_count -= 1

        assert self.get_hungry() >= 0
        assert self.red_fish_count >= 0
        assert self.blue_fish_count >= 0

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
        properties.append(f'fat_cards={self.fat_cards_count}')
        properties.append('communications:')
        properties.extend(list_of_communications)
        properties.append('cooperations:')
        properties.extend(list_of_cooperations)
        properties.append('symbiosys:')
        properties.extend(list_of_symbiosys)
        properties.append(f'fat={fat_count}, hibernation state={hibernation_state}, poisoned={poisoned},'
                          f' hungry={hungry}')

        return properties

    def get_hungry(self):
        """
        return how hungry is animal: int
        """
        # return self.hungry
        hungry = 1
        if self.is_high_body_weight():
            hungry += 1
        if self.is_carnivorous():
            hungry += 1
        if self.has_parasite():
            hungry += 2

        result = hungry - self.red_fish_count - self.blue_fish_count
        assert result >= 0

        return result

    def get_fat_cards(self):
        """
        return number of fat cards: int
        """
        return self.fat_cards_count

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

    def add_fat_card(self):
        """
        add fat card and increase fat_Cards_count
        return None
        """
        self.fat_cards_count += 1

    def remove_fat_card(self):
        """
        remove fat card from animal
        return none
        """
        assert self.get_fat_cards() > 0

        self.fat_cards_count -= 1

        if self.fat > self.fat_cards_count:
            self.fat = self.fat_cards_count

    def has_parasite(self):
        """
        return True if animal has parasite, else return False
        """
        if 'parasite' in self.get_single_animal_properties():
            return True
        else:
            return False

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

    def is_poisoned(self):
        """
        returns if animal is poisoned
        """
        return self.poisoned

    def poison(self):
        """
        set poisoned state to True
        """
        self.poisoned = True

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

    def remove_symbiosys(self, symbiont):
        """
        remove symbiosys from animal symbiosys list (for lost tail property)
        symbiont - Animal() to remove
        assume symbiont in symbiosys list
        return None
        """
        assert isinstance(symbiont, Animal)
        assert symbiont in self.get_symbiosys()

        self.symbiosys.remove(symbiont)

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
        returns list - list of animals (instances of Animal class) communication to current animal
        """
        return self.communication.copy()

    def remove_communication(self, communicator):
        """
        remove communicator from animal communication list, remove animal from communicator cooperation list
        for tail loss function
        assume communicator - Animal()
        assume communicator in animal communication list
        return None
        """
        assert isinstance(communicator, Animal)
        assert communicator in self.get_communication()
        assert self in communicator.get_communication()

        self.communication.remove(communicator)
        communicator.communication.remove(self)

    def add_cooperation(self, animal):
        """
        animal: Animal() instance
        add cooperate to current animal, append it to animal.cooperate list
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

    def remove_cooperation(self, cooperator):
        """
        remove cooperator from animal cooperation list, remove animal from cooperator cooperation list
        for tail loss function
        assume cooperator - Animal()
        assume cooperator in animal cooperation list
        return None
        """
        assert isinstance(cooperator, Animal)
        assert cooperator in self.get_cooperation()
        assert self in cooperator.get_cooperation()

        self.cooperation.remove(cooperator)
        cooperator.cooperation.remove(self)

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
        print_msg - flag to not print message why currant animal can not attack current victim
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

    @staticmethod
    def find_players_animal_belong(animal, players_list: list):
        """
        return player to which animal belong, or 'unknown_player' else
        """
        assert isinstance(animal, Animal)
        assert type(players_list) == list
        for player in players_list:
            assert isinstance(player, Player)

        player_id = animal.get_belong_to_player_id()

        for player in players_list:
            if player.get_player_id() == player_id:
                assert animal in player.get_player_animals()
                return player

        return 'unknown_player'


class Deck:
    """
    deck of playing cards
    """

    cards = [("sharp_vision", "fat"), ("grazing", "fat"), ("parasite", "carnivorous"), ("parasite", "fat"),
             ("burrowing", "fat"), ("cooperation", "carnivorous"), ("cooperation", "fat"),
             ("poisonous", "carnivorous"),
             ("camouflage", "fat"), ("hibernation_ability", "carnivorous"), ("mimicry",), ("symbiosys",),
             ("scavenger",), ("piracy",), ("tail_loss",), ("running",), ("swimming",), ("swimming",),
             ("communication", "carnivorous"), ("high_body_weight", "fat"),
             ("high_body_weight", "carnivorous")]

    def __init__(self, number_of_players: int):
        self.playing_deck = self.make_deck(number_of_players)

    @staticmethod
    def get_cards():
        """
        return copy of cards list
        """
        return Deck.cards.copy()

    def make_deck(self, number_of_players: int):

        """
        Return set_cards -
        number_of_players = len(players_list)
        assume 2 <= number_of_players <= 8
        """
        assert type(number_of_players) == int, f'Deck:make_deck(): type of number of players is not int'
        assert 2 <= number_of_players <= 8, f'Deck:make_deck(): {number_of_players} not 2 <= number_of_players <= 8'

        # Making set_cards from cards and shuffling it,
        # set twice 'set_cards' for 5 - 8 players.
        if number_of_players < 5:
            set_cards = self.cards * 4
        elif 5 <= number_of_players <= 8:
            set_cards = self.cards * 8
        else:
            print("looks like this is something wrong with number_players!")
            raise ValueError
        shuffle(set_cards)
        return set_cards

    def take_deckcards(self, number=1):
        """
        takes <number> random cards from deck and returns them
        number - int - number of cards to take from the deck
        assume there are enough cards in deck to take
        return list of cards from deck
        """

        assert type(number) == int, f'Deck.take_deckcards: ({number}: number not an integer)'
        assert len(self.playing_deck) >= number, f'DEck.take_deckcards: ({self.playing_deck}: ' \
                                                 f'not enough cards to take to card hand)'

        cards_to_return = []
        for _ in range(number):
            cards_to_return.append(self.playing_deck.pop())

        return cards_to_return

    def get_playing_deck(self):
        """
        return copy of playing deck
        """
        return self.playing_deck.copy()


class Development_Phase:
    """
    development phase take players list and first player from Players class
    """

    def __init__(self, user_input=Functions.input_function):
        self.list_of_pass = []
        self.development_phase_function(user_input)

    @staticmethod
    def make_single_property(player: Player, property: str, user_input=Functions.input_function):
        """
        add single property to animal properties
        animal - Animal() instance
        assume property is not symbiosys, communication, cooperation, parasite, fat
        return True if property not in animal properties, else return False
        """

        assert type(property) == str, f'Development_Phase.make_single_property(): property is not string'
        assert isinstance(player, Player), f'Development_Phase.make_single_property(): player is not Player instance'

        if not player.get_player_animals():
            print('player has not animals')
            return False

        animal = player.get_player_animal(player, user_input)

        if property in animal.get_single_animal_properties():
            print('this animal already has this property')
            return False
        elif property == 'scavenger':
            if 'carnivorous' in animal.get_single_animal_properties():
                print('carnivorous can not be scavenger')
                return False
        elif property == 'carnivorous':
            if 'scavenger' in animal.get_single_animal_properties():
                print('scavenger can not be carnivorous')
                return False

        animal.add_single_animal_property(property)
        return True

    @staticmethod
    def make_symbiosys_property(player: Player, user_input=Functions.input_function):
        """
        add symionts (Animal() from player to animal.symbiosys list
        player - Player() instance
        assume player has more then 2 animals and they are not simbionts
        return True if property not in animal properties, and we can add symbiont else return False
        """

        assert isinstance(player, Player), f'Development_Phase.make_symbiosys_property(): player is not Player instance'

        if len(player.get_player_animals()) < 2:
            print('player has less then 2 animals')
            return False

        # pick animal
        print('choose animal:')
        animal = player.get_player_animal(player, user_input)

        # pick symbiont
        print('choose symbiont:')
        symbiont = player.get_player_animal(player, user_input)

        if symbiont == animal:
            print('you choose animal and symbiont for the same animal')
            return False

        elif symbiont in animal.get_symbiosys():
            print('your symbiont already in animal symbiosys')
            return False

        else:
            animal.add_symbiosys(symbiont)
            return True

    @staticmethod
    def make_communication_property(player: Player, user_input=Functions.input_function):
        """
        add communication/cooperation (Animal() from player
        player - Player() instance
        assume player has more then 2 animals and they are not communication
        return True if property not in animal properties, and we can add symbiont else return False
        """

        assert isinstance(player, Player), f'Development_Phase.make_comm_coop_property(): player is not Player instance'

        if len(player.get_player_animals()) < 2:
            print('player has less then 2 animals')
            return False

        # pick animal
        print('choose animal')
        animal1 = player.get_player_animal(player, user_input)

        # pick communication/cooperation
        print(f'choose communication animal')
        animal2 = player.get_player_animal(player, user_input)

        if animal2 == animal1:
            print(f'you choose animal and communication animal for the same animal')
            return False

        elif animal2 in animal1.get_communication():
            print('your animal already in another animal communications')
            return False

        elif animal1 in animal2.get_communication():
            print('your animal already in another animal communications')
            return False

        else:
            animal1.add_communication(animal2)
            animal2.add_communication(animal1)
            return True

    @staticmethod
    def make_cooperation_property(player: Player, user_input=Functions.input_function):
        """
        add communication/cooperation (Animal() from player
        player - Player() instance
        assume player has more then 2 animals and they are not communication
        return True if property not in animal properties, and we can add symbiont else return False
        """

        assert isinstance(player, Player), f'Development_Phase.make_comm_coop_property(): player is not Player instance'

        if len(player.get_player_animals()) < 2:
            print('player has less then 2 animals')
            return False

        # pick animal
        print('choose animal')
        animal1 = player.get_player_animal(player, user_input)

        # pick communication/cooperation
        print(f'choose cooperation animal')
        animal2 = player.get_player_animal(player, user_input)

        if animal2 == animal1:
            print(f'you choose animal and cooperation animal for the same animal')
            return False

        elif animal2 in animal1.get_cooperation():
            print('your animal already in another animal cooperation')
            return False

        elif animal1 in animal2.get_cooperation():
            print('your animal already in another animal cooperation')
            return False

        else:
            animal1.add_cooperation(animal2)
            animal2.add_cooperation(animal1)
            return True

    @staticmethod
    def make_fat_property(player: Player, user_input=Functions.input_function):
        """
        add fat property to players animal
        assume animal has free fat slots
        assume player has animals
        return True if can add a fat or False if can not
        """
        assert isinstance(player, Player), f'Development_Phase.make_fat_property(): player is not Player instance'

        if not player.get_player_animals():
            print('player has not animals')
            return False

        animal = player.get_player_animal(player, user_input)
        animal.add_fat_card()
        return True

    @staticmethod
    def make_parasite_property(players_list: list, user_input=Functions.input_function):
        """
        add parasite property to animal from all players
        players_list: list - list of Players()
        assume that animal hos not parasite property
        return True if success or False
        """
        assert type(players_list) == list, f'Development_Phase.make_parasite_property():' \
                                           f'players_list is not list'
        for player in players_list:
            assert isinstance(player, Player), f'Development_Phase.make_parasite_property():' \
                                               f'{player} is not Player instance'

        # choose player
        player = Players.get_player_from_list(players_list)

        # choose animals
        print('animal to give parasite:')
        animal = player.get_player_animal(player, user_input)

        if 'parasite' in animal.get_single_animal_properties():
            print('This animal already has parasite')
            return False
        else:
            animal.add_single_animal_property('parasite')
            return True

    @staticmethod
    def get_property_from_card(card: tuple, user_input=Functions.input_function):
        """
        get string - property from card
        assume card from Deck
        return: str property
        """

        # if card with single property
        if len(card) == 1:
            property = card[0]

        # if card with two properties
        else:
            print('your card has two properties:')
            for number, _ in enumerate(card):
                print(f'{number + 1} {_}')

            choose = user_input(['1', '2'], 'Choose property number(1,2)')
            property = card[int(choose) - 1]

        print(f'your property is {property}')
        return property

    @staticmethod
    def make_property(players_list, player: Player, card: tuple, user_input=Functions.input_function):
        """
        take property from card, try to put it on animal
        card - card from player's hand
        return True if can make this property, else return False
        """
        assert type(players_list) == list
        for _ in players_list:
            assert isinstance(_, Player)
        assert isinstance(player, Player), f'Development_Phase.make_parasite_property():' \
                                           f'player is not Player instance'
        assert player in players_list
        assert card in Deck.get_cards(), f'Development_Phase.make_parasite_property():' \
                                         f'{card} is not in cards of game'

        property = Development_Phase.get_property_from_card(card, user_input)

        if property == 'symbiosys':
            result = Development_Phase.make_symbiosys_property(player, user_input)
            if not result:
                return False

        elif property == 'communication':
            result = Development_Phase.make_communication_property(player, user_input)
            if not result:
                return False

        elif property == 'cooperation':
            result = Development_Phase.make_cooperation_property(player, user_input)
            if not result:
                return False

        elif property == 'fat':
            result = Development_Phase.make_fat_property(player, user_input)
            if not result:
                return False

        elif property == 'parasite':
            result = Development_Phase.make_parasite_property(players_list, user_input)
            if not result:
                return False

        else:
            result = Development_Phase.make_single_property(player, property, user_input)
            if not result:
                return False

        return True

    def development_phase_function(self, user_input=Functions.input_function):
        """
        development phase function - while all players not in list_of_pass
        return None
        """
        player = Players.first_number_player

        print('Development phase:')
        while len(self.list_of_pass) != Players.get_players_number():

            if player in self.list_of_pass:
                player = Players.next_player(player)
                continue

            print('*' * 84)
            print(f'turn of player {player.get_player_name()}')

            # if player has not cards on his card_hand - automatically pass
            if len(player.get_handcards()) == 0:
                self.list_of_pass.append(player)
                player = Players.next_player(player)
                continue

            # if player has animals
            if player.get_player_animals():

                # choose  say pass
                choose = user_input(['y', 'Y', 'n', 'N'], 'Do you want to say pass?')

                if choose == 'y':
                    self.list_of_pass.append(player)
                    player = Players.next_player(player)
                    continue

            # choose card from hand
            card = player.take_handcard(user_input)

            # if player has not animals yet
            if not player.get_player_animals():
                print('you have not animals yet')
                choose = 'a'

            else:
                # choose what do you want - animal or property
                choose = user_input(['a', 'A', 'p', 'P'], 'Do you want create animal (a) or property (p)?:')

            if choose == 'a':
                player.make_animal()
                player = Players.next_player(player)
                continue

            elif choose == 'p':

                print('your animals are:')
                for animal in player.get_player_animals():
                    print(animal.get_animal_properties())

                result = Development_Phase.make_property(Players.get_player_list(), player, card, user_input)

                if result:
                    player = Players.next_player(player)
                    continue

                else:
                    print('can not realize this property - please choose another')
                    player.put_handcard(card)
                    continue

        print('End of development phase')


class Define_Eating_Base_Phase:

    def __init__(self, players_number):

        assert 2 <= players_number < 8

        if players_number == 2:
            self.red_fish = randint(1, 6) + 2
        elif players_number == 3:
            self.red_fish = randint(1, 6) + randint(1, 6)
        elif players_number == 4:
            self.red_fish = randint(1, 6) + randint(1, 6) + 2
        elif players_number == 5:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + 2
        elif players_number == 6:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + 4
        elif players_number == 7:
            self.red_fish = randint(1, 6) + randint(1, 6) + randint(1, 6) + randint(1, 6) + 2
        elif players_number == 8:
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

    def __init__(self, players: list, first_number_player: Player, eating_base: int):
        """
        players: list - list of Players instances
        first_number_player: int - number of first player (from main)
        eating_base: int - number of red fish from Define_Eating_Base_Phase
        """
        assert type(players) == list, f'Eating_Phase.__init__(): type of players ({type(players)}) not list'
        assert 1 < len(players) <= 8, f'Eating_Phase.__init__(): len of players not 1 < ({len(players)} <= 8)'
        for player in players:
            assert isinstance(player, Player), f'Eating_Phase.__init__(): {player} not instance of Player class'
        assert isinstance(first_number_player, Player)
        assert type(eating_base) == int, f'Eating_Phase.__init__(): {eating_base} not integer'
        assert eating_base >= 0, f'Eating_Phase.__init__(): {eating_base} < 0'

        self.players = players
        self.first_player = first_number_player
        self.eating_base = eating_base

    @staticmethod
    def grazing_function(player: Player, eating_base: int, user_input=Functions.input_function):
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
            raise ValueError
        print(f'new eating base = {eating_base}')
        return eating_base

    @staticmethod
    def communication(player: Player, animal: Animal, eating_base: int, user_input=Functions.input_function):
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
    def cooperation(player: Player, animal: Animal, user_input=Functions.input_function):
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
        assert animal in player.get_player_animals(), f'Eating_Phase.cooperation(): animal is not in players animals'
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
    def take_red_fish(player: Player, animal: Animal, eating_base: int, user_input=Functions.input_function):
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
            eating_base = Eating_Phase.communication(player, animal, eating_base, user_input)

        # if animal cooperation
        if animal.get_cooperation():
            Eating_Phase.cooperation(player, animal, user_input)

        return eating_base

    @staticmethod
    def take_blue_fish(player: Player, animal: Animal):
        """
        player: Player() instance
        animal: Animal instance
        take blue fish reduce hungry or increase fat
        make pair properties
        assume animal can eat
        return True if animal can take blue fish , else return False
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
            if animal.get_cooperation():
                Eating_Phase.cooperation(player, animal)
            return True

        # if animal has free fat
        elif animal.get_is_full_fat() > 0:
            animal.increase_fat()
            if animal.get_cooperation():
                Eating_Phase.cooperation(player, animal)
            return True

        return False

    @staticmethod
    def fat_to_blue_fish(animal: Animal, user_input=Functions.input_function):
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
    def choose_animal_to_attack(animal: Animal, player_list: list, user_input=Functions.input_function):
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
                                               f'instance'
        assert animal.can_hunt(), f'Eating_Phase.choose_animal_to_attack(): animal can not hunt'

        print('choose player, animal to hunt:')
        player = Players.get_player_from_list(player_list, user_input)
        victim = player.get_player_animal(player, user_input)

        if victim == animal:
            print('you can not attack yourself')
            return False

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
    def tail_loss_property(animal: Animal, user_input=Functions.input_function):
        """
        if attacked by carnivorous animal is tail loss - it remove one of its properties
        animal - Animal() instance
        assume animal has tail loss property
        return True if animal loss tail else return False
        """

        assert isinstance(animal, Animal), f'Eating_Phase.running_property(): animal is not animal instance'
        assert animal.is_tail_loss(), f'Eating_Phase.running_property(): animal has not tail_loss property'

        choose = user_input(['Y', 'y', 'n', 'N'], f'your animal has tail loss property Do you want to use it? y/n: ')

        if choose == 'n':
            return False

        elif choose == 'y':
            # 1 take list of animal properties - if it is empty return false
            single_properties_cards = animal.get_single_animal_properties()
            symbiosys_properties_cards = animal.get_symbiosys()
            communication_properties_cards = animal.get_communication()
            cooperation_properties_cards = animal.get_cooperation()
            fat_cards = animal.get_fat_cards()

            number_single = len(single_properties_cards)
            number_symb = len(symbiosys_properties_cards)
            number_coop = len(cooperation_properties_cards)
            number_comm = len(communication_properties_cards)
            number_fat = fat_cards

            print('choose property to remove as tail:')
            for _, property in enumerate(single_properties_cards):
                print(f'{_ + 1} {property}')

            for _, symbiont in enumerate(symbiosys_properties_cards):
                print(f'{_ + number_single + 1} symbiosys {symbiont}')

            for _, cooperator in enumerate(cooperation_properties_cards):
                print(f'{_ + number_single + number_symb + 1} cooperators {cooperator}')

            for _, communicator in enumerate(communication_properties_cards):
                print(f'{_ + number_single + number_symb + number_coop + 1} communicator {communicator}')

            for _ in range(fat_cards):
                print(f'{_ + number_single + number_symb + number_coop + number_comm + 1} fat')

            all_numbers = number_fat + number_single + number_symb + number_comm + number_coop

            # 2 choose property to remove

            choose = user_input([str(x + 1) for x in range(all_numbers)], 'Choose property number to remove as tail: ')
            choose_num = int(choose) - 1

            if choose_num < number_single:
                tail = ('single', single_properties_cards[choose_num])

            elif choose_num < number_single + number_symb:
                tail = ('symbiosys', symbiosys_properties_cards[choose_num - number_single])
            elif choose_num < number_single + number_symb + number_coop:
                tail = ('cooperation', cooperation_properties_cards[choose_num - number_single - number_symb])
            elif choose_num < number_single + number_symb + number_coop + number_comm:
                tail = ('communication', communication_properties_cards[choose_num - number_single - number_symb -
                                                                        number_coop])
            elif choose_num < number_single + number_symb + number_coop + number_comm + number_fat:
                tail = ('fat_cards', 'fat')
            else:
                raise ValueError

            # 3 change single and pair properties, and relationships
            if tail[0] == 'single':
                print(f'you choose single property {tail[1]}')
                animal.remove_single_animal_property(tail[1])

            elif tail[0] == 'symbiosys':
                print(f'you choose symbiosys property with animal {tail[1]}')
                animal.remove_symbiosys(tail[1])

            elif tail[0] == 'cooperation':
                print(f'you choose cooperation property with animal {tail[1]}')
                animal.remove_cooperation(tail[1])

            elif tail[0] == 'communication':
                print(f'you choose communication property with animal {tail[1]}')
                animal.remove_communication(tail[1])

            elif tail[0] == 'fat_cards':
                print(f'you choose fat property')
                animal.remove_fat_card()

            return True

        else:
            raise ValueError

    @staticmethod
    def mimicry_property(carnivorous: Animal, animal: Animal, player: Player, mimicry_list: list,
                         user_input=Functions.input_function):
        """
        redirect attack from current animal to another animal in players hand
        assume player haas more then 1 animals in his hand
        return another animal or False
        """
        assert isinstance(animal, Animal)
        assert isinstance(carnivorous, Animal)
        assert isinstance(player, Player)
        assert animal in player.get_player_animals()
        assert 'mimicry' in animal.get_single_animal_properties()
        assert animal not in mimicry_list

        animals_to_redirect = player.get_animals_to_attack(carnivorous)
        # remove itself
        animals_to_redirect.remove(animal)
        # remove carnivorous
        if carnivorous in animals_to_redirect:
            animals_to_redirect.remove(carnivorous)
        # remove mimicry list members (those, who already used mimicry property)
        for item in mimicry_list:
            if item in animals_to_redirect:
                animals_to_redirect.remove(item)

        if not animals_to_redirect:
            return False

        else:

            choose = user_input(['Y', 'y', 'n', 'N'], f'your animal has mimicry property. Do you want to use it? y/n: ')

            if choose == 'n':
                return False

            elif choose == 'y':

                print('choose animal to redirect attack, you can choose only animal which carnivorous can attack')
                redirected_animal = player.get_player_animal(player, user_input)

                if redirected_animal == carnivorous:
                    print(f'you can not redirect attack to your attacker!')
                    return False

                elif not carnivorous.can_attack(redirected_animal):
                    print('carnivorous can not attack this animal. You can not use mimicry property')
                    return False

                elif redirected_animal == animal:
                    print('you can not redirect attack to yourself. Choose another animal:')
                    return False

                elif redirected_animal in mimicry_list:
                    print('you can not redirect attack to animal which already use mimicry redirection')
                    return False

                else:
                    mimicry_list.append(animal)
                    return redirected_animal

            else:
                raise ValueError

    @staticmethod
    def attack_function(victim: Animal, carnivorous: Animal, players: list, mimicry_list: list,
                        user_input=Functions.input_function):
        """
        !recursive function at mimicry property!
        assume carnivorous can attack victim
        return number of blue fish after carnivorous attack animal: int
        """
        assert isinstance(victim, Animal)
        assert type(players) == list
        for _ in players:
            assert isinstance(_, Player)
        assert type(mimicry_list) == list
        assert isinstance(carnivorous, Animal)
        assert carnivorous.can_attack(victim)

        victim_player = Animal.find_players_animal_belong(victim, players)
        print(f'{victim_player.get_player_name()}, your animal is under attack!')

        if victim.is_running():
            result = Eating_Phase.running_property(victim)
            if result:
                return 0
        if victim.is_tail_loss():
            result = Eating_Phase.tail_loss_property(victim, user_input)
            if result:
                return 1
        if victim.is_mimicry() and victim not in mimicry_list:
            result = Eating_Phase.mimicry_property(carnivorous, victim, victim_player, mimicry_list, user_input)
            if result != False:  # if result = redirected_animal
                return Eating_Phase.attack_function(result, carnivorous, players, mimicry_list, user_input)

        victim.animal_death(victim_player)
        if victim.is_poisonous():
            carnivorous.poison()
        return 2

    @staticmethod
    def scavenger_property(player_hunter: Player, user_input=Functions.input_function):
        """
        realise scavenger property
        return True if somebody can realize scavenger property else false
        """
        assert isinstance(player_hunter, Player)
        assert player_hunter in Players.get_player_list()

        # for current player
        scavengers = player_hunter.get_scavenger_animals()
        if scavengers and Functions.any_in(scavengers, player_hunter.get_can_eat_animals()):
            if len(scavengers) == 1:
                scavenger = scavengers[0]
                result = Eating_Phase.take_blue_fish(player_hunter, scavenger)
                if result:
                    print(f'animal {scavenger} took blue fish as scavenger')
                    return True
                else:
                    raise ValueError
            else:
                while True:
                    scavenger = player_hunter.get_player_animal(player_hunter, user_input, scavengers)
                    result = Eating_Phase.take_blue_fish(player_hunter, scavenger)
                    if result:
                        print(f'animal {scavenger} took blue fish as scavenger')
                        return True
        # for players clockwise
        player = Players.next_player(player_hunter)
        while player != player_hunter:
            scavengers = player.get_scavenger_animals()
            if scavengers and Functions.any_in(scavengers, player.get_can_eat_animals()):
                if len(scavengers) == 1:
                    scavenger = scavengers[0]
                    result = Eating_Phase.take_blue_fish(player, scavenger)
                    if result:
                        print(f'animal {scavenger} took blue fish as scavenger')
                        return True
                    else:
                        raise ValueError
                else:
                    while True:
                        scavenger = player.get_player_animal(player, user_input, scavengers)
                        result = Eating_Phase.take_blue_fish(player, scavenger)
                        if result:
                            print(f'animal {scavenger} took blue fish as scavenger')
                            return True

            player = Players.next_player(player)

        return False

    @staticmethod
    def hunting(carnivorous: Animal, player_hunter: Player, player_list: list, user_input=Functions.input_function):
        """
        hunting process
        animal: Animal instance
        player_list - list of Player() instances
        assume animal is carnivorous
        assume animal can hunt
        assume there are animals to hunt
        return: None
        """
        assert isinstance(carnivorous, Animal), f'EatingPhase.hunting(): animal is not Animal instance'
        assert type(player_list) == list, f'EatingPhase.hunting(): player_list is not list is {type(player_list)}'
        for _ in player_list:
            assert isinstance(player_hunter, Player), f'Eating_Phase.hunting(): {player_hunter} is no Player() instance'
        assert carnivorous.can_hunt(), f'EatingPhase.hunting(): animal can not hunt'
        assert Functions.exist_animals_to_hunt(carnivorous,
                                               player_list), f'EatingPhase.hunting(): there are not animals ' \
                                                             f'to hunt'
        assert isinstance(player_hunter, Player)
        assert carnivorous in player_hunter.get_player_animals()

        # choose animal to attack

        victim = Eating_Phase.choose_animal_to_attack(carnivorous, player_list, user_input)

        while not victim:
            print('you can not attack this animal')
            victim = Eating_Phase.choose_animal_to_attack(carnivorous, player_list, user_input)

        mimicry_list = []
        blue_fish = Eating_Phase.attack_function(victim, carnivorous, player_list, mimicry_list, user_input)

        for food in range(blue_fish):

            # if animal is hungry
            if carnivorous.get_hungry() > 0:
                carnivorous.increase_blue_fish()

            # if animal has free fat
            elif carnivorous.get_is_full_fat() > 0:
                carnivorous.increase_fat()

        # cooperation property - only one blue fish

        if blue_fish:  # if animal cooperation
            if carnivorous.get_cooperation():
                Eating_Phase.cooperation(player_hunter, carnivorous)

        # scavenger property

        if blue_fish == 2:  # if carnivorous killed victim
            Eating_Phase.scavenger_property(player_hunter, user_input)



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

    players = Players()
    deck = Deck(players.get_players_number())

    for player in players.get_player_list():
        player.set_player_name()
        for _ in range(6):
            player.put_handcard(deck.take_deckcards()[0])

    development_phase = Development_Phase()
    define_eating_base_phase = Define_Eating_Base_Phase(players.get_players_number())
    food = define_eating_base_phase.get_food_count()
    print(define_eating_base_phase.get_text_of_phase())
