a'''
Created on Sep 9, 2018

@author: xxx
'''
import unittest
import module
from random import randint 



#from module import player

class Test(unittest.TestCase):
    
    def test_takecards(self):
        koloda = module.makecoloda(4)
        for i in range (15):
            lenght = len(koloda)
            number = randint(0,len(koloda)//2)
            #number = -2
            if len(koloda)> number:
                iset = module.take_cards(number, koloda)
                self.assertEqual(len(iset), number)
                self.assertEqual(len(iset)+len(koloda), lenght)
            else:
                iset = module.take_cards(number, koloda)
                self.assertRaises(IndexError)

    def test_take_handcard(self):
        test_player = module.player()
        test_player.cards_hand=['one','two','three','four','five','six']
        first_len = len(test_player.cards_hand)
        for i in range(first_len):
            #print ('i=',i)
            num = randint(1,len(test_player.cards_hand))
            #print('num=',num)
            card = test_player.cards_hand[num-1]
            self.assertEqual(module.take_handcard(test_player,test=1, cardnum = num), card)
            self.assertEqual(len(test_player.cards_hand), first_len-i-1)
        #self.assertEqual(take_handcard(test_player,test=1,cardnum = 1), '')
        self.assertRaises(IndexError)
        #test_player.cards_hand=['one','two','three','four','five','six']
        #num = 10
        #take_handcard(test_player,test=1, cardnum = num)
        

    def test_makeanimal(self):
        testplayer = module.player()
        self.assertEqual(testplayer.animals, [])
        module.make_animal(testplayer)
        self.assertEqual(len(testplayer.animals), 1)
        self.assertEqual(module.make_animal(testplayer),1)
        
    
    def test_make_parasite(self):
        for repeat in range (100):
            players_list = []
            karti = ["ostr", "zhir", "topo","zhir","hish", "zhir", "norn","zhir", 
             ["sotr"],"hish", ["sotr"], "zhir", "jado","hish", "komm","zhir", "spac","hish",
             "mimi",["simb"],"pada","pira","otbr","bist","vodo","vodo","vzai",'bolsh']
            
            number_of_players = randint(2,8)
            for i in range(number_of_players):
                players_list.append(module.player())
                players_list[i].name = str(i)
                for n in range(randint(1,4)):
                    (players_list[i].animals.append(module.animal()))
                    for p in range(randint(1,4)):
                        players_list[i].animals[n].property.append(karti[randint(0,len(karti)-1)])
                                                                                     
            active_num = randint(0,len(players_list)-1)
            while 1:
                player = randint(0,len(players_list)-1)
                if player == active_num:
                    print("loop unstopable because you can't send parasite to yourself")
                    continue
                else:
                    
                    animal = randint(0,len(players_list[player].animals)-1)
                    first_hungry = players_list[player].animals[animal].hungry
                    first_len_property = len(players_list[player].animals[animal].property)
                    
                    #player = active_num
                    #player = -2
                    #player = len(players_list)+1
                    #animal = -1
                    #animal = len(players_list[player].animals)+1
                    #animal = 'a'
                    self.assertEqual(module.make_parasite(players_list, active_num, player = player,animal = animal),1)
                    self.assertEqual('para' in players_list[player].animals[animal].property, True)
                    self.assertEqual(players_list[player].animals[animal].hungry, first_hungry+2)
                    self.assertEqual(players_list[player].animals[animal].parasite,1)
                    self.assertEqual(len(players_list[player].animals[animal].property),first_len_property+1)
                    self.assertEqual(module.make_parasite(players_list, active_num, player = player,animal = animal,ret_card = 'y'),0)
                    #module.make_parasite(players_list, active_num, player = player,animal = animal,ret_card = 'n')
                    
                    break

    def test_make_property(self):
        players_list = []
        karti = [("ostr", "zhir"), ("topo","zhir"), ("para","hish"), ("para","zhir"), ("norn","zhir"), 
         (["sotr"],"hish"), (["sotr"], "zhir"), ("jado","hish"), ("komm","zhir"), ("spac","hish"),
         ("mimi",),(["simb"],),("pada",),("pira",),("otbr",),("bist",),("vodo",),("vodo",),(["vzai"],"hish"),
         ("bols","zhir"),("bols","hish")]
        number_of_players = randint(2,8)
        for i in range(number_of_players):
            players_list.append(module.player())
            players_list[i].name = str(i)
            for n in range(randint(1,4)):
                (players_list[i].animals.append(module.animal()))
                                                                                  
        active_num = randint(0,len(players_list)-1)
        # test1
        player = players_list[active_num]
        #card = karti[randint(0,len(karti)-1)]
        card = (["one"],"two")
        card_property_count = 1
        animal_number = randint(1,len(player.animals))
        #animal_number = len(player.animals)+1
        self.assertEqual(module.make_property(player, card, players_list, active_num,
                                              test=1, card_property_count=card_property_count,
                                              animal_number=animal_number), 1)
        self.assertEqual(["one"] in player.animals[animal_number-1].property, True)
        self.assertEqual(module.make_property(player, card, players_list, active_num,
                                              test=1, card_property_count=card_property_count,
                                              animal_number=animal_number, ret_card = 'y'), 0)
        self.assertEqual(len(player.cards_hand) == 1 and 
                         card in player.cards_hand, True)
        
        # property_value == card[:][0]
        #card_property_count = 2
        # property_value == card[:][1]
        #card_property_count = 3
        #card_property_count = -2
        #card_property_count = 'a'
        #card_property_count = 2.5
        #card = (["one",])
        ## property_value == card[:][0]
    
            
#if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testmakeanimal']
 #   unittest.module()
    
