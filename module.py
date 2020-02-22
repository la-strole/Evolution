"""
Created on 15 10 2017

@author: zhenya.aka.john@gmail.com
"""
from random import shuffle, randint


class Player:
    """ Player container of animals. """

    def __init__(self):
        # self.first_hand = []
        # i.first_hand = take_cards(6)
        self.cards_hand = []
        self.animals = []  # list of animls = amimal()
        self.grazing_count = 0  # count of 'topo' on hand
        self.player_id = 0
        self.name = "default_name"


class Animal:
    def __init__(self):
        self.animal_id = animal_id
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


def next_player(num, players):
    """Select next Player. players - players list return next num or -1 if failure"""
    try:
        if len(players) > 1:
            if 0 <= num <= len(players) - 1 <= 7:
                if len(players) > num + 1:
                    next_num = num + 1
                else:
                    next_num = 0
                return next_num
            print("something wrong with num value")
            return -1
        else:
            print("number of player are less or equal than 1")
            return -1
    except TypeError:
        print("something wrong with type")
        return -1


def take_cards(number: int, card_set: list):
    """Take <number> of cards from <card_set> and return it and remove from <card_set>."""
    try:
        if number <= 0:
            print('number is less than zero or zero')
            return -1
        else:
            if number <= len(card_set):
                try:
                    return [card_set.pop() for i in range(number)]
                except IndexError:
                    print("end of cards!")
                    return -1
            else:
                print('error with number in take_cards function')
                return -1
    except (TypeError, AttributeError):
        print("type error in card_set")
        return -1


def take_handcard(player):
    """Take one card from <Player>'s hand and return it (Player - active_player).  """
    if isinstance(player, Player):
        if isinstance(player.cards_hand, list):
            if player.cards_hand:
                while 1:
                    # Return number of card from Player's hand.
                    try:
                        print("your hand is:", player.cards_hand)
                        card_num = int(input("choose card's number")) - 1
                        if 0 <= card_num < len(player.cards_hand):
                            card = player.cards_hand.pop(card_num)
                            break
                        else:
                            print("try again")
                    except:
                        print("error, try again")
                        continue
                return card
            else:
                print("this Player hasn't any cards!")
                return -1
        else:
            print("player handcards is not a list")
            return -1
    else:
        print("player is not instnce of Player class")
        return -1

def make_animal(player):
    print("Adding new Animal to you")
    new_animal = Animal()
    player.animals.append(new_animal)
    for i in range(len(player.animals)):
        print('Animal', i + 1, ':', player.animals[i].property)
        # for i in Player.animals:
    return 1

# TODO make returncard_to_coloda function to return card
def make_parasite(players):
    """ set parasite property t another player's animal players - players list"""
    for count, item in enumerate(players):
        print(f"player {count} {item.name}")
        for number, animal in enumerate(item.animals):
            print(f"animal {number} {animal.property}")
    player_num = input("choose player number")
    if 'para' in all(players[player_num].animals.property):
        print(f" all {players[player_num].name} animals has parasites - choose another player")
    else:
        for number, animal in enumerate(item.animals):
            print(f"animal {number} {animal.property}")
        animal_num = input("choose animal number")
        if players[player_num].animals[animal_num].parasite == 0:
            players[player_num].animals[animal_num].property.append("para")
            players[player_num].animals[animal_num].parasite += 1
            players[player_num].animals[animal_num].hungry += 2
            print(players[player_num].animals[animal_num].property)
