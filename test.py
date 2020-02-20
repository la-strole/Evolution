import module
import unittest


class TestEvolution(unittest.TestCase):
    def test_next_player(self):
        """ test different value for num and range for player list"""
        num_variants = [-1, 8, 'a', chr(1099), 1, 4, 0]
        number_of_players = [1, 2, 7, 8]
        for number in number_of_players:
            players_list_test = [x for x in range(number)]
            result = list(map(lambda x: module.next_player(x, players=players_list_test), num_variants))
            

