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
                                       f'({len(alternatives)})'
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
        return True if at least one element from list a are in list b
        assume a, b - lists
        return bool
        """""
        assert type(a) == list
        assert type(b) == list
        return any(i in b for i in a)

    @staticmethod
    def any_not_in(a: list, b: list):
        """
        return True if at least one element from list a are NOT in list b
        assume a, b - lists
        return bool
        """
        assert type(a) == list
        assert type(b) == list
        return any(i not in b for i in a)


class Players:
    """
    Players of evolution game
    """

    def __init__(self, user_input=Functions.input_function):

        self.players_list = []
        self.make_players_list(user_input)
        self.first_number_player = choice((self.get_player_list()))

    def make_players_list(self, user_input=Functions.input_function):
        """
        Make players list = [instances of Player class] by default min 2 max 8.
        Return None
        """

        choose = user_input([str(x + 1) for x in range(1, 8)], 'number of players (2-8): ')
        assert 2 <= int(choose) <= 8
        for i in range(int(choose)):
            self.players_list.append(Player())  # List of instances of Player class.

    def next_player(self, player):
        """
        Select next Player.
        return: next player
        """

        # find player in players list
        number = self.players_list.index(player)

        next_number = (number + 1) % len(self.get_player_list())

        return self.players_list[next_number]

    def get_player_list(self):
        """
        return copy of players_list
        """
        return self.players_list.copy()

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

    @staticmethod
    def get_animals_for_piracy(players_list: list):
        assert type(players_list) == list
        for player in players_list:
            assert isinstance(player, Player)

        result = []
        for player in players_list:
            for animal in player.get_player_animals():
                if (animal.get_red_fish() > 0 or animal.get_blue_fish() > 0) and animal.get_hungry() > 0:
                    result.append(animal)

        return result

    @staticmethod
    def get_alive_animals(player_list):
        """
        return alive animals (then carnivorous can try hunt)
        """
        result = []

        for player in player_list:
            for animal in player.get_player_animals():
                if animal.is_alive():
                    result.append(animal)

        return result


class Player:
    """ Player container of animals. """
    player_id = 0

    def __init__(self):
        self.cards_hand = []
        self.animals = []  # list of animals = animal()
        self.player_id = Player.player_id
        self.name = Player.player_id  # by default
        Player.player_id += 1

        # there are playing cards according to the rules and you can watch them at any time,
        # but I'm already working with properties - so far so.
        self.cards_dump = 0

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

    def increase_cards_dump(self, number=1):
        """
        increase cards damp to number (1 by default)
        return None
        """
        self.cards_dump += number

    def get_cards_damp(self):
        """
        return int: cards damp
        """
        return self.cards_dump

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

    def get_can_take_fish_animals(self):
        """
        return list of animals from player hand which can take red or blue fish
        """
        return [animal for animal in self.get_player_animals() if animal.can_take_fish()]

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

    def get_can_eat_animals(self):
        """
        returns list of animals which can eat (are hungry, not full fat, has not hungry symbiosys and not in hibernate
                                               or has fat and not in hibernate state)
        """
        result = [animal for animal in self.get_player_animals() if animal.can_eat()]

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
        player.increase_cards_dump()

        print(f'animal {self}, died...')

        # delete all pair properties

        if self.get_communication():
            for communicator in self.get_communication():
                communicator.remove_communication(self)
                player.increase_cards_dump()
            self.communication = []

        if self.get_cooperation():
            for cooperator in self.get_cooperation():
                cooperator.remove_cooperation(self)
                player.increase_cards_dump()
            self.cooperation = []

        for item in player.get_player_animals():
            if self in item.get_symbiosys():
                item.remove_symbiosys(self)
                player.increase_cards_dump()

        player.increase_cards_dump(len(self.get_single_animal_properties()))

    def increase_red_fish(self, number=1):
        """
        increase red fish count on number - 1 by default
        """
        self.red_fish_count += number

    def get_red_fish(self):
        """
        return int - red fish count
        """
        return self.red_fish_count

    def reduce_red_fish(self, number=1):
        """
        reduce red fish on number (1 by default)
        """
        assert self.get_red_fish() >= number

        self.red_fish_count -= number

    def increase_blue_fish(self, number=1):
        """
        increase blue fish count on number - 1 by default
        """
        self.blue_fish_count += number

    def get_blue_fish(self):
        """
        return int - blue fish count
        """
        return self.blue_fish_count

    def reduce_blue_fish(self, number=1):
        """
        reduce blue fish on number (1 by default)
        """
        assert self.get_blue_fish() >= number

        self.blue_fish_count -= number

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
        if self.is_hibernation_ability() and not self.hibernation_active:
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

    def from_hibernate(self):
        """
        wake up animal
        return None
        """
        self.hibernation_active = False

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

    def can_take_fish(self):
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

    def can_eat(self):
        """
        returns True if animal is hungry or has free fat slots and has not hungry symbiosys or has fat cards ,
        is not in hibernate status
        else: return False
        using in player.get_can_eat for eating phase function
        """
        if (self.get_hungry() > 0 or self.get_is_full_fat() > 0) \
                and not self.is_hibernate() \
                and not self.exist_hungry_symbiosys():
            return True
        elif self.get_hungry() > 0 and self.get_fat() and not self.is_hibernate():
            return True
        else:
            return False

    def can_hunt(self):
        """
        return True if animal can hunt (is carnivorous, can eat)
        else return False
        """
        if self.is_carnivorous() and self.can_take_fish():
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

    def find_players_animal_belong(self, players_list: list):
        """
        return player to which animal belong, or 'unknown_player' else
        """

        assert type(players_list) == list
        for player in players_list:
            assert isinstance(player, Player)

        player_id = self.get_belong_to_player_id()

        for player in players_list:
            if player.get_player_id() == player_id:
                assert self in player.get_player_animals()

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
            set_cards = self.cards.copy() * 4
            #
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!#
        # set_cards = self.cards.copy()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        elif 5 <= number_of_players <= 8:
            set_cards = self.cards.copy() * 8
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

    def __init__(self, players: Players, user_input=Functions.input_function):

        assert isinstance(players, Players)

        self.players = players
        self.players_list = players.get_player_list()
        self.first_player = players.first_number_player
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

        # pick communication
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
    def make_property(players_list, player: Player, property: str, user_input=Functions.input_function):
        """
        take property from card, try to put it on animal
        property - froperty from card from player's hand
        return True if can make this property, else return False
        """
        assert type(players_list) == list
        for _ in players_list:
            assert isinstance(_, Player)
        assert isinstance(player, Player), f'Development_Phase.make_parasite_property():' \
                                           f'player is not Player instance'
        assert player in players_list

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
        player = self.first_player

        print('Development phase:')
        while len(self.list_of_pass) != len(self.players_list):

            if player in self.list_of_pass:
                player = self.players.next_player(player)
                continue

            print('*' * 84)
            print(f'turn of player {player.get_player_name()}')

            # if player has not cards on his card_hand - automatically pass
            if len(player.get_handcards()) == 0:
                self.list_of_pass.append(player)
                player = self.players.next_player(player)
                continue

            # if player has animals
            if player.get_player_animals():

                # choose  say pass
                choose = user_input(['y', 'Y', 'n', 'N'], 'Do you want to say pass?')

                if choose == 'y':
                    self.list_of_pass.append(player)
                    player = self.players.next_player(player)
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
                player = self.players.next_player(player)
                continue

            elif choose == 'p':

                print('your animals are:')
                for animal in player.get_player_animals():
                    print(animal.get_animal_properties())

                property = Development_Phase.get_property_from_card(card, user_input)
                result = Development_Phase.make_property(self.players_list, player, property, user_input)

                if result:
                    player = self.players.next_player(player)
                    continue

                else:
                    print('can not realize this property - please choose another')
                    player.put_handcard(card)
                    continue

        print('End of development phase')


class Define_Eating_Base_Phase:

    def __init__(self, players: Players):

        assert isinstance(players, Players)

        players_number = len(players.get_player_list())

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

    def __init__(self, players: Players, eating_base: int, hibernate_list: list, is_last_turn=False):
        """
        eating_base: int - number of red fish from Define_Eating_Base_Phase
        is_last_turn - bool (False by default) if this turn is last - in last turn we can not use hibernation property
        hibernate_list- list of ani,als - which use hibernation in last turn - they can not use  this property again
        """

        assert type(eating_base) == int, f'Eating_Phase.__init__(): {eating_base} not integer'
        assert eating_base >= 0, f'Eating_Phase.__init__(): {eating_base} < 0'
        assert isinstance(players, Players)

        self.eating_base = eating_base
        self.is_last_turn = is_last_turn
        self.hibernate_list = hibernate_list
        self.players = players

        self.list_of_pass = set()
        self.new_hibernate_list = []
        self.animals_used_piracy = []
        self.animals_used_hunt = []

        self.player = self.players.first_number_player
        self.player_list = self.players.get_player_list()

    @staticmethod
    def grazing_function(eating_base: int, max_number: int, user_input=Functions.input_function):
        """
        change eating_base: int
        number - number of red fish to destroy: int
        user_input - added to unit tst - to change user input in test.py
        return: int - new eating base
        """

        assert eating_base > 0, f'Eating_Phase.grazing_function() - self.eating base <= 0'
        assert max_number > 0, f'Eating_Phase.grazing_function() - number of animals with grazing property - 0'

        if max_number < eating_base:
            end_number = max_number
        else:
            end_number = eating_base
        destroy_number = user_input([str(number) for number in range(1, end_number + 1)],
                                    f'You are using grazing property to destroy eating base. Input number'
                                    f'to delay from eating base (1-{end_number})')
        if eating_base - int(destroy_number) >= 0:
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
            if item.can_take_fish():
                if item not in communicative_relationships:
                    communicative_relationships.append(item)
        took_red_fish = []
        first_animal = animal

        def recursive_find_communicate(animal: Animal, eating_base: int, user_input):
            # base case:

            if eating_base == 0 \
                    or not (set(communicative_relationships) - set(took_red_fish)) <= set(
                player.get_can_take_fish_animals()) \
                    or (len(took_red_fish) == len(communicative_relationships)):
                return eating_base
            else:
                # only one animal has communication property
                if len(communicative_relationships) - len(took_red_fish) == 1:
                    animal_to_take = (set(communicative_relationships) - set(took_red_fish)).pop()
                else:
                    # 2. ask player what animal should take  the red fish
                    to_choose_list = [x for x in communicative_relationships if (x not in took_red_fish) and (
                        x.can_take_fish())]
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
                    print(f'animal {animal_to_take} increase fat to {animal_to_take.get_fat()}')
                else:
                    raise ValueError

                took_red_fish.append(animal_to_take)

                if animal_to_take.get_communication():
                    for item in animal_to_take.get_communication():
                        if item.can_take_fish():
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
            if item.can_take_fish():
                if item not in cooperative_relationships:
                    cooperative_relationships.append(item)
        took_blue_fish = []
        first_animal = animal

        def recursive_find_cooperate(animal: Animal, user_input):
            # base case:

            if not (set(cooperative_relationships) - set(took_blue_fish)) <= set(player.get_can_take_fish_animals()) \
                    or (len(took_blue_fish) == len(cooperative_relationships)):
                return None

            else:

                if len(cooperative_relationships) - len(took_blue_fish) == 1:
                    # only one animal has communication property
                    animal_to_take = (set(cooperative_relationships) - set(took_blue_fish)).pop()
                else:
                    # 2. ask player what animal should take  the red fish
                    to_choose_list = [x for x in cooperative_relationships if (x not in took_blue_fish) and (
                        x.can_take_fish())]
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
                    print(f'animal {animal_to_take} increase fat to {animal_to_take.get_fat()}')
                else:
                    raise ValueError

                took_blue_fish.append(animal_to_take)

                if animal_to_take.get_cooperation():
                    for item in animal_to_take.get_cooperation():
                        if item.can_take_fish():
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
        assert animal.can_take_fish(), f'Eating_phase.take_red_fish(): {animal} can not eat ' \
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
        assert animal.can_take_fish(), f'Eating_phase.take_blue_fish(): {animal} can not eat ' \
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
        assume player has more then 1 animals in his hand
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
    def attack_function(victim: Animal, carnivorous: Animal, players_list: list, mimicry_list: list,
                        user_input=Functions.input_function):
        """
        !recursive function at mimicry property!
        assume carnivorous can attack victim
        return number of blue fish after carnivorous attack animal: int
        """
        assert isinstance(victim, Animal)
        assert type(players_list) == list
        for _ in players_list:
            assert isinstance(_, Player)
        assert type(mimicry_list) == list
        assert isinstance(carnivorous, Animal)
        assert carnivorous.can_attack(victim)

        victim_player = victim.find_players_animal_belong(players_list)
        print(f'{victim_player.get_player_name()}, your animal is under attack!')

        if victim.is_running():
            result = Eating_Phase.running_property(victim)
            if result:
                return 0
        if victim.is_tail_loss():
            result = Eating_Phase.tail_loss_property(victim, user_input)
            if result:
                victim_player.increase_cards_dump()
                return 1
        if victim.is_mimicry() and victim not in mimicry_list:
            result = Eating_Phase.mimicry_property(carnivorous, victim, victim_player, mimicry_list, user_input)
            if result != False:  # if result = redirected_animal
                return Eating_Phase.attack_function(result, carnivorous, players_list, mimicry_list, user_input)

        victim.animal_death(victim_player)
        if victim.is_poisonous():
            carnivorous.poison()
        return 2

    @staticmethod
    def scavenger_property(player_hunter: Player, players: Players, user_input=Functions.input_function):
        """
        realise scavenger property
        return True if somebody can realize scavenger property else false
        """
        assert isinstance(player_hunter, Player)
        assert player_hunter in players.get_player_list()
        assert isinstance(players, Players)

        # for current player
        scavengers = player_hunter.get_scavenger_animals()
        if scavengers and Functions.any_in(scavengers, player_hunter.get_can_take_fish_animals()):
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
        player = players.next_player(player_hunter)
        while player != player_hunter:
            scavengers = player.get_scavenger_animals()
            if scavengers and Functions.any_in(scavengers, player.get_can_take_fish_animals()):
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

            player = players.next_player(player)

        return False

    @staticmethod
    def hunting(carnivorous: Animal, player_hunter: Player, players: Players, user_input=Functions.input_function):
        """
        hunting process
        animal: Animal instance
        player_list - list of Player() instances
        assume animal is carnivorous
        assume animal can hunt
        assume there are animals to hunt
        return: True if carnivorous attacked victim , else return false
        """
        assert isinstance(carnivorous, Animal), f'EatingPhase.hunting(): animal is not Animal instance'
        assert isinstance(players, Players)
        assert carnivorous.can_hunt(), f'EatingPhase.hunting(): animal can not hunt'
        assert isinstance(player_hunter, Player)
        assert carnivorous in player_hunter.get_player_animals()

        player_list = players.get_player_list()
        # choose animal to attack

        victim = Eating_Phase.choose_animal_to_attack(carnivorous, player_list, user_input)

        if not victim:
            print('you can not attack this animal')
            return False

        else:
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
                Eating_Phase.scavenger_property(player_hunter, players, user_input)

            return True

    @staticmethod
    def piracy_property(pirate: Animal, animals_to_piracy: list, players_list: list,
                        user_input=Functions.input_function):
        """
        realise piracy property
        pirate - Animal()
        animals_to_piracy - list of animals which already got red/blue fish in this turn, but still are hungry
        players_list - list of players
        assume pirate can eat
        assume pirate do not try to use piracy property on itself
        return True - if animal use piracy property - else return False
        """

        assert 'piracy' in pirate.get_single_animal_properties()
        assert isinstance(pirate, Animal)
        assert type(animals_to_piracy) == list
        assert pirate.can_take_fish()
        assert len(animals_to_piracy) >= 1
        assert not (len(animals_to_piracy) == 1 and pirate in animals_to_piracy)
        assert type(players_list) == list

        for player in players_list:
            assert isinstance(player, Player)

        print(f'{pirate} is pirate.')

        print('choose an animal to steal red/blue fish. The animal must receive fish this turn, but not be fed')
        player = Players.get_player_from_list(players_list, user_input)
        animal = player.get_player_animal(player, user_input)

        if animal == pirate:
            print(f'You can not steal food from yourself!')
            return False

        elif animal not in animals_to_piracy:
            print(f'You can not steal food from this animal!')
            return False
        else:
            if animal.get_blue_fish():
                animal.reduce_blue_fish()
            elif animal.get_red_fish():
                animal.reduce_red_fish()
            else:
                raise ValueError

            Eating_Phase.take_blue_fish(pirate.find_players_animal_belong(players_list), pirate)
            return True

    def make_buttons_for_animal(self, context, buttons: dict, eating_base: int, animals_to_piracy: list):
        """
        context - (animal, player, players_list) tuple
        buttons - look at eating phase turn
        """
        animal, player, players_list, history = context

        # pass
        if eating_base > 0 and player.get_hungry_animals():
            buttons['pass'] = False
        else:
            buttons['pass'] = True

        # next player
        buttons['next player'] = True

        # take red fish
        if eating_base > 0 and animal.can_take_fish() and \
                not Functions.any_in(['hunt', 'fat change', 'piracy', 'hibernate', 'grazing', 'take red fish'],
                                     history):
            buttons['take red fish'] = True

        # hunt
        if animal.can_hunt() and animal not in self.animals_used_hunt and \
                len(Players.get_alive_animals(players_list)) > 1 \
                and not Functions.any_in(['take red fish', 'fat change', 'piracy', 'hibernate', 'grazing', 'hunt'],
                                         history):
            buttons['hunt'] = True

        # fat_change
        if animal.get_hungry() > 0 and animal.get_fat() > 0 and \
                not Functions.any_in(['hunt', 'fat change', 'piracy', 'hibernate', 'grazing', 'take red fish'],
                                     history):
            buttons['fat change'] = True

        # hibernate
        if animal.can_hibernate() and animal not in self.hibernate_list and \
                not Functions.any_in(['hunt', 'fat change', 'piracy', 'hibernate', 'grazing'], history):
            if self.is_last_turn:
                buttons['hibernate'] = False
            else:
                buttons['hibernate'] = True

        # piracy
        if animal.is_piracy() and animal not in self.animals_used_piracy and animal.can_take_fish() and \
                animals_to_piracy and \
                not Functions.any_in(['hunt', 'fat change', 'piracy', 'hibernate', 'grazing'], history):

            if len(animals_to_piracy) == 1 and animal in animals_to_piracy:
                buttons['piracy'] = False
            else:
                buttons['piracy'] = True

        # grazing
        if eating_base > 0 and player.get_grazing_count() and \
                not Functions.any_in(['hunt', 'fat change', 'piracy', 'hibernate', 'grazing'], history):
            buttons['grazing'] = True

        # another animal
        if not Functions.any_in(['hunt', 'fat change', 'piracy', 'hibernate', 'grazing', 'take red fish'], history):
            if len(player.get_player_animals()) > 1:
                buttons['another animal'] = True

        return buttons

    def eating_phase(self, user_input=Functions.input_function):
        """
        base case - if all players says pass (self.list_of_pass)
        return None
        """

        print('*******************Eating phase*************************')
        player = self.player

        while len(self.list_of_pass) != len(self.player_list):  # main loop

            if not player.get_can_eat_animals():
                if player.get_grazing_count() == 0 or self.eating_base == 0:
                    self.list_of_pass.add(player)

            if player in self.list_of_pass:
                player = self.players.next_player(player)
                continue  # main loop

            buttons_template = {'pass': False, 'next player': False, 'take red fish': False, 'hunt': False,
                                'fat change': False, 'hibernate': False, 'piracy': False, 'grazing': False,
                                'another animal': False}

            history = []

            animals_to_piracy = Players.get_animals_for_piracy(self.player_list)

            # if there are not animals that can eat but has grazing animals
            if not player.get_can_eat_animals() and player.get_grazing_count():
                animal = player.get_player_animals()[0]

            # if there are animals that can eat
            else:
                # select animal from player hand
                animal = player.get_player_animal(player, user_input)

            while 1:  # loop choose
                context = (animal, player, self.player_list, history)
                buttons = self.make_buttons_for_animal(context, buttons_template.copy(), self.eating_base,
                                                       animals_to_piracy)

                variants = [button for button in buttons.keys() if buttons[button]]
                choose = user_input(variants, f'What do you want? {variants}: ')

                if choose == 'pass':
                    history.append(choose)
                    self.list_of_pass.add(player)
                    player = self.players.next_player(player)
                    break  # choose loop

                elif choose == 'next player':
                    history.append(choose)
                    player = self.players.next_player(player)
                    break  # choose loop

                elif choose == 'take red fish':
                    history.append(choose)
                    self.eating_base = Eating_Phase.take_red_fish(player, animal, self.eating_base, user_input)
                    continue  # choose loop

                elif choose == 'hunt':
                    result = Eating_Phase.hunting(animal, player, self.players, user_input)
                    if result:
                        history.append(choose)
                        self.animals_used_hunt.append(animal)
                        continue  # choose loop
                    else:
                        print('hunt was not successful')
                        continue  # choose loop

                elif choose == 'fat change':
                    history.append(choose)
                    Eating_Phase.fat_to_blue_fish(animal, user_input)
                    continue  # choose loop

                elif choose == 'hibernate':
                    history.append(choose)
                    animal.to_hibernate()
                    self.new_hibernate_list.append(animal)

                elif choose == 'piracy':
                    result = Eating_Phase.piracy_property(animal, animals_to_piracy, self.player_list,
                                                          user_input)
                    if result:
                        history.append(choose)
                        self.animals_used_piracy.append(animal)
                        continue  # choose loop
                    else:
                        print('piracy was not successful')
                        continue  # choose loop

                elif choose == 'grazing':
                    history.append(choose)
                    self.eating_base = Eating_Phase.grazing_function(self.eating_base,
                                                                     player.get_grazing_count(), user_input)
                    continue  # choose loop

                elif choose == 'another animal':
                    history = []
                    animal = player.get_player_animal(player)
                    continue  # choose loop

        print(f"{'*' * 30} End of eating phase {'*' * 30}")
        for player in self.player_list:
            print(f'player {player}')
            for animal in player.get_player_animals():
                print(f'{animal}')


class Extinction_Phase:
    """
    extinction phase
    """

    def __init__(self, players: Players, deck: Deck):

        assert isinstance(players, Players)
        assert isinstance(deck, Deck)
        self.players = players
        self.players_list = self.players.get_player_list()
        self.deck = deck

    def animal_extinction(self):
        """
        all hungry animals die
        return None
        """
        for player in self.players_list:
            for animal in player.get_player_animals():
                if (animal.get_hungry() > 0 and not animal.is_hibernate()) or animal.is_poisoned():
                    animal.animal_death(player)

    def take_playing_cards(self):
        """
        each player take cards from playing deck
        assume all hungry animals already died
        return None
        """
        excluded_list = []

        can_take_cards = dict()

        # initialize dictionary
        for player in self.players_list:
            if not player.get_player_animals() and not player.get_handcards():
                can_take_cards[player] = [6, 0]
            else:
                can_take_cards[player] = [len(player.get_player_animals()) + 1, 0]

        player = self.players.first_number_player

        while len(excluded_list) != len(self.players_list):

            # if deck is empty
            if len(self.deck.get_playing_deck()) == 0:
                break

            # if player took max number of cards
            if can_take_cards[player][0] == can_take_cards[player][1]:
                excluded_list.append(player)
                continue

            player.put_handcard(self.deck.take_deckcards()[0])
            can_take_cards[player][1] += 1
            player = self.players.next_player(player)

    def cleaning(self):
        """
        prepare to next turn
        assume all animal that have to die - died.
        """
        for player in self.players_list:

            for animal in player.get_player_animals():

                animal.reduce_red_fish(animal.get_red_fish())
                animal.reduce_blue_fish(animal.get_blue_fish())
                if animal.is_hibernate():
                    animal.from_hibernate()

    def extinction_phase(self):

        self.animal_extinction()
        self.cleaning()
        self.take_playing_cards()


def properties_count(player: Player):
    """
    assume all animals are alive
    count properties from player
    """
    assert isinstance(player, Player)
    count = 0
    single_properties = 0
    symbiosys_properties = 0
    comm_coop_properties = 0

    for animal in player.get_player_animals():
        count += 2
        single_properties += len(animal.get_single_animal_properties())
        symbiosys_properties += len(animal.get_symbiosys())
        comm_coop_properties += len(animal.get_communication())
        comm_coop_properties += len(animal.get_cooperation())

        if animal.is_high_body_weight() or animal.is_carnivorous():
            count += 1
        if 'parasite' in animal.get_single_animal_properties():
            count += 2

    result = count + single_properties + symbiosys_properties + (comm_coop_properties / 2)

    return int(result)


def scoring(players: Players):
    """
    score count
    print scores
    return None
    """
    assert isinstance(players, Players)
    score_dict = dict()

    for player in players.get_player_list():
        score_dict[player] = properties_count(player)

    for p, s in sorted(score_dict.items(), key=lambda item: item[1], reverse=True):
        print(f'{p.get_player_name()}\t total score: {s}\t cards damp = {p.get_cards_damp()}')


def game():
    """
    game of evolution
    """

    players = Players()

    deck = Deck(len(players.get_player_list()))

    for player in players.get_player_list():
        player.set_player_name()
        for _ in range(6):
            player.put_handcard(deck.take_deckcards()[0])

    while len(deck.get_playing_deck()) > 0:
        development_phase = Development_Phase(players)

        define_eating_base_phase = Define_Eating_Base_Phase(players)
        food = define_eating_base_phase.get_food_count()
        print(define_eating_base_phase.get_text_of_phase())

        eating_phase = Eating_Phase(players, food, [])
        eating_phase.eating_phase()

        extinction_phase = Extinction_Phase(players, deck)
        extinction_phase.extinction_phase()

        players.first_number_player = players.next_player(players.first_number_player)

    # last turn
    print('last turn')
    development_phase = Development_Phase(players)
    define_eating_base_phase = Define_Eating_Base_Phase(players)
    food = define_eating_base_phase.get_food_count()
    print(define_eating_base_phase.get_text_of_phase())

    eating_phase = Eating_Phase(players, food, [], is_last_turn=True)
    eating_phase.eating_phase()

    extinction_phase = Extinction_Phase(players, deck)
    extinction_phase.extinction_phase()

    scoring(players)


if __name__ == "__main__":
    game()

# change deck in make cards function - was changed to min value
# todo problem with take cards - two alive animals . tree cards on gand and take only 2 cards...