def make_parasite(players_list, active_num, **kwargs):
    """Set parasite to another Player.  """
    for i in range(len(players_list)):
        print (i + 1, " ", players_list[i].name, '\n', "animals:\n")
        for item in range(len(players_list[i].animals)):
            print("Animal", item + 1, players_list[i].animals[item].property)
    print("=" * 40, "\n")
    print("this property you can set only to another Player's Animal")
    while 1:  # Main loop.
        try:
            want_next_loop = 0
            if 'Player' in kwargs.keys():
                player = kwargs['Player']
            else:
                player = int(input("input number of Player")) - 1
            if player == active_num:
                print("you can't set 'parasite' property to your own animals!\
                        try again!")
                continue  # Main loop.
            elif player < 0 or player >= len(players_list):
                print("wrong number, plese try again!")
                continue  # Main loop.
            else:
                while 1:  # Choose Animal loop.
                    if 'Animal' in kwargs.keys():
                        animal = kwargs['Animal']
                    else:
                        animal = int(input("input number of Animal")) - 1
                    if 0 <= animal < len(players_list[player].animals):
                        if players_list[player].animals[animal].parasite == 0:
                            players_list[player].animals[animal].property.append("para")
                            players_list[player].animals[animal].parasite += 1
                            players_list[player].animals[animal].hungry += 2
                            print(players_list[player].animals[animal].property)
                            break  # Choose Animal loop.
                        else:
                            print("error - each Animal has only one parasite")
                            while 1:  # Little loop.

                                if 'ret_card' in kwargs.keys():
                                    ret_card = kwargs['ret_card']
                                else:
                                    ret_card = input("do you want to return your card\
                                                      to your hand? y/n")
                                if ret_card == 'y' or ret_card == 'Y':
                                    return 0
                                elif ret_card == 'n' or 'N':
                                    want_next_loop = 1
                                    break  # Little loop.
                                else:
                                    print ("please, say 'y' or 'n'")
                                    continue  # Little loop.
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


