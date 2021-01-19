import module
import unittest
import random
from unittest.mock import patch
from random import randint, sample
import subprocess


class TestEvolution(unittest.TestCase):

    @staticmethod
    def make_players_with_animals(num_p, num_a):
        """
        make players list with aniamls
        return Players instance
        """

        def user_input(*arg):
            return str(num_p)

        players = module.Players(user_input)

        for player in players.get_player_list():
            for _ in range(num_a):
                player.make_animal()

        return players

    def test_Functions_exist_animals_to_hunt(self):
        """
        unit test for Functions_exist_animals_to_hunt()
        """

        players = TestEvolution.make_players_with_animals(3, 2)

        # make carnivorous 1 aniaml of 1 player
        player1 = players.get_player_list()[0]
        carnivorous = player1.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # test if it can hunt - expect True
        self.assertEqual(module.Functions.exist_animals_to_hunt(carnivorous, players.get_player_list()), True)

        # test if 2 animal of 1 player is high_body_weght -> we need to check animal from 2 player
        animal1_2 = player1.get_player_animals()[1]
        animal1_2.add_single_animal_property('high_body_weight')
        self.assertEqual(module.Functions.exist_animals_to_hunt(carnivorous, players.get_player_list()), True)

        # test if false
        for player in players.get_player_list():
            for animal in player.get_player_animals():
                animal.add_single_animal_property('camouflage')
        self.assertEqual(module.Functions.exist_animals_to_hunt(carnivorous, players.get_player_list()), False)

    def test_class_Players(self):
        """
        unit test for Players init function
        """
        # number of players - random 2- 8
        number = randint(2, 8)

        def user_input(*args):
            return str(number)

        players = module.Players(user_input)
        self.assertEqual(players.get_players_number(), number)

        # number of players = 1
        number = 1

        def user_input(*args):
            return str(number)

        self.assertRaises(AssertionError, module.Players, user_input)

        # number of players = 9
        number = 9

        def user_input(*args):
            return str(number)

        self.assertRaises(AssertionError, module.Players, user_input)

    def test_class_player(self):
        """
        unit test for methods from class Player
        """

        module.Player.player_id = 0

        player1 = module.Player()
        player2 = module.Player()

        self.assertEqual(player1.get_player_id(), 0)
        self.assertEqual(player2.get_player_id(), 1)
        self.assertEqual(player1.get_player_name(), 0)
        self.assertEqual(player2.get_player_name(), 1)

        # get_handcards()

        card = 'bla'
        self.assertRaises(AssertionError, player1.put_handcard, card)
        card = ("sharp_vision", "fat")
        player1.put_handcard(card)
        self.assertEqual(player1.get_handcards(), [card])

        def user_input(*args):
            return '0'

        card = player1.take_handcard(user_input)
        self.assertEqual(card, ("sharp_vision", "fat"))
        self.assertEqual(player1.get_handcards(), [])

    def test_Deck_class(self):
        """
        unit test for Deck
        """
        deck = module.Deck(2)
        self.assertEqual(len(deck.get_playing_deck()), 4 * len(module.Deck.get_cards()))

        number_of_cards = randint(1, 15)
        cards = deck.take_deckcards(number_of_cards)
        self.assertEqual(type(cards), list)
        self.assertEqual(len(deck.get_playing_deck()), (4 * len(module.Deck.get_cards()) - number_of_cards))

    def test_development_phase(self):
        """
        unit test for development phase class
        """
        number_of_players = 2

        def user_input(*arg):
            return str(number_of_players)

        players_list = module.Players(user_input)

        mitja = players_list.first_number_player
        mitja.name = 'mitja'
        for player in players_list.get_player_list():
            if player != mitja:
                vanja = player
        vanja.name = 'vanja'

        mitja.put_handcard(("sharp_vision", "fat"))
        mitja.put_handcard(("poisonous", "carnivorous"))
        mitja.put_handcard(("cooperation", "fat"))
        mitja.put_handcard(("communication", "carnivorous"))
        mitja.put_handcard(("poisonous", "carnivorous"))
        mitja.put_handcard(("grazing", "fat"))
        print(f'mitja hand: {mitja.get_handcards()}')

        vanja.put_handcard(("sharp_vision", "fat"))
        vanja.put_handcard(("poisonous", "carnivorous"))
        vanja.put_handcard(("communication", "carnivorous"))
        vanja.put_handcard(("camouflage", "fat"))
        vanja.put_handcard(("grazing", "fat"))
        vanja.put_handcard(("burrowing", "fat"))
        print(f'vanja hand: {vanja.get_handcards()}')

        # structure of the longest string^
        # 'n' - do you want to say pass?
        # '1' - choose card from card hand (every turn 1 - because they shift to top
        # 'p' - animal/property?
        # '1' - your card has two properties - choose one of them
        # '1' - for animal
        # '2' - for second animal if it is pair property (like communication, cooperation, symbiosus)

        answers = ['1',  # mitja add first animal
                   '1',  # vanja add first animal
                   'n', '1', 'p', '1', '1',  # mitja add poisonous property to 1 animal
                   'n', '1', 'a',  # vanja add second animal
                   'n', '1', 'a',  # mitja add second animal
                   'n', '1', 'p', '1', '1', '2',  # vanja add communication to animals 1,2
                   'n', '1', 'p', '2', '1',  # mitja add carnivorous to second animal
                   'n', '1', 'p', '1', '2',  # vanja add camouflage to second animal
                   'n', '1', 'a',  # mitja add third animal
                   'n', '1', 'p', '1', '2',  # vanja add grazing to second animal
                   'y',  # mitja say pass
                   'n', '1', 'p', '2', '2']  # vanja add fat to second animal

        def gen_answers(answers):
            for answer in answers:
                print(f'user answer = {answer}')
                yield answer

        user_gen = gen_answers(answers)

        def user_input(*args):
            return next(user_gen)

        development_phase = module.Development_Phase(user_input)

        self.assertEqual(len(mitja.get_player_animals()), 3)
        self.assertEqual(len(vanja.get_player_animals()), 2)

        animal_m_1 = mitja.get_player_animals()[0]
        animal_m_2 = mitja.get_player_animals()[1]
        animal_m_3 = mitja.get_player_animals()[2]

        animal_v_1 = vanja.get_player_animals()[0]
        animal_v_2 = vanja.get_player_animals()[1]

        self.assertEqual(animal_m_1.is_carnivorous(), True)
        self.assertEqual(animal_m_1.is_poisonous(), True)
        self.assertEqual(animal_m_1.get_hungry(), 2)

        self.assertEqual(animal_m_2.get_hungry(), 1)
        self.assertEqual(animal_m_2.get_single_animal_properties(), [])
        self.assertEqual(animal_m_2.get_fat(), 0)

        self.assertEqual(animal_m_3.get_hungry(), 1)
        self.assertEqual(animal_m_3.get_single_animal_properties(), [])
        self.assertEqual(animal_m_3.get_fat(), 0)

        print(f'animal_m_1: {animal_m_1.get_animal_properties()}')
        print(f'animal_m_2: {animal_m_2.get_animal_properties()}')
        print(f'animal_m_3: {animal_m_3.get_animal_properties()}')

        self.assertEqual(animal_v_1.get_hungry(), 1)
        self.assertEqual(animal_v_1.get_single_animal_properties(), [])
        self.assertEqual(animal_v_1.get_fat(), 0)

        self.assertEqual(animal_v_2.get_hungry(), 1)
        self.assertEqual(animal_v_2.get_single_animal_properties(), ['camouflage', 'grazing'])
        self.assertEqual(animal_v_2.get_fat(), 0)
        self.assertEqual(animal_v_2.fat_cards_count, 1)
        self.assertEqual(animal_v_2 in animal_v_1.get_communication(), True)
        self.assertEqual(animal_v_1 in animal_v_2.get_communication(), True)

        print(f'animal_v_1: {animal_v_1.get_animal_properties()}')
        print(f'animal_v_2: {animal_v_2.get_animal_properties()}')



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
        eating_phase = module.Eating_Phase(eating_base=5, hibernate_list=[])
        # eating base < 0
        eating_phase.eating_base = 0
        self.assertRaises(AssertionError, eating_phase.grazing_function, eating_phase.eating_base, 2)
        # destroy  elements > of eating base
        eating_phase.eating_base = 5
        self.assertRaises(ValueError, eating_phase.grazing_function, eating_phase.eating_base, 2,
                          test_input1)
        # destroy 2 elements of red fish
        eating_phase.eating_base = 5
        eating_phase.eating_base = eating_phase.grazing_function(eating_phase.eating_base, 2, test_input2)
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

    def test_take_red_fish(self):

        """
        unit test for module.eating_phase.take_red_fish function
        """

        # 1 if animal is hungry

        eating_base = 3
        player = module.Player()
        for _ in range(3):
            player.make_animal()
        animal = player.get_player_animals()[0]
        result = module.Eating_Phase.take_red_fish(player, animal, eating_base)
        self.assertEqual(result, 2)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.red_fish_count, 1)
        self.assertEqual(animal.blue_fish_count, 0)
        self.assertEqual(animal.fat, 0)

        # 2 if animal is not hungry bau has free fat

        eating_base = 3
        player = module.Player()
        for _ in range(3):
            player.make_animal()
        animal = player.get_player_animals()[0]
        animal.increase_red_fish()
        animal.add_fat_card()
        result = module.Eating_Phase.take_red_fish(player, animal, eating_base)
        self.assertEqual(result, 2)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.red_fish_count, 1)
        self.assertEqual(animal.blue_fish_count, 0)
        self.assertEqual(animal.fat, 1)

        # 3 if animal communication

        eating_base = 3
        player = module.Player()
        for _ in range(3):
            player.make_animal()
        animal1 = player.get_player_animals()[0]
        animal2 = player.get_player_animals()[1]
        animal3 = player.get_player_animals()[2]

        animal1.add_communication(animal2)
        animal1.add_communication(animal3)
        animal2.add_communication(animal1)
        animal2.add_communication(animal3)
        animal3.add_communication(animal1)
        animal3.add_communication(animal2)

        def user_input(*arg):
            return '1'

        result = module.Eating_Phase.take_red_fish(player, animal1, eating_base, user_input)
        self.assertEqual(result, 0)
        self.assertEqual(animal1.get_hungry(), 0)
        self.assertEqual(animal1.red_fish_count, 1)
        self.assertEqual(animal1.blue_fish_count, 0)
        self.assertEqual(animal1.fat, 0)
        self.assertEqual(animal2.get_hungry(), 0)
        self.assertEqual(animal2.red_fish_count, 1)
        self.assertEqual(animal2.blue_fish_count, 0)
        self.assertEqual(animal2.fat, 0)
        self.assertEqual(animal3.get_hungry(), 0)
        self.assertEqual(animal3.red_fish_count, 1)
        self.assertEqual(animal3.blue_fish_count, 0)
        self.assertEqual(animal3.fat, 0)

        # 4 if animal cooperation

        eating_base = 3
        player = module.Player()
        for _ in range(3):
            player.make_animal()
        animal1 = player.get_player_animals()[0]
        animal2 = player.get_player_animals()[1]
        animal3 = player.get_player_animals()[2]

        animal1.add_cooperation(animal2)
        animal1.add_cooperation(animal3)
        animal2.add_cooperation(animal1)
        animal2.add_cooperation(animal3)
        animal3.add_cooperation(animal1)
        animal3.add_cooperation(animal2)

        def user_input(*arg):
            return '1'

        result = module.Eating_Phase.take_red_fish(player, animal1, eating_base, user_input)
        self.assertEqual(result, 2)
        self.assertEqual(animal1.get_hungry(), 0)
        self.assertEqual(animal1.red_fish_count, 1)
        self.assertEqual(animal1.blue_fish_count, 0)
        self.assertEqual(animal1.fat, 0)
        self.assertEqual(animal2.get_hungry(), 0)
        self.assertEqual(animal2.red_fish_count, 0)
        self.assertEqual(animal2.blue_fish_count, 1)
        self.assertEqual(animal2.fat, 0)
        self.assertEqual(animal3.get_hungry(), 0)
        self.assertEqual(animal3.red_fish_count, 0)
        self.assertEqual(animal3.blue_fish_count, 1)
        self.assertEqual(animal3.fat, 0)

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

    def test_tail_loss_property(self):
        """
        unit test for tail loss property
        """

        # tail = tail loss card

        animal = module.Animal()
        animal.add_single_animal_property('tail_loss')

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '1']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_single_animal_properties()), 0)
        print(animal.get_animal_properties())

        # add another single property

        animal = module.Animal()
        animal.add_single_animal_property('tail_loss')
        animal.add_single_animal_property('piracy')

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '2']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_single_animal_properties()), 1)
        print(animal.get_animal_properties())

        # add "high body weight" single properties"

        animal = module.Animal()
        animal.add_single_animal_property('tail_loss')
        animal.add_single_animal_property('high_body_weight')
        animal.add_single_animal_property('piracy')

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '2']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(animal.get_hungry(), 2)
        animal.increase_red_fish(2)
        self.assertEqual(animal.get_hungry(), 0)
        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_single_animal_properties()), 2)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.red_fish_count, 1)
        print(animal.get_animal_properties())

        # add "parasite, carnivorous" single properties"

        animal = module.Animal()
        animal.add_single_animal_property('tail_loss')
        animal.add_single_animal_property('high_body_weight')
        animal.add_single_animal_property('parasite')
        animal.add_single_animal_property('carnivorous')

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '3']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(animal.get_hungry(), 5)
        animal.increase_red_fish(1)
        animal.increase_blue_fish(4)
        self.assertEqual(animal.get_hungry(), 0)
        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_single_animal_properties()), 3)
        self.assertEqual(animal.get_hungry(), 0)
        self.assertEqual(animal.red_fish_count, 0)
        self.assertEqual(animal.blue_fish_count, 3)
        print(animal.get_animal_properties())

        # add symbiosys property

        animal = module.Animal()
        symbiont1 = module.Animal()
        symbiont2 = module.Animal()
        animal.add_single_animal_property('tail_loss')
        animal.add_symbiosys(symbiont1)
        animal.add_symbiosys(symbiont2)
        animal.add_single_animal_property('piracy')

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '4']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(animal.get_hungry(), 1)
        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_single_animal_properties()), 2)
        self.assertEqual(len(animal.get_symbiosys()), 1)
        self.assertEqual(symbiont1 in animal.get_symbiosys(), True)
        print(animal.get_animal_properties())

        # add different properties

        animal = module.Animal()
        symbiont1 = module.Animal()
        symbiont2 = module.Animal()
        communicator1 = module.Animal()
        communicator2 = module.Animal()
        cooperator1 = module.Animal()
        cooperator1.add_cooperation(animal)
        cooperator2 = module.Animal()
        cooperator2.add_cooperation(animal)
        fat_cards = 2

        animal.add_single_animal_property('tail_loss')
        animal.add_symbiosys(symbiont1)
        animal.add_symbiosys(symbiont2)
        animal.add_single_animal_property('piracy')
        animal.add_fat_card()
        animal.add_fat_card()

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '5']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(animal.get_hungry(), 1)
        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_single_animal_properties()), 2)
        self.assertEqual(len(animal.get_symbiosys()), 2)
        self.assertEqual(symbiont1 in animal.get_symbiosys(), True)
        self.assertEqual(animal.get_fat_cards(), 1)
        print(animal.get_animal_properties())

        animal.add_cooperation(cooperator1)
        animal.add_cooperation(cooperator2)

        def user_gen(answers):
            for answer in answers:
                yield answer

        answers = ['y', '5']
        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        module.Eating_Phase.tail_loss_property(animal, user_input)
        self.assertEqual(len(animal.get_cooperation()), 1)
        self.assertEqual(len(cooperator1.get_cooperation()), 0)

        def hand_test_tail_loss():

            animal = module.Animal()
            animal.add_single_animal_property('tail_loss')
            cooperators = []
            communications = []
            single_properties = ['high_body_weight', 'swimming', 'sharp_vision', 'burrowing', 'carnivorous', 'parasite',
                                 'hibernation_ability', 'tail_loss', 'mimicry', 'running', 'poisonous', 'grazing',
                                 'scavenger', 'camouflage', 'piracy']

            for x in range(random.randint(3, 5)):
                animal.single_properties.append(random.choice(single_properties))

            symb = randint(0, 1)
            comm = randint(0, 1)
            coop = randint(0, 1)

            if symb:
                for s in range(randint(1, 3)):
                    animal.add_symbiosys(module.Animal())

            if comm:
                for com in range(randint(1, 3)):
                    communicator = module.Animal()
                    communications.append(communicator)
                    animal.add_communication(communicator)
                    communicator.add_communication(animal)

            if coop:
                for coo in range(randint(1, 3)):
                    cooperator = module.Animal()
                    cooperators.append(cooperator)
                    animal.add_communication(cooperator)
                    cooperator.add_communication(animal)

            print('*' * 100)
            print(f'before: {animal.get_animal_properties()}')
            module.Eating_Phase.tail_loss_property(animal)
            print(f'after: {animal.get_animal_properties()}')

    def test_hunting(self):
        """
        unit test for hunting function
        """

        # =============================================
        # male players list
        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # assert there are not animals to hunt
        self.assertRaises(AssertionError, module.Eating_Phase.hunting, player_hunter.get_player_animals()[0],
                          player_hunter, player_list)

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[2].make_animal()
        player_list[2].make_animal()

        victim1 = player_hunter.get_player_animals()[1]
        victim1.add_single_animal_property('high_body_weight')
        victim2 = player_list[1].get_player_animals()[0]
        victim2.add_single_animal_property('poisonous')
        victim3 = player_list[2].get_player_animals()[0]
        victim4 = player_list[2].get_player_animals()[1]

        answers = ['1',  # choose first player to attack itself
                   '1',  # choose as victim carnivorous ]
                   '1',  # choose first player
                   '2',  # choose victim1 which is high_body_weight
                   '2',  # choose second player
                   '1']  # choose victim2

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        # if carnivorous can not attack animal - choose another - look at text on console
        # expect to see: you can not attack this animal

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(victim2.is_alive(), False)
        self.assertEqual(carnivorous.get_hungry(), 0)
        self.assertEqual(carnivorous.blue_fish_count, 2)
        self.assertEqual(carnivorous.is_poisoned(), True)

        # ========================================================================

        # add communications, symbiosys, cooperations

        # male players list
        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')
        carnivorous.increase_red_fish()

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        victim1.add_symbiosys(victim2)
        victim2.add_cooperation(victim1)
        victim1.add_cooperation(victim2)
        victim2.add_communication(victim3)
        victim3.add_communication(victim2)

        self.assertEqual(victim2 in victim1.get_symbiosys(), True)
        self.assertEqual(victim2 in victim1.get_cooperation(), True)
        self.assertEqual(victim2 in victim3.get_communication(), True)
        self.assertEqual(victim1 in victim2.get_cooperation(), True)
        self.assertEqual(victim3 in victim2.get_communication(), True)

        answers = ['2',  # choose first player to attack itself
                   '2']  # choose as victim carnivorous ]

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(victim2.is_alive(), False)
        self.assertEqual(carnivorous.get_hungry(), 0)
        self.assertEqual(carnivorous.blue_fish_count, 1)
        self.assertEqual(carnivorous.is_poisoned(), False)
        self.assertEqual(victim2 not in victim1.get_symbiosys(), True)
        self.assertEqual(victim2 not in victim1.get_cooperation(), True)
        self.assertEqual(victim2 not in victim3.get_communication(), True)
        self.assertEqual(victim1 not in victim2.get_cooperation(), True)
        self.assertEqual(victim3 not in victim2.get_communication(), True)

        # ============================================================================
        # scavenger test

        # make players list
        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')
        carnivorous.increase_red_fish()

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim3.add_single_animal_property('scavenger')

        answers = ['2',  # choose first player to attack player[1]
                   '2']  # choose as victim victim2 ]

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(victim3.blue_fish_count, 0)

        # =================================================================================
        # if player_hunter's scavenger can not take blue_fish, and player2 has two scavengers
        # and choose second

        # make players list
        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')
        carnivorous.increase_red_fish()

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        hunter_scavenger.add_single_animal_property('scavenger')
        hunter_scavenger.to_hibernate()
        victim2.add_single_animal_property('scavenger')
        victim3.add_single_animal_property('scavenger')

        answers = ['2',  # choose first player to attack player[1]
                   '1',  # choose as victim victim1
                   '2']  # choose scavenger to take blue fish victim3

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 0)
        self.assertEqual(victim2.blue_fish_count, 0)
        self.assertEqual(victim3.blue_fish_count, 1)

        # ===================================================================================
        # with mimicry and tail loss

        # 1. victim1 mimicry to victim2. carnivorous can attack victim2
        # make players list
        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim1.add_single_animal_property('mimicry')
        victim2.add_single_animal_property('mimicry')
        victim3.add_single_animal_property('mimicry')

        answers = ['2',  # choose first player to attack player[1]
                   '1',  # choose as victim victim1
                   'y',  # choose victim1 use mimicry property
                   '2',  # choose victim2 to redirect attack
                   'n']  # victim2 do not want to redirect attack to victim3 and die

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(carnivorous.blue_fish_count, 2)
        self.assertEqual(victim2.is_alive(), False)
        self.assertEqual(victim1.is_alive(), True)
        self.assertEqual(victim3.is_alive(), True)

        # 2. victim1 mimicry to victim2. carnivorous can NOT attack victim2

        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim1.add_single_animal_property('mimicry')
        victim2.add_single_animal_property('mimicry')
        victim2.add_single_animal_property('swimming')
        victim3.add_single_animal_property('mimicry')

        answers = ['2',  # choose first player to attack player[1]
                   '1',  # choose as victim victim1
                   'y',  # choose victim1 use mimicry property
                   '2']  # choose victim2 to redirect attack

        # 'n']  # victim2 do not want to redirect attack to victim3 and die

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(carnivorous.blue_fish_count, 2)
        self.assertEqual(victim2.is_alive(), True)
        self.assertEqual(victim1.is_alive(), False)
        self.assertEqual(victim3.is_alive(), True)

        # 3. victim1 is only one animal

        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim1.add_single_animal_property('mimicry')

        answers = ['2',  # choose first player to attack player[1]
                   '1']  # choose as victim victim1

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(carnivorous.blue_fish_count, 2)

        self.assertEqual(victim1.is_alive(), False)

        # 4 victim2 try to mimicry to victim1 wich already mimicried to victim2

        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim1.add_single_animal_property('mimicry')
        victim2.add_single_animal_property('mimicry')
        victim3.add_single_animal_property('mimicry')

        answers = ['2',  # choose first player to attack player[1]
                   '1',  # choose as victim victim1
                   'y',  # choose victim1 use mimicry property
                   '2',  # choose victim2 to redirect attack
                   'y',  # victim2 want to redirect attack to victim1 and die
                   '1']  # victim2 choose victim1 as redirected animal and die

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(carnivorous.blue_fish_count, 2)
        self.assertEqual(victim2.is_alive(), False)
        self.assertEqual(victim1.is_alive(), True)
        self.assertEqual(victim3.is_alive(), True)

        # 5 victim2 try to mimicry to victim3 which carnivorous can attack

        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim1.add_single_animal_property('mimicry')
        victim2.add_single_animal_property('mimicry')
        victim3.add_single_animal_property('mimicry')

        answers = ['2',  # choose first player to attack player[1]
                   '1',  # choose as victim victim1
                   'y',  # choose victim1 use mimicry property
                   '2',  # choose victim2 to redirect attack
                   'y',  # victim2 want to redirect attack to victim3
                   '3']  # victim2 choose victim3 as redirected animal

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(carnivorous.blue_fish_count, 2)
        self.assertEqual(victim2.is_alive(), True)
        self.assertEqual(victim1.is_alive(), True)
        self.assertEqual(victim3.is_alive(), False)

        # 6 victim2 try to mimicry to victim3 which carnivorous can  NOT attack

        print('GGGG'* 100)
        def user_input(*args):
            return '3'

        players = module.Players(user_input)
        player_list = players.get_player_list()

        # make player_hunter
        player_hunter = player_list[0]

        # make carnivorous
        player_hunter.make_animal()
        carnivorous = player_hunter.get_player_animals()[0]
        carnivorous.add_single_animal_property('carnivorous')

        # add animals to hunt

        player_hunter.make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()
        player_list[1].make_animal()

        hunter_scavenger = player_hunter.get_player_animals()[1]
        victim1 = player_list[1].get_player_animals()[0]
        victim2 = player_list[1].get_player_animals()[1]
        victim3 = player_list[1].get_player_animals()[2]
        victim4 = player_list[1].get_player_animals()[3]

        hunter_scavenger.add_single_animal_property('scavenger')
        victim1.add_single_animal_property('mimicry')
        victim2.add_single_animal_property('mimicry')
        victim3.add_single_animal_property('mimicry')
        victim3.add_single_animal_property('burrowing')
        victim3.increase_red_fish()

        answers = ['2',  # choose first player to attack player[1]
                   '1',  # choose as victim victim1
                   'y',  # choose victim1 use mimicry property
                   '2',  # choose victim2 to redirect attack
                   'y',  # victim2 want to redirect attack to victim3
                   '3']  # victim2 choose victim3 as redirected animal and die

        def user_gen(answers):
            for answer in answers:
                yield answer

        f = user_gen(answers)

        def user_input(*args):
            return next(f)

        self.assertEqual(module.Eating_Phase.hunting(carnivorous, player_hunter, player_list, user_input), None)
        self.assertEqual(hunter_scavenger.blue_fish_count, 1)
        self.assertEqual(carnivorous.blue_fish_count, 2)
        self.assertEqual(victim2.is_alive(), False)
        self.assertEqual(victim1.is_alive(), True)
        self.assertEqual(victim3.is_alive(), True)

if __name__ == '__main__':
    unittest.main()
