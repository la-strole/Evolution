import module
import unittest
from unittest.mock import patch
from random import randint


class TestEvolution(unittest.TestCase):

    def test_next_player(self):
        """ unit test for module.next_player(num: int, players: list)"""
        # type(num) == int
        num_test_cases_not_int = ['1', '', [1], (1,), {1: 1}]
        for test_case in num_test_cases_not_int:
            self.assertRaises(AssertionError, module.next_player, test_case, [1, 2, 3])
        # type(players) == list
        players_test_cases_not_list = ['1', '', (1,), {1: 1}]
        for test_case in players_test_cases_not_list:
            self.assertRaises(AssertionError, module.next_player, 1, test_case)
        # 1 < len(plyesrs) <= 7
        players_test_case = [-1000000000, -1, 0, 1, 8, 1000000000]
        for test_case in players_test_case:
            self.assertRaises(AssertionError, module.next_player, 1, test_case)
        # 0 <= num <= len(players)
        players_test_case = [1, 2, 3]  # relevant
        num_test_cases = [-100000000000, -1, 4, 100000000000]
        for test_case in num_test_cases:
            self.assertRaises(AssertionError, module.next_player, test_case, players_test_case)
        # num = 0
        self.assertEqual(module.next_player(0, [1, 2, 3]), 1)
        # num = len(players) - 1
        self.assertEqual(module.next_player(2, [1, 2, 3]), 0)
        # relevant test
        for i in range(10):
            players = [[1, 2], [1, 2, 3, 4], [1, 2, 3, 4, 5, 6, 7]]
            num_variants = [randint(0,1), randint(0,3), randint(0,6)]
            result = map(module.next_player, num_variants, players)
            answer_matrix = [(n+1) % len(p) for n,p in zip(num_variants, players)]
            #print(answer_matrix)
            for a, r in zip(answer_matrix, result):
                self.assertEqual(r, a)
        print('module.next_player(num: int, players: list) - OK')

    def test_take_cards(self):
        """
        unit test for module.take_cards(number: in, card_set: list) function
        """
        # type(num) == int
        num_test_cases_not_int = ['1', '', [1], (1,), {1: 1}]
        for test_case in num_test_cases_not_int:
            self.assertRaises(AssertionError, module.take_cards, test_case, [1, 2, 3])
        # type(cars set) == list
        card_test_cases_not_list = ['1', '', (1,), {1: 1}]
        for test_case in card_test_cases_not_list:
            self.assertRaises(AssertionError, module.take_cards, 1, test_case)
        # number > 0
        num_test_cases = [-100000000000, -1, 0]
        for test_case in num_test_cases:
            self.assertRaises(AssertionError, module.take_cards, test_case, [1, 2, 3])
        # number < len(cars) -> return -1
        for i in range(10):
            cards = [1*randint(1, 100)]
            num = len(cards) + randint(1, 100)
            self.assertEqual(module.take_cards(num, cards), -1)
        # relevant answer
        for i in range(10):
            cards = [x for x in range(randint(1, 100))]
            start_len_cards = len(cards)
            num = randint(1, len(cards))
            #print(f'num={num}\tlen_cards={len(cards)}')
            result = module.take_cards(num, cards)
            #print(f'new len_cards={len(cards)}')
            self.assertEqual(len(result), num)
            self.assertEqual(type(result), list)
            #print(len(cards))
            self.assertEqual(len(cards), start_len_cards - num)
        print('module.take_cards(number: int, card_set: list)- OK')

    def test_faza_razvitija(self):
        """
        unit test for faza_razvitija(players: list, number: int) function
        """

        players_list = [module.Player('first_player'), module.Player('second_player')]
        cards = [("ostr", "zhir"), ("topo", "zhir"), ("para", "hish"), ("para", "zhir"),
                 ("norn", "zhir"), (["sotr"], "hish"), (["sotr"], "zhir"), ("jado", "hish"),
                 ("komm", "zhir"), ("spac", "hish"), ("mimi",), (["simb"],),
                 ("pada",), ("pira",), ("otbr",), ("bist",), ("vodo",), ("vodo",),
                 (["vzai"], "hish"), ("bols", "zhir"), ("bols", "hish")]
        hands = [("ostr", "zhir"), ("ostr", "zhir")]
        for player in players_list:
            player.get_cards_hand().extend(hands)
        first_number = 0
        razvitie = module.Faza_Razvitija(players_list, first_number)
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
        """
        #if active player don't have animals
        razvitie.test = True
        razvitie.faza_rezvitija_function()
    # todo looks like test fail - after adding animal - first player is still active player


if __name__ == '__main__':
    unittest.main()