def make_property(player, card, players_list, active_num, **kwargs):
    # Player = Player() or players_list[i]
    """ Defines the property for Player's Animal players_list and active_num -
        for function make_parasite.
          
    """

    def print_player_animals(player):
        number = 1
        for animal in player.animals:
            print(number, ' ', animal.property)
            number += 1
        return 1

    if 'test' in kwargs.keys():
        testoption = 1  # Everywhere with input in this funcion to set values
        #    in unittest.
    else:
        testoption = 0
    # if properties are more than one return property_value
    if len(card) > 1:
        while 1:
            # Test1.  
            try:
                print("your card has more than one property ", card)
                if testoption:
                    choise = kwargs['card_property_count']
                else:
                    choise = int(input("choose property (1/2)"))
                if choise == 1:
                    property_value = card[:][0]
                    break
                elif choise == 2:
                    property_value = card[:][1]
                    break
                else:
                    print("incorrect input - try again!")
            except(ValueError):
                print("exeption! try again")
        print("your property", property_value)

    else:
        property_value = card[:][0]  # If only one propery on the card.
        print("your property", property_value)

    lenght_player_animals = len(player.animals)

    if property_value not in [['vzai'], ['simb'], ['sotr'], "para", "zhir"]:
        # Property is single and not parasite, zhir.  
        while 1:  # Test for single properties.
            print_player_animals(player)
            if testoption:
                choise = kwargs['animal_number'] - 1
            else:
                choise = int(input("choose animals's number to add property: ")) - 1

            if choise > lenght_player_animals - 1 or choise < 0:
                print("error with choise number - please, try again!")
                continue  # Test for single properrties.

            current_animal = player.animals[choise]
            if property_value in current_animal.property:
                # Not dubles.
                print("This Animal already has this property! choose another Animal!")
                if testoption:
                    ret_card = kwargs['ret_card']
                else:
                    ret_card = input("do you want to return your card \
                                     to your hand? y/n")
                if ret_card == 'y' or ret_card == 'Y':
                    player.cards_hand.append(card)
                    return 0
                else:
                    continue  # Test for single properies loop.
            elif (property_value == "pada") and ("hish" in current_animal.property):
                print("Hish can't have padal'shik property")
                ret_card = input("do you want to return youra card to your hand? y/n")
                if testoption:
                    ret_card = kwargs['ret_card']
                if ret_card == 'y' or ret_card == 'Y':
                    player.cards_hand.append(card)
                    return 0
                else:
                    continue  # Test for single properies loop.
            elif (property_value == "hish") and ("pada" in current_animal.property):
                print("your Animal has padalshik property it can't be hish!")
                ret_card = input("do you want to return youra card to your hand? y/n")
                if testoption:
                    ret_card = kwargs['ret_card']
                if ret_card == 'y' or ret_card == 'Y':
                    player.cards_hand.append(card)
                    return 0
                else:
                    continue  # Test for single properies loop.
            else:
                current_animal.property.append(property_value)

                if property_value == "vodo":
                    current_animal.swimmimg = True
                elif property_value == "bist":
                    current_animal.running = True
                elif property_value == "mimi":
                    player.animals[choise].mimicry = True
                elif property_value == "pada":
                    player.animals[choise].scavenger = True
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
                break  # Test for single properies loop.
        return 1
    elif property_value == "para":
        if testoption:
            if (make_parasite(players_list, active_num, player=kwargs['para_player'],
                              animal=kwargs['para_animal'])):
                return 1
            else:
                player.cards_hand.append(card)
                return 0
        else:
            if (make_parasite(players_list, active_num)):
                return 1
            else:
                player.cards_hand.append(card)
                return 0
    elif property_value == "zhir":
        while 1:  # Zhir loop.
            print_player_animals(player)
            if testoption:
                choise = kwargs['animal_number'] - 1
            else:
                choise = int(input("choose animals's number to add property: ")) - 1

            if choise > lenght_player_animals - 1 or choise < 0:
                print("error with choise number - plaese try again!")
                continue  # Zhir loop.

            current_animal = player.animals[choise]
            current_animal.fat_cards_count += 1
            current_animal.property.apppend("zhir")
            break  # Zhir loop.
        return 1
    else:  # If property is double.
        property_value = property_value.copy()
        if lenght_player_animals < 2:
            print ("Error - you can't apply this property because you have\
                    only one Animal")
            player.cards_hand.append(card)
            return 0
        elif property_value == ["sotr"]:
            for i in range(lenght_player_animals):
                print ("Animal ", i + 1, player.animals[i].property)
            print("choose pair of animals (example: 1,3)")
            while 1:  # Choose sotr pair.
                try:
                    choise = []
                    if testoption:
                        item = kwargs['pair_of_animals_sotr']
                    else:
                        item = (input("pair of your animals (1,3):")).split(",")
                    for f in item[:]:
                        choise.append(int(f))
                    if len(choise) != 2:
                        print("you have to input a PAIR of numbers-animals\
                              (example: 1,2)")
                        continue  # Choose sotr loop.
                    elif ((0 < choise[0] <= lenght_player_animals) and
                          (0 < choise[1] <= lenght_player_animals) and
                          (choise[0] != choise[1])):
                        property_value.append(choise[:][0])
                        property_value.append(choise[:][1])
                        print("property_value=", property_value)  # For test.
                        property_value_reverse = []
                        property_value_reverse.append(property_value[:][0])
                        property_value_reverse.append(property_value[:][2])
                        property_value_reverse.append(property_value[:][1])
                        if ((property_value in player.animals[choise[0] - 1].property) or
                                (property_value in player.animals[choise[1] - 1].property)):
                            print("This animals had been already sotrudniki!\
                                  try another card!")
                            player.cards_hand.append(card)
                            return 0
                        elif (property_value_reverse in player.animals[choise[0] - 1].property or
                              property_value_reverse in player.animals[choise[1] - 1].property):
                            print("This animals had been already sotrudniki reverse!\
                                  try another card!")
                            player.cards_hand.append(card)
                            return 0
                        else:
                            player.animals[choise[0] - 1].property.append(property_value)
                            player.animals[choise[1] - 1].property.append(property_value)
                            print ('Animal', choise[0], ' ', player.animals[choise[0] - 1].property)
                            print ('Animal', choise[1], ' ', player.animals[choise[1] - 1].property)
                            break  # Choose sotr pair loop.

                except:
                    print("exception choose pair animals! try again!")
                    continue  # Choose sotr pair loop.
            return 1
        elif property_value == ["simb"]:
            for i in range(lenght_player_animals):
                print ("Animal ", i + 1, player.animals[i].property)
            print("choose pair of animals simiont/ne simbiont (example: 1,3)")
            while 1:  # Choose simb pair loop.
                try:
                    choise = []
                    if testoption:
                        item = kwargs['pair_of_animals_simb']
                    else:
                        item = (input("pair of your animals simbiont/\
                                      ne simbiont (1,3):")).split(",")
                    for f in item[:]:
                        choise.append(int(f))
                    if len(choise) != 2:
                        print("you have to input a PAIR of numbers-animals\
                              (example: 1,2)")
                        continue  # Choose simb pair loop.
                    elif ((0 < choise[0] <= lenght_player_animals) and
                          (0 < choise[1] <= lenght_player_animals) and
                          (choise[0] != choise[1])):
                        property_value.append(choise[:][0])
                        property_value.append(choise[:][1])
                        property_value_reverse = []
                        property_value_reverse.append(property_value[:][0])
                        property_value_reverse.append(property_value[:][2])
                        property_value_reverse.append(property_value[:][1])
                        if ((property_value in player.animals[choise[0] - 1].property) or
                                (property_value in player.animals[choise[1] - 1].property)):
                            print("This animals had been already simbionti!\
                                  try another card!")
                            player.cards_hand.append(card)
                            return 0
                        elif ((property_value_reverse in player.animals[choise[0] - 1].property or
                               property_value_reverse in player.animals[choise[1] - 1].property)):
                            print("This animals had been already simbionti reverse!\
                                  try another card!")
                            player.cards_hand.append(card)
                            return 0
                        else:
                            player.animals[choise[0] - 1].property.append(property_value)
                            player.animals[choise[1] - 1].property.append(property_value)
                            print ('Animal', choise[0], ' ', player.animals[choise[0] - 1].property)
                            print ('Animal', choise[1], ' ', player.animals[choise[1] - 1].property)
                            break  # Choose simb pair loop.
                except:
                    print("exception choosing simbiont/ ne simbiont! try again!")
                    continue  # Choose simb pair loop.
            return 1
        elif property_value == ["vzai"]:
            for i in range(lenght_player_animals):
                print ("Animal ", i + 1, player.animals[i].property)
            print("choose pair of animals vzaimodejstvie (example: 1,3)")
            while 1:  # Choose vzai pair loop.
                try:
                    choise = []
                    if testoption:
                        item = kwargs['pair_of_animals_vzai']
                    else:
                        item = (input("pair of your animals (1,3):")).split(",")
                    for f in item[:]:
                        choise.append(int(f))
                    if len(choise) != 2:
                        print("you have to input a PAIR of numbers-animals (example: 1,2)")
                        continue  # Choose vzai pair loop.
                    elif ((0 < choise[0] <= lenght_player_animals) and
                          (0 < choise[1] <= lenght_player_animals) and
                          (choise[0] != choise[1])):
                        property_value.append(choise[:][0])
                        property_value.append(choise[:][1])
                        property_value_reverse = []
                        property_value_reverse.append(property_value[:][0])
                        property_value_reverse.append(property_value[:][2])
                        property_value_reverse.append(property_value[:][1])
                        if ((property_value in player.animals[choise[0] - 1].property) or
                                (property_value in player.animals[choise[1] - 1].property)):
                            print("This animals had been already vzaimod!\
                                  try another card!")
                            player.cards_hand.append(card)
                            return 0
                        elif (property_value_reverse in player.animals[choise[0] - 1].property or
                              property_value_reverse in player.animals[choise[1] - 1].property):
                            print("This animals had been already vzaimod! reverse!\
                                  try another card!")
                            player.cards_hand.append(card)
                            return 0
                        else:
                            player.animals[choise[0] - 1].property.append(property_value)
                            player.animals[choise[1] - 1].property.append(property_value)
                            print ('Animal', choise[0], ' ', player.animals[choise[0] - 1].property)
                            print ('Animal', choise[1], ' ', player.animals[choise[1] - 1].property)
                            break  # Choose vzai pair loop.
                except:
                    print("exception choosing animals for vzai! try again!")
                    continue  # Choose vzai pair loop.
            return 1


