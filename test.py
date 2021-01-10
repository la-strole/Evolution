import module
import unittest
from unittest.mock import patch
from random import randint


class TestEvolution(unittest.TestCase):

    @staticmethod
    def user_input_generator(chooses: list):
        """
        emulate user input - generator with results from list chooses
        chooses: list - list of str values to user input
        """
        assert type(chooses) == list, f'Test.Evolution.user_input_generator(): chooses is no list'
        for item in chooses:
            assert type(item) == str, f'Test.Evolution.user_input_generator(): not all chooses items are str'

        for item in chooses:
            yield item

    @staticmethod
    def user_input_emulator(*ars, chooses):
        """
        chooses: list - list of str values to user input
        returns next() of user_input_generator
        """
        assert type(chooses) == list, f'Test.Evolution.user_input_emulator(): chooses is no list'
        for item in chooses:
            assert type(item) == str, f'Test.Evolution.user_input_emulator(): not all chooses items are str'
        f = TestEvolution.user_input_generator(chooses)
        return next(f)

    def test_next_player(self):
        """ unit test for module.next_player(num: int, players: list)"""
        # type(num) == int
        num_test_cases_not_int = ['1', '', [1], (1,), {1: 1}]
        for test_case in num_test_cases_not_int:
            self.assertRaises(AssertionError, module.Functions.next_player, test_case, [1, 2, 3])
        # type(players) == list
        players_test_cases_not_list = ['1', '', (1,), {1: 1}]
        for test_case in players_test_cases_not_list:
            self.assertRaises(AssertionError, module.Functions.next_player, 1, test_case)
        # 1 < len(plyesrs) <= 7
        players_test_case = [-1000000000, -1, 0, 1, 8, 1000000000]
        for test_case in players_test_case:
            self.assertRaises(AssertionError, module.Functions.next_player, 1, test_case)
        # 0 <= num <= len(players)
        players_test_case = [1, 2, 3]  # relevant
        num_test_cases = [-100000000000, -1, 4, 100000000000]
        for test_case in num_test_cases:
            self.assertRaises(AssertionError, module.Functions.next_player, test_case, players_test_case)
        # num = 0
        self.assertEqual(module.Functions.next_player(0, [1, 2, 3]), 1)
        # num = len(players) - 1
        self.assertEqual(module.Functions.next_player(2, [1, 2, 3]), 0)
        # relevant test
        for i in range(10):
            players = [[1, 2], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7]]
            num_variants = [randint(0, 1), randint(0, 3), randint(0, 6)]
            result = map(module.Functions.next_player, num_variants, players)
            answer_matrix = [(n + 1) % len(p) for n, p in zip(num_variants, players)]
            # print(answer_matrix)
            for a, r in zip(answer_matrix, result):
                self.assertEqual(r, a)
        print('module.next_player(num: int, players: list) - OK')

    def test_development_phase(self):
        """
        unit test for module.development_phase(players: list, number: int) function
        """

        players_list = [module.Player('first_player'), module.Player('second_player')]
        cards = [("ostr", "zhir"), ("topo", "zhir"), ("para", "hish"), ("para", "zhir"),
                 ("norn", "zhir"), (["sotr"], "hish"), (["sotr"], "zhir"), ("jado", "hish"),
                 ("komm", "zhir"), ("spac", "hish"), ("mimi",), (["simb"],),
                 ("pada",), ("pira",), ("otbr",), ("bist",), ("vodo",), ("vodo",),
                 (["vzai"], "hish"), ("bols", "zhir"), ("bols", "hish")]
        hands = [("ostr", "zhir"), ("ostr", "zhir")]
        for player in players_list:
            player.cards_hand.extend(hands)
        first_number = 0
        razvitie = module.Development_Phase(players_list, first_number)
        """# if all players say pass (len(list_of_pass = len(players))
        razvitie.list_of_pass = players_list[:]
        razvitie.faza_rezvitija_function()
    # if current player in list_say_pass - next player
        razvitie = module.Faza_Razvitija(players_list[:], first_number)
        razvitie.list_of_pass.append(first_number)
        razvitie.faza_rezvitija_function()
    # if player has not cards in his hand - automatic pass
        players_list[0].set_cards_hand([])
        razvitie = module.Faza_Razvitija(players_list, first_number)
        razvitie.faza_rezvitija_function()
    #if active player don't have animals
        razvitie.test = True
        razvitie.faza_rezvitija_function()
        """

    def test_make_property(self):
        """
        unit test for make_property function
        """

        class Player(module.Player):
            def take_handcard(self):
                return 'carnivorous',

        class functions_test(module.Functions):

            @staticmethod
            def input_function(alternatives, greeting: str):
                return next(answers_generator)

        def gen_answer():
            # put here answers to question in list
            answers = ['1', 'y']
            for answer in answers:
                yield answer

        answers_generator = gen_answer()

        def clear_players(playerslist):
            playerslist = []

        players_list = [Player(str(x)) for x in range(3)]

        player = players_list[0]
        """# player has one animal
        player.get_player_animals().append(module.Animal())
        self.assertEqual(functions_test.make_property(player, players_list), 1)
        self.assertEqual('property' in player.get_player_animals()[0].get_animal_properties(), True)
        # if property value in animal_properties
        clear_players(players_list)
        players_list = [Player(str(x)) for x in range(3)]
        player = players_list[0]
        player.get_player_animals().append(module.Animal())
        player.get_player_animals()[0].get_animal_properties().append('property')
        self.assertEqual(functions_test.make_property(player, players_list), 0)
        self.assertEqual(('property',) in player.get_cards_hand(), True)
        
        # if property value == hish and pada in animal properties
        clear_players(players_list)
        players_list = [Player(str(x)) for x in range(3)]
        player = players_list[0]
        player.get_player_animals().append(module.Animal())
        player.get_player_animals()[0].get_animal_properties().append('hish')
        self.assertEqual(functions_test.make_property(player, players_list), 0)
        self.assertEqual(('pada',) in player.get_cards_hand(), True)
        """
        # if property value == pada and hish in animal properties
        clear_players(players_list)
        players_list = [Player(str(x)) for x in range(3)]
        player = players_list[0]
        player.animals.append(module.Animal())
        player.get_player_animals()[0].add_single_animal_property('scavenger')
        self.assertEqual(functions_test.make_property(player, players_list), 0)
        self.assertEqual(('carnivorous',) in player.get_handcards(), True)

    def test_init_Eating_Phase(self):
        """
        unit test for Eating_Phase constructor
        """
        # player not a list (int instead)
        self.assertRaises(AssertionError, module.Eating_Phase, players=1, first_number_player=0,
                          eating_base=5)
        # len of players < 1
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player()], first_number_player=0,
                          eating_base=5)
        # len of players > 8
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player() for x in range(9)],
                          first_number_player=0, eating_base=5)
        # not all players instances of Player() class
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player(), 1], first_number_player=0,
                          eating_base=5)
        # first number is no int type
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player, module.Player()],
                          first_number_player='1', eating_base=5)
        # first number < 0
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player, module.Player()],
                          first_number_player=-1, eating_base=5)
        # first number == 0
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player, module.Player()],
                          first_number_player=0, eating_base=5)
        # first number > len(players)
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player, module.Player()],
                          first_number_player=3, eating_base=5)
        # eating base not int type
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player, module.Player()],
                          first_number_player=1, eating_base='5')
        # eating base < 0
        self.assertRaises(AssertionError, module.Eating_Phase, players=[module.Player, module.Player()],
                          first_number_player=1, eating_base=-1)

    def test_get_grazing_count(self):
        """
        unit test for Player.get_grazing_count()
        """

        rand_animals = [module.Animal() for x in range(randint(1, 10))]
        for item in rand_animals:
            item.add_single_animal_property('grazing')
        # if player.get_grazing_count == len(animals)
        player = module.Player()
        player.animals = rand_animals
        self.assertEqual(player.get_grazing_count(), len(rand_animals))
        # if no animals with grazing property
        rand_animals = [module.Animal()]
        player.animals = rand_animals
        self.assertEqual(player.get_grazing_count(), 0)
        # if player has not animals at all
        player.animals = []
        self.assertEqual(player.get_grazing_count(), 0)

    def test_grazing_function(self):
        """
        unit test for grazing function
        """

        # define user input function
        def test_input1(*args):
            return '6'

        def test_input2(*args):
            return '2'

        players = [module.Player() for x in range(5)]
        # add grazing animlas to Player[0]
        grazing_animal = module.Animal()
        grazing_animal.add_single_animal_property('grazing')
        for i in range(5):
            players[0].animals.append(grazing_animal)
        # instance of eating Phase class
        eating_phase = module.Eating_Phase(players=players, first_number_player=0, eating_base=5)
        # eating base < 0
        eating_phase.eating_base = 0
        self.assertRaises(AssertionError, eating_phase.grazing_function, players[0], eating_phase.eating_base)
        # player has not grazing animals
        eating_phase.eating_base = 5
        self.assertRaises(AssertionError, eating_phase.grazing_function, players[1], eating_phase.eating_base)
        # destroy  elements > of eating base
        eating_phase.eating_base = 5
        self.assertRaises(AssertionError, eating_phase.grazing_function, players[0], eating_phase.eating_base,
                          test_input1)
        # destroy 2 elements of red fish
        eating_phase.eating_base = 5
        eating_phase.eating_base = eating_phase.grazing_function(players[0], eating_phase.eating_base, test_input2)
        self.assertEqual(eating_phase.eating_base, 3)

    def test_communication(self):
        """
        unit test for module.communication()
        """
        player = module.Player()
        # create animal
        animals = [module.Animal() for x in range(3)]
        player.animals = animals
        # test assertions
        # ------------------------
        # eating base <= 0
        eating_base = 0
        self.assertRaises(AssertionError, module.Eating_Phase.communication, player, animals[0], eating_base)
        # animal has communication property
        self.assertRaises(AssertionError, module.Eating_Phase.communication, player, animals[0], eating_base=4)
        # animal is no Animal intance
        self.assertRaises(AssertionError, module.Eating_Phase.communication, player, 1, eating_base=4)
        # -------------------------

        # first case two animals
        animals[0].add_communication(animals[1])
        animals[1].add_communication(animals[0])

        eating_base = module.Eating_Phase.communication(player, animals[0], eating_base=2)
        self.assertEqual(eating_base, 1)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[0].get_hungry(), 1)

        # second case tree in the ring and base case - len(took_red_fish) == len(communication_relation)
        animals = [module.Animal() for x in range(3)]
        player.animals = animals
        animals[0].add_communication(animals[1])
        animals[0].add_communication(animals[2])
        animals[1].add_communication(animals[0])
        animals[1].add_communication(animals[2])
        animals[2].add_communication(animals[0])
        animals[2].add_communication(animals[1])

        def user_answers(*args):
            return '1'

        eating_base = module.Eating_Phase.communication(player, animals[0], eating_base=3, user_input=user_answers)
        self.assertEqual(eating_base, 0)
        self.assertEqual(animals[0].get_hungry(), 0)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 0)

        # third case tree in the ring and base case - eating base == 0
        animals = [module.Animal() for x in range(3)]
        player.animals = animals
        animals[0].add_communication(animals[1])
        animals[0].add_communication(animals[2])
        animals[1].add_communication(animals[0])
        animals[1].add_communication(animals[2])
        animals[2].add_communication(animals[0])
        animals[2].add_communication(animals[1])

        def user_answers(*args):
            return '1'

        eating_base = module.Eating_Phase.communication(player, animals[0], eating_base=2, user_input=user_answers)
        self.assertEqual(eating_base, 0)
        self.assertEqual(animals[0].get_hungry(), 1)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 0)

        # forth case tree in the ring and base case - animals[2] can't eat
        animals = [module.Animal() for x in range(3)]
        player.animals = animals
        animals[0].add_communication(animals[1])
        animals[0].add_communication(animals[2])
        animals[1].add_communication(animals[0])
        animals[1].add_communication(animals[2])
        animals[2].add_communication(animals[0])
        animals[2].add_communication(animals[1])

        animals[2].add_symbiosys(module.Animal())

        def user_answers(*args):
            return '1'

        eating_base = module.Eating_Phase.communication(player, animals[0], eating_base=3, user_input=user_answers)
        self.assertEqual(eating_base, 2)
        self.assertEqual(animals[0].get_hungry(), 1)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 1)

        # fifth case six in the two rings
        animals = [module.Animal() for x in range(6)]
        player.animals = animals
        id = 1
        for animal in animals:
            animal.animal_id = id
            id += 1
        animals[0].add_communication(animals[1])
        animals[0].add_communication(animals[2])
        animals[0].add_communication(animals[3])
        animals[0].add_communication(animals[5])
        animals[1].add_communication(animals[0])
        animals[1].add_communication(animals[2])
        animals[1].add_communication(animals[4])
        animals[2].add_communication(animals[0])
        animals[2].add_communication(animals[1])
        animals[2].add_communication(animals[3])
        animals[3].add_communication(animals[2])
        animals[3].add_communication(animals[0])
        animals[4].add_communication(animals[1])
        animals[5].add_communication(animals[4])
        animals[5].add_communication(animals[0])

        def user_generator():
            answers = ['1', '4', '3', '3', '1']
            for answer in answers:
                yield answer

        f = user_generator()

        def user_input(*args):
            return next(f)

        eating_base = module.Eating_Phase.communication(player, animals[0], eating_base=6, user_input=user_input)
        self.assertEqual(eating_base, 0)
        self.assertEqual(animals[0].get_hungry(), 0)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 0)
        self.assertEqual(animals[3].get_hungry(), 0)
        self.assertEqual(animals[4].get_hungry(), 0)
        self.assertEqual(animals[5].get_hungry(), 0)


    def test_cooperation(self):
        """
        unit test for module.cooperation()
        """
        player = module.Player()
        # create animal
        animals = [module.Animal() for x in range(3)]
        player.animals = animals
        # test assertions
        # ------------------------

        # animal has cooperation property
        self.assertRaises(AssertionError, module.Eating_Phase.cooperation, player, animals[0])
        # animal is no Animal intance
        self.assertRaises(AssertionError, module.Eating_Phase.cooperation, player, 1)
        # -------------------------

        # first case two animals
        animals[0].add_cooperation(animals[1])
        animals[1].add_cooperation(animals[0])

        answer = module.Eating_Phase.cooperation(player, animals[0])
        self.assertEqual(answer, None)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[0].get_hungry(), 1)

        # second case tree in the ring and base case - len(took_blue_fish) == len(cooperation_relation)
        animals = [module.Animal() for _ in range(3)]
        player.animals = animals
        animals[0].add_cooperation(animals[1])
        animals[0].add_cooperation(animals[2])
        animals[1].add_cooperation(animals[0])
        animals[1].add_cooperation(animals[2])
        animals[2].add_cooperation(animals[0])
        animals[2].add_cooperation(animals[1])

        def user_answers(*args):
            return '1'

        eating_base = module.Eating_Phase.cooperation(player, animals[0], user_input=user_answers)
        self.assertEqual(eating_base, None)
        self.assertEqual(animals[0].get_hungry(), 0)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 0)

        # third case tree in the ring and base case - animals[2] can't eat
        animals = [module.Animal() for x in range(3)]
        player.animals = animals
        animals[0].add_cooperation(animals[1])
        animals[0].add_cooperation(animals[2])
        animals[1].add_cooperation(animals[0])
        animals[1].add_cooperation(animals[2])
        animals[2].add_cooperation(animals[0])
        animals[2].add_cooperation(animals[1])

        animals[2].add_symbiosys(module.Animal())

        def user_answers(*args):
            return '1'

        eating_base = module.Eating_Phase.cooperation(player, animals[0], user_input=user_answers)
        self.assertEqual(eating_base, None)
        self.assertEqual(animals[0].get_hungry(), 1)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 1)

        # fifth case six in the two rings
        animals = [module.Animal() for x in range(6)]
        player.animals = animals
        id = 1
        for animal in animals:
            animal.animal_id = id
            id += 1
        animals[0].add_cooperation(animals[1])
        animals[0].add_cooperation(animals[2])
        animals[0].add_cooperation(animals[3])
        animals[0].add_cooperation(animals[5])
        animals[1].add_cooperation(animals[0])
        animals[1].add_cooperation(animals[2])
        animals[1].add_cooperation(animals[4])
        animals[2].add_cooperation(animals[0])
        animals[2].add_cooperation(animals[1])
        animals[2].add_cooperation(animals[3])
        animals[3].add_cooperation(animals[2])
        animals[3].add_cooperation(animals[0])
        animals[4].add_cooperation(animals[1])
        animals[5].add_cooperation(animals[4])
        animals[5].add_cooperation(animals[0])

        def user_generator():
            answers = ['1', '4', '3', '3', '1']
            for answer in answers:
                yield answer

        f = user_generator()

        def user_input(*args):
            return next(f)

        eating_base = module.Eating_Phase.cooperation(player, animals[0], user_input=user_input)
        self.assertEqual(eating_base, None)
        self.assertEqual(animals[0].get_hungry(), 0)
        self.assertEqual(animals[1].get_hungry(), 0)
        self.assertEqual(animals[2].get_hungry(), 0)
        self.assertEqual(animals[3].get_hungry(), 0)
        self.assertEqual(animals[4].get_hungry(), 0)
        self.assertEqual(animals[5].get_hungry(), 0)

    '''
    def test_take_red_fish(self):

        """
        unit test for module.eating_phase.take_red_fish function
        """
        # test assertions
        # 1 animal is not Animal instance
        animal = 1
        player = module.Player()
        player.animals.append(animal)
        self.assertRaises(AssertionError, module.Eating_Phase.take_red_fish, player, animal, 5)
        # 2 type of eating base != int
        animal = module.Animal()
        player.animals.append(animal)
        self.assertRaises(AssertionError, module.Eating_Phase.take_red_fish, player, animal, '5')
        # 3 eating base <= 0
        animal = module.Animal()
        player.animals.append(animal)
        self.assertRaises(AssertionError, module.Eating_Phase.take_red_fish, player, animal, 0)
        self.assertRaises(AssertionError, module.Eating_Phase.take_red_fish, player, animal, -4)
        # 4 animal can't eat
        animal = module.Animal()
        player.animals.append(animal)
        animal.add_symbiosys(module.Animal())
        self.assertRaises(AssertionError, module.Eating_Phase.take_red_fish, player, animal, 2)

        # if animal is hungry, has free fat cards and it's symbionts are not hungry
        animal = module.Animal()
        player.animals.append(animal)
        symbiont = module.Animal()
        symbiont.increase_red_fish()
        animal.fat_cards_count = 1
        animal.add_symbiosys(symbiont)

        eating_base = module.Eating_Phase.take_red_fish(player, animal, 1)
        self.assertEqual(eating_base, 0)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.get_is_full_fat(), 1)
        self.assertEqual(animal.get_fat(), 0)

        # if animal is not hungry, but has free at cards and it's symbionts are not hungry
        animal = module.Animal()
        player.animals.append(animal)
        symbiont = module.Animal()
        symbiont.increase_red_fish()
        animal.increase_red_fish()
        animal.fat_cards_count = 1
        animal.add_symbiosys(symbiont)

        eating_base = module.Eating_Phase.take_red_fish(player, animal, 1)
        self.assertEqual(eating_base, 0)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.get_is_full_fat(), 0)
        self.assertEqual(animal.get_fat(), 1)


       
        # emulation user input
        #-----------------------------------------------------------------------------
        def user_answers(*args):
            answers = ['1', '2', '1', '1', '2', '1', '1', '1', '1', '1', '1', '1', '1', '1']
            for item in answers:
                yield item

        f = user_answers()

        def user_input(*ars):
            return next(f)
        #-----------------------------------------------------------------------------

        def standard_values(player):
            """
            set player's animals property to default values
            """
            for animal in player.animals:
                animal.hungry = 1
                animal.fat = 0
                animal.fat_cards_count = 0
                animal.simbiosys = []
                animal.communication = []
                animal.cooperation = []

        players = [module.Player() for x in range(5)]
        eating_phase = module.Eating_Phase(players, first_number_player=0, eating_base=5)
        # adding animals to player
        for i in range(3):
            players[0].animals.append(module.Animal())
        players[0].animals[0].hungry = 0
        # if animal is not hungry and has no free fat (look at text this animal is not hungry and is enough fat!
        # Choose another animal!) next animal is hungry
        # eating_phase.eating_base = 5
        eating_phase.take_red_fish(players[0], user_input, 5) # answers [0], [1]
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[1].fat, 0)
        self.assertEqual(eating_phase.eating_base, 4)
        # return standard values
        standard_values(players[0])
        # if animal is not hungry but has free fat
        eating_phase.eating_base = 5
        players[0].animals[0].hungry = 0
        players[0].animals[0].fat_cards_count = 1
        eating_phase.take_red_fish(players[0], user_input) # answers[2]
        self.assertEqual(eating_phase.eating_base, 4)
        self.assertEqual(players[0].animals[0].fat, 1)
        # return standards values
        standard_values(players[0])
        # if animal has hungry simbiont - it can't eat
        eating_phase.eating_base = 5
        # add symbiosis
        players[0].animals[0].add_symbiosys(players[0].animals[1])
        # symbiosys is hungry
        # look at text 'one of its symbionts is hungry: {symbiont} - this animal cant eat'
        eating_phase.take_red_fish(players[0], user_input) # answers [3], [4]
        self.assertEqual(eating_phase.eating_base, 4)
        # now symbiont is not hungry
        players[0].animals[1].hungry = 0
        eating_phase.take_red_fish(players[0], user_input) # answers [5]
        self.assertEqual(eating_phase.eating_base, 3)
        self.assertEqual(players[0].animals[0].hungry, 0)
        # set default values
        standard_values(players[0])
        eating_phase.eating_base = 5
        # if animal has communication
        # make communication property 0-1
        players[0].animals[0].add_communication(players[0].animals[1])
        players[0].animals[1].add_communication(players[0].animals[0])
        # 1. if communicator is hungry and there are enough red fish
        eating_phase.take_red_fish(players[0], user_input) # answers [6]
        self.assertEqual(eating_phase.eating_base, 3)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 0)
        # 2. if communicaotor is not hungry, but is  enough fat and there are enough red fish
        standard_values(players[0])
        eating_phase.eating_base = 5
        # make communication property 0-1
        players[0].animals[0].add_communication(players[0].animals[1])
        players[0].animals[1].add_communication(players[0].animals[0])
        players[0].animals[1].hungry = 0
        players[0].animals[1].fat_cards_count = 1
        eating_phase.take_red_fish(players[0], user_input)  # answers [7]
        self.assertEqual(eating_phase.eating_base, 3)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 1)
        # 3. if communicator is hungry but there are not enpugh red fish
        standard_values(players[0])
        eating_phase.eating_base = 1
        # make communication property 0-1
        players[0].animals[0].add_communication(players[0].animals[1])
        players[0].animals[1].add_communication(players[0].animals[0])
        eating_phase.take_red_fish(players[0], user_input)  # answers [8]
        self.assertEqual(eating_phase.eating_base, 0)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 1)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 0)
        # 4. if communicator is not hungry but has extra fat card - but not enough red fish
        standard_values(players[0])
        eating_phase.eating_base = 1
        # make communication property 0-1
        players[0].animals[0].add_communication(players[0].animals[1])
        players[0].animals[1].add_communication(players[0].animals[0])
        players[0].animals[1].hungry = 0
        players[0].animals[1].fat_cards_count = 1
        eating_phase.take_red_fish(players[0], user_input)  # answers [9]
        self.assertEqual(eating_phase.eating_base, 0)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 0)
        # cooperatopn property
        # set default values
        standard_values(players[0])
        eating_phase.eating_base = 5
        # if animal has cooperation
        # make cooperation property 0-1
        players[0].animals[0].add_cooperation(players[0].animals[1])
        players[0].animals[1].add_cooperation(players[0].animals[0])
        # 1. if cooperator is hungry and there are enough red fish
        eating_phase.take_red_fish(players[0], user_input)  # answers [10]
        self.assertEqual(eating_phase.eating_base, 4)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 0)
        # 2. if cooperator is not hungry, but is  enough fat and there are enough red fish
        standard_values(players[0])
        eating_phase.eating_base = 5
        # make cooperation property 0-1
        players[0].animals[0].add_cooperation(players[0].animals[1])
        players[0].animals[1].add_cooperation(players[0].animals[0])
        players[0].animals[1].hungry = 0
        players[0].animals[1].fat_cards_count = 1
        eating_phase.take_red_fish(players[0], user_input)  # answers [11]
        self.assertEqual(eating_phase.eating_base, 4)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 1)
        # 3. if cooperator is hungry but there are not enpugh red fish
        standard_values(players[0])
        eating_phase.eating_base = 1
        # make cooperation property 0-1
        players[0].animals[0].add_cooperation(players[0].animals[1])
        players[0].animals[1].add_cooperation(players[0].animals[0])
        eating_phase.take_red_fish(players[0], user_input)  # answers [12]
        self.assertEqual(eating_phase.eating_base, 0)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 0)
        # 4. if cooperator is not hungry but has extra fat card - but not enough red fish
        standard_values(players[0])
        eating_phase.eating_base = 1
        # make cooperation property 0-1
        players[0].animals[0].add_cooperation(players[0].animals[1])
        players[0].animals[1].add_cooperation(players[0].animals[0])
        players[0].animals[1].hungry = 0
        players[0].animals[1].fat_cards_count = 1
        eating_phase.take_red_fish(players[0], user_input)  # answers [13]
        self.assertEqual(eating_phase.eating_base, 0)
        self.assertEqual(players[0].animals[0].hungry, 0)
        self.assertEqual(players[0].animals[1].hungry, 0)
        self.assertEqual(players[0].animals[0].fat, 0)
        self.assertEqual(players[0].animals[1].fat, 1)
        
    '''

    def test_fat_to_blue_fish(self):
        """
        unit test for module.Eating_Phase.fat_to_blue_fish()
        """
        animal = module.Animal()

        # test assertions
        # if animal has not fat cards
        self.assertRaises(AssertionError, module.Eating_Phase.fat_to_blue_fish, animal)
        # if animal has fat cards but not hungry
        animal.fat_cards_count = 1
        animal.increase_fat()
        animal.increase_red_fish()
        self.assertRaises(AssertionError, module.Eating_Phase.fat_to_blue_fish, animal)

        # if we try to reduce hungry to negative
        animal = module.Animal()
        animal.fat_cards_count = 1
        animal.fat = 1

        def user_input(*args):
            return '2'

        self.assertRaises(AssertionError, module.Eating_Phase.fat_to_blue_fish, animal, user_input)

        # if everything is ok
        animal = module.Animal()
        animal.fat_cards_count = 1
        animal.fat = 1

        def user_input(*args):
            return '1'

        self.assertEqual(module.Eating_Phase.fat_to_blue_fish(animal, user_input), None)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.get_fat(), 0)
        self.assertEqual(animal.get_is_full_fat(), 1)




if __name__ == '__main__':
    unittest.main()
