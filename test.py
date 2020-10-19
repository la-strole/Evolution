import module
import unittest
from random import randint


class TestEvolution(unittest.TestCase):

    def test_next_player(self):
        """ test different value for num and range for player list"""
        num_variants = [-1, 8, 'a', chr(1099), 1, 4, 0]
        number_of_players = [1, 2, 7, 8]
        answer_matrix = [[-1, -1, -1, -1, -1, -1, -1], [-1, -1, -1, -1, 0, -1, 1], [-1, -1, -1, -1, 2, 5, 1],
                         [-1, -1, -1, -1, 2, 5, 1]]
        result = []
        for number in number_of_players:
            players_list_test = [x for x in range(number)]
            result.append(list(map(lambda x: module.next_player(x, players=players_list_test), num_variants)))
        self.assertEqual(result, answer_matrix)

    def test_take_cards(self):
        """ test error Indexerror"""
        for i in range(30):
            card_set = [x for x in range(randint(0, 40))]
            old_card_set = card_set[:]
            number = randint(0, 100)
            if number < 20:
                number = 0 - number
            if number < 0:
                self.assertEqual(module.take_cards(number, card_set), -1)
                self.assertEqual(len(card_set), len(old_card_set))
            elif number > len(card_set):
                self.assertEqual(module.take_cards(number, card_set), -1)
                self.assertEqual(len(card_set), len(old_card_set))
            else:
                self.assertEqual(type(module.take_cards(number, card_set)), list)
                self.assertEqual(len(card_set), len(old_card_set) - number)
        card_set = 'string'
        old_card_set = card_set
        self.assertEqual(module.take_cards(number, card_set), -1)
        self.assertEqual(len(card_set), len(old_card_set))
        card_set = []
        old_card_set = card_set[:]
        self.assertEqual(module.take_cards(number, card_set), -1)
        self.assertEqual(len(card_set), len(old_card_set))


if __name__ == '__main__':
    unittest.main()