def make_players_list():
    """Make players list = [] by default min 2 max 8. Return players_list.  """
    players = []
    while True:
        try:
            number_of_players = int(input("input number of players (2...8)"))
            if (number_of_players >= 8) or (number_of_players < 2):
                print ("bad number, try again")
            else:
                break
        except ValueError:
            print("value error! bad number of players, try again")
        except NameError:
            print("name error! bad number of players, try again")
    for i in range(number_of_players):
        players.append(Player())  # List of instances of Player class.
        while True:
            try:
                players[i].name = str(input("input Player's name: "))
                players[i].player_id = i
                break
            except ValueError:
                print("try to input another name")
    return players


def make_koloda(number_of_players):
    """ Return set_cards - cards - set of cards,
       number_of_players = len(plyers_list) -  above.  
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
        raise(ValueError)
    shuffle(set_cards)
    return set_cards


def make_first_hand(players: list, card_set: list):
    """take 6 random cards from card_set to each Player"""

    for player in players:
        player.cards_hand = take_cards(6, card_set)
    return 1


def faza_razvitija(players, number):
    list_of_pass = []
    active_player = players[number]
    global animal_id
    while 1:
        # Main loop.          
        if len(list_of_pass) == len(players):
            print("All players said PASS")
            break  # Exit from main loop.

        elif number in list_of_pass:  # If active Player say PASS.
            number = next_player(number, players)
            active_player = players[number]
            continue  # Contunie main loop with next actie Player.
        else:  # If active Player don't say PASS.
            if not active_player.cards_hand:
                # If Player hasn't cards in his hand - automatic PASS.
                list_of_pass.append(number)
                number = next_player(number, players)
                active_player = players[number]
                continue  # Contunie main loop with next actie Player.

            print("active Player ", active_player.name, "=" * 20, "\n")
            print("Player's hand: ", active_player.cards_hand)
            if active_player.animals:

                for i in active_player.animals:
                    print('Animal:', i.property)
            else:
                print ("you haven't animals yet")
            while 1:  # Loop for unsuitable properties -
                #  to posibility of returning card to koloda.
                # animal_id = 0
                if active_player.animals:
                    while 1:  # loop of choose PASS/ no PASS
                        try:
                            pass_faza = input("do you want to say Pass (y/n)")
                            if pass_faza == 'Y' or pass_faza == 'y':
                                list_of_pass.append(number)
                                break  # Exit from loop of choose PASS/ no PASS.
                            elif pass_faza == 'N' or pass_faza == 'n':
                                break  # Exit from loop of choose PASS/ no PASS.  
                            else:
                                print("try again!")
                        except:
                            print('exception yes/no pass fraza! try again!')
                    if number in list_of_pass:
                        break  # Exit from loop 'suitable'.
                    while 1:  # Loop of choose Animal/property.
                        flag_suit = 0
                        try:
                            choise = input("do you want to make new Animal or\
                                           new property? (a/p)")
                            if choise == 'A' or choise == 'a':
                                take_handcard(active_player)
                                make_animal(active_player)
                                animal_id += 1
                                flag_suit = 1
                                break  # Exit from loop of choose Animal/property.
                            elif choise == 'P' or choise == 'p':
                                # If you can set property to the Animal:
                                flag_suit = make_property(active_player,
                                                          take_handcard(active_player),
                                                          players, number)
                                break  # Exit from loop of choose Animal/property.
                            else:
                                print("try again!")
                        except:
                            print('try again!')
                    if flag_suit == 1:
                        break  # Exit from loop 'suitable'.
                    else:
                        continue  # Loop 'suitable'  return unsuitable card to
                        #  hand in function make_property.

                else:  # If you don't have any animals.
                    print("now you have to make your first Animal from your hand")
                    take_handcard(active_player)
                    make_animal(active_player)
                    animal_id += 1
                    break  # Exit from loop 'suitable'.
            number = next_player(number, players)
            active_player = players[number]
            continue  # Loop 'mainloop'.

    for i in range(len(players)):
        print (players[i].name, '\n', "animals:\n")
        for item in range(len(players[i].animals)):
            print("Animal", item + 1, players[i].animals[item].property,
                  "hungry=", players[i].animals[item].hungry)
        print("=" * 20, "\n")
    print("end of faza razvitije")
    return 1


animal_id = 0  # Global - for different  Animal id in Animal class -
# increments 2 times in global in faza razvitija function.
if __name__ == "__main__":
    players_list = make_players_list()
    # players_list - list of instances of class "Player"
    koloda = make_koloda(len(players_list))
    make_first_hand(players_list, koloda)
    active_num = randint(0, len(players_list) - 1)
    first_num = active_num  # For faza pitanije.
    faza_razvitija(players_list, active_num)

    """    
    #=========================================================================
    #                      FAZA OPREDELENIJA KORMOVOJ BAZY
    
    length_player_list=len(players_list)
    if length_player_list == 2:
        red_fish = randint(1,6) + 2
    elif length_player_list == 3:
        red_fish = randint(1,6) + randint(1,6)
    elif length_player_list == 4:
        red_fish = randint(1,6) + randint(1,6) + 2
    elif length_player_list == 5:
        red_fish = randint(1,6) + randint(1,6) + randint(1,6) + 2
    elif length_player_list == 6:
        red_fish = randint(1,6) + randint(1,6) + randint(1,6) + 4
        red_fish = randint(1,6) + randint(1,6) + randint(1,6) + 2
    elif length_player_list == 7:
        red_fish = randint(1,6) + randint(1,6) + randint(1,6) + randint(1,6) + 
                   randint(1,4) + 2       
    elif length_player_list == 8:
        red_fish = randint(1,6) + randint(1,6) + randint(1,6) + randint(1,6) + 
                   randint(1,4) + 4         
    else:
        print ("you have too mach players")
        raise ('ValueError')
    
    
    print ("="*10,"faza opr kprm bazy","="*10)
    print ("FOOD=",red_fish,"\n"*2)
    
    
    #==========================================================================
                                        # FAZA PITANIJA
    active_num = first_num                                    
    active_player = players_list[first_num]        
    while 1: # main loop of faza pitanija
        if red_fish > 0: # if red_fish exists in korm baza
            flag_hungry = 0
            flag_zhir = 0
            flag_topotun = 0
            for Animal in active_player.animals: # if one of animals is hungry
                if ['topo'] in  Animal.property:
                    flag_topotun += 1
                if Animal.hungry > 0:
                    flag_hungry += 1
                if ["zhir"] in Animal.property and Animal.fat_cards_count > Animal.fat:
                    flag_zhir += 1
            if (flag_hungry == 0 and flag_zhir == 0) and red_fish > 0: 
            # all animals aren't hungry and zhir
                if flag_topotun > 0:
                    while 1: # loop of choose topotun
                        try:
                            topotun_choise= input("do you want to use 'topotun'? y/n") 
                            if topotun_choise == 'Y' or topotun_choise == 'y':
                                if flag_topotun > 1:
                                    topotun_num = input("how many red_fish do you want to delete? \
                                                         max = ",flag_topotun)
                                    if 0 < topotun_num <= flag_topotun:
                                        if red_fish-topotun_num >=0:
                                            red_fish -= topotun_num
                                        else:
                                            red_fish = 0   
                                    else: 
                                        print("something wrong with input number of red_fish!")
                                        continue # continue choose topotun         
                                else: 
                                    topotun_num = 1        
                                    red_fish -= topotun_num
                                break # exit from loop of choose topotun
                            elif pass_faza == 'N' or pass_faza == 'n':
                                break  #exit from loop topotun
                            else: 
                                print("try again!")    
                        except:
                            print('exception yes/no tpotun_choose! try again!')     
          
            else:
                print("some of your animals are hungry or zhir")
                break # break loop faza pitanije for test
    
        else:
            print("you don't have any red_fishes in your korm baza")
            break # break loop faza pitanije for test
    
        break # break loop faza pitanije for test
    
    
    
    
    
    
    
    
    #--------------------------------------------------------------------------------------------
    """