"""
Original author - /u/mpaw975
Edited by    - /u/Azgurath
"""
from builtins import range

"""
Ver si hacer Mulligan Automatico
"""

"""
Tron Simulator
Relevant Cards
4 Mine
4 PP
4 Tower
4 Sphere (labeled star)
4 Star
4 Map
4 Prophetic Prism
4 Stirring
4 Mulldrifter
24 Other cards
"""

import random

## Initialize some variables that count useful things
count_turn_3_mull = 0
turn_3_tron = 0
map_opening = 0
star_opening = 0
other_opening = 0
no_land_opening = 0
hard_opening = 0 # Here you have one Tron piece, one star and one map (for now you play the star)
hard_success_3_tron = 0 # How many times the hard opening worked out to find Tron?
hard_success_3_mull = 0 # How many times the hard opening worked out to find Tron and play Mull?

## Change this to False if you want to always be on the play
on_the_draw = False

## Hand Size
starting_size = 4

## Number of simulations
## N = 100000 should take a couple of seconds, N = million ~30 seconds.
N = 100000

def missing_piece(card,hand,battlefield):
    missing = False 
    for land in ["Mine", "PP", "Tower"]:
        if card == land and card not in hand and card not in battlefield:
            missing = True                
    return missing

def tron_pieces(hand,battlefield):
    # How many new tron pieces in total?
    tron_pieces = 0
    if "Mine" in hand or "Mine" in battlefield:
        tron_pieces += 1
    if "PP" in hand or "PP" in battlefield:
        tron_pieces += 1
    if "Tower" in hand or "Tower" in battlefield:
        tron_pieces += 1                
    return tron_pieces

def new_tron_pieces_in_hand(hand,battlefield):
    # How many new tron pieces in hand?
    new_tron_in_hand = 0
    if "Mine" in hand and "Mine" not in battlefield:
        new_tron_in_hand += 1
    if "PP" in hand and "PP" not in battlefield:
        new_tron_in_hand += 1
    if "Tower" in hand and "Tower" not in battlefield:
        new_tron_in_hand += 1                
    return new_tron_in_hand

def game(draw):
    # Populate the deck
    deck = ["Mine", "Mine", "Mine", "Mine",
            "PP", "PP", "PP", "PP",
            "Tower", "Tower", "Tower", "Tower",
            "star", "star", "star", "star",
            "star", "star", "star", "star",
            "map", "map", "map", "map",
            "prism", "prism", "prism", "prism",
            "stirrings", "stirrings", "stirrings", "stirrings",
            "mull", "mull", "mull", "mull"]
    
    for x in range(60 - len(deck)):
        deck.append("dead")
    
    # Keep track of stats
    # 0 = Map openings, 1 = Star openings, 2 = Other opening, 3 = Hard Opening, 4 = No Land Opening, 5 = T3 Tron, 6 = T3 Mulldrifter
    opening = [0,0,0,0,0,0,0]
       
    # Populate the battlefield
    battlefield = []
    
    # Populate the starting hand    
    hand = random.sample(deck,starting_size)
    
    #Take the cards out of the deck
    for card in hand:
        deck.remove(card)

    hand_amounts = [0,0,0,0,0,0,0,0]
    hand_amounts[0] = hand.count("Mine")
    hand_amounts[1] = hand.count("PP")
    hand_amounts[2] = hand.count("Tower")
    hand_amounts[3] = hand.count("star")
    hand_amounts[4] = hand.count("map")
    hand_amounts[5] = hand.count("prism")
    hand_amounts[6] = hand.count("stirrings")
    hand_amounts[7] = hand.count("mull")
    
    ### HERE GOES MULLIGAN ###
    
    # Global
    ########
    
    prisms_in_battlefield = 0
    
    # Turn 1
    ########

    #Scry
    scry = starting_size < 7
    scry_bottom = True
    new_card = random.choice(deck)
    if scry:
        # How many new tron pieces in hand?
        new_tron_in_hand = new_tron_pieces_in_hand(hand, battlefield)       
        
        # If we have natural tron, keep Mulldrifter, star, or prism on top. (if needed)
        if new_tron_in_hand == 3 or (new_tron_in_hand == 2 and "map" in hand):
            if new_card is "mull" and "mull" not in hand:
                scry_bottom = False
            elif new_card is "star" and "mull" in hand:
                # Here we could argue to leave star anyway to crack for mana for Stirrings or Mulldrifter, but I don't know, we'll see
                # Keeping the star always seems to affect little or nothing (need more sampling)
                scry_bottom = False            
            elif new_card is "prism" and "mull" in hand:
                # There are a few other situations where leaving prism on top wouldn't be the worst, but we are just playing at getting Turn 3 Mulldrifter
                # If keeping the star wasn't good there is no point in checking the prism                            
                scry_bottom = False
        elif new_tron_in_hand == 2 and "map" not in hand:
            if missing_piece(new_card, hand, battlefield):
                scry_bottom = False
            elif new_card is "map":
                scry_bottom = False
            elif new_card is "stirrings" and (("stirrings" not in hand) or (hand.count("stirrings") == 1 and "star" in hand)):
                scry_bottom = False
            elif new_card is "star" and  (("stirrings" in hand and "star" not in hand) or (hand.count("stirrings") > 1 and hand.count("star") == 1)):
                scry_bottom = False
            # It's actually better to always put the prism in the bottom (by a tiny, tiny hair (~0.05) (maybe it's just variance))
            # elif new_card is "prism" and "stirrings" in hand and "star" not in hand and "prism" not in hand:
                #scry_bottom = False
        elif new_tron_in_hand == 1:
            if missing_piece(new_card, hand, battlefield):
                scry_bottom = False
            elif new_card is "stirrings" and "stirrings" not in hand and "star" in hand:
                scry_bottom = False
            elif new_card is "star" and "star" not in hand and "stirrings" in hand:
                scry_bottom = False
        else:
            if missing_piece(new_card, hand, battlefield):
                scry_bottom = False
                            
    if scry_bottom:
        # If we scry to the bottom, remove the card from the deck.
        # This isn't totally accurate, but only matters if we crack a map.
        # Unlikely to have any significant impact.

        # A possible solution would be having a seperate list of cards_on_bottom
        # that holds cards known to be on the bottom from scrying or ancient
        # stirrings. Those cards would be removed the list of cards in the deck.
        # When a map is cracked, every card in the cards_on_bottom list would be
        # re-appened to the deck list and therefore able to be drawn.
        deck.remove(new_card)
        new_card = random.choice(deck)         
    
    # Draw a card
    if draw:
        # We already picked a card if we scryed
        if not scry:
            new_card = random.choice(deck)
        hand.append(new_card)
        deck.remove(new_card)
    
    # Playing a land
    lands_played_this_turn = 0
    for land in ["Mine", "PP", "Tower"]:
        if lands_played_this_turn == 0 and land in hand and land not in battlefield:
            hand.remove(land)
            battlefield.append(land)
            lands_played_this_turn = 1
    
    # Check if you played a land
    if lands_played_this_turn > 0:
        # Decide on map or star        
        if "map" in hand and "star" in hand:
            # How many new tron pieces in hand?
            new_tron_in_hand = new_tron_pieces_in_hand(hand, battlefield)
            
            # 2 new pieces? Do star to look for Mulldrifter + Color Fix
            if new_tron_in_hand == 2:
                # Star Opening
                hand.remove("star")
                battlefield.append("star")
                opening[1] += 1
            elif new_tron_in_hand == 1:
                # Map Opening
                hand.remove("map")
                battlefield.append("map")
                opening[0] += 1
            elif new_tron_in_hand == 0:
                ##### These are the hard choice openings (with my logic playing star is way better)
                hand.remove("star")
                battlefield.append("star")
                opening[3] += 1
        elif "map" in hand:
            # Map Opening
            hand.remove("map")
            battlefield.append("map")
            opening[0] += 1
        elif "star" in hand:
            # Star Opening
            hand.remove("star")
            battlefield.append("star")
            opening[1] += 1
        else:
            # Other opening
            opening[2] += 1
    # If you didn't play a land (imposible to get Tron turn 3)                        
    else:
        opening[4] += 1
        return hand_amounts, opening
            
    # Turn 2
    ########
      
    # Draw a card
    new_card = random.choice(deck)
    hand.append(new_card)
    deck.remove(new_card)    
    
    # Count battlefield
    lands_in_battlefield = 1 # (otherwise we would not be here)
    available_C_mana = 1
    G_mana = 0
    
    lands_played_this_turn = 0
    # Play land / Search for Tron
    stop = False
    while not stop:
        if lands_played_this_turn == 0:
            # Playing a land
            for land in ["Mine", "PP", "Tower"]:
                if lands_played_this_turn == 0 and land in hand and land not in battlefield:
                    hand.remove(land)
                    battlefield.append(land)
                    lands_in_battlefield += 1
                    available_C_mana += 1
                    lands_played_this_turn = 1
                
        # Checking for Tron
        if tron_pieces(hand,battlefield) == 3:
            stop = True
        else:
            # Crack Map
            if "map" in battlefield and available_C_mana >= 2:
                # Cost
                available_C_mana -= 2
                # Ability
                battlefield.remove("map")
                for tutored_land in ["Mine", "PP", "Tower"]:
                    if tutored_land not in battlefield and tutored_land in deck:
                        deck.remove(tutored_land)
                        hand.append(tutored_land)
            # Crack Star                
            elif "star" in battlefield and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                
                # Ability
                battlefield.remove("star")
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
                # Add G mana            
                G_mana += 1                        
            # Play Stirrings (Looking for Missing Piece > Map > Star > Prism)
            elif "stirrings" in hand and G_mana > 0:
                # Cost
                G_mana -= 1
                # Ability                                           
                hand.remove("stirrings")
                # Resolve Stirrings
                temp_cards = random.sample(deck, 5)
                card_chosen = 0
                for card in temp_cards:
                    deck.remove(card)
                    if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in battlefield and card not in hand:
                        card_chosen = 1
                        hand.append(card)                                                        
                # Take map, star or prism if you didn't find Tron
                if card_chosen == 0 and "map" in temp_cards and "map" not in hand and "map" not in battlefield and lands_in_battlefield == 2 and (available_C_mana + G_mana) == 1:
                    card_chosen = 1
                    hand.append("map")                    
                elif card_chosen == 0 and "star" in temp_cards:
                    card_chosen = 1
                    hand.append("star")
                elif card_chosen == 0 and "prism" in temp_cards:
                    card_chosen = 1
                    hand.append("prism")
            # Play Map (Likely meaning no Mulldrifter Turn 3)
            elif "map" in hand and "map" not in battlefield and lands_in_battlefield == 2 and (available_C_mana + G_mana) == 1:
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1               
                # Play Map
                hand.remove("map")
                battlefield.append("map")                     
            # Play Star          
            elif "star" in hand and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                                        
                # Ability
                hand.remove("star")
                battlefield.append("star")
            # Play Prism
            elif "prism" in hand and (available_C_mana + G_mana) >= 2:
                # Cost
                if available_C_mana >= 2:
                    available_C_mana -= 2
                elif available_C_mana == 1:
                    available_C_mana -= 1
                    G_mana -= 1                           
                else:
                    G_mana -= 2                                                   
                # Ability
                hand.remove("prism")
                battlefield.append("prism")
                prisms_in_battlefield += 1
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
            # Nothing to do
            else:
                stop = True
        
    # If you didn't play a land is imposible to get Tron turn 3        
    if lands_played_this_turn == 0:
        return hand_amounts, opening
    
    if tron_pieces(hand,battlefield) == 3:
        stop = False
    else:
        stop = True        
    # Search for Mulldrifter (only if you already have Tron)
    while not stop:
        # Checking for Mulldrifter
        if "mull" in hand:
            stop = True
        else:
            # Crack Star
            if "star" in battlefield and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                
                # Ability
                battlefield.remove("star")
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
                # Add G mana            
                G_mana += 1                      
            # Play Star
            elif "star" in hand and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                                        
                # Ability
                hand.remove("star")
                battlefield.append("star")                
            # Play Prism
            elif "prism" in hand and (available_C_mana + G_mana) >= 2:
                # Cost
                if available_C_mana >= 2:
                    available_C_mana -= 2
                elif available_C_mana == 1:
                    available_C_mana -= 1
                    G_mana -= 1                           
                else:
                    G_mana -= 2                                                   
                # Ability
                hand.remove("prism")
                battlefield.append("prism")
                prisms_in_battlefield += 1
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)                
            # Play Stirrings (Looking for Star > Prism)
            elif "stirrings" in hand and G_mana > 0:
                # Cost
                G_mana -= 1
                # Ability                                           
                hand.remove("stirrings")
                # Resolve Stirrings
                temp_cards = random.sample(deck, 5)
                if "star" in temp_cards:
                    hand.append("star")
                elif "prism" in temp_cards:
                    hand.append("prism")                    
            # Nothing to do       
            else:
                stop = True       
        
    if (tron_pieces(hand,battlefield) == 3) and ("mull" in hand):
        stop = False
    else:
        stop = True
    # Search for Fix (if you already have Tron and Mulldrifter)
    while not stop:
        # Play Prism        
        if "prism" in hand and (available_C_mana + G_mana) >= 2:            
            # Cost
            if available_C_mana >= 2:
                available_C_mana -= 2
            elif available_C_mana == 1:
                available_C_mana -= 1
                G_mana -= 1                           
            else:
                G_mana -= 2                                                   
            # Ability
            hand.remove("prism")
            battlefield.append("prism")
            prisms_in_battlefield += 1
            # Draw a card
            new_card = random.choice(deck)
            hand.append(new_card)
            deck.remove(new_card)
        # Play Star                    
        elif "star" in hand and (available_C_mana + G_mana) >= 1:
            # Cost
            if available_C_mana > 0:
                available_C_mana -= 1
            else:
                G_mana -= 1                                        
            # Ability
            hand.remove("star")
            battlefield.append("star")              
        # Play Stirrings            
        elif "stirrings" in hand and G_mana > 0:
            # Cost
            G_mana -= 1
            # Ability                                           
            hand.remove("stirrings")
            # Resolve Stirrings
            temp_cards = random.sample(deck, 5)
            if "star" in temp_cards:
                hand.append("star")
            elif "prism" in temp_cards:
                hand.append("prism")
        # Nothing to do                      
        else:
            stop = True                         

    # Turn 3
    #########
        
    # Draw a card
    new_card = random.choice(deck)
    hand.append(new_card)
    deck.remove(new_card)
    
    # Count battlefield
    lands_in_battlefield = 2 # (otherwise we would not be here)
    available_C_mana = 2
    G_mana = 0    
    untapped_prisms_in_battlefield = prisms_in_battlefield

    lands_played_this_turn = 0
    # Play land / Search for Tron
    stop = False
    while not stop:
        if lands_played_this_turn == 0:
            # Playing a land
            for land in ["Mine", "PP", "Tower"]:
                if lands_played_this_turn == 0 and land in hand and land not in battlefield:
                    hand.remove(land)
                    battlefield.append(land)
                    lands_in_battlefield += 1
                    available_C_mana += 1
                    # Fix the mana Because of Tron (I'll assume that you always tap the tower last) (which is not always possible, but in those cases you can't case Mulldrifter no matter what)
                    if available_C_mana == 3:
                        available_C_mana = 7
                    elif available_C_mana == 2:
                        available_C_mana = 5
                    else:
                        available_C_mana = 3                    
                    lands_played_this_turn = 1
                
        # Checking for Tron
        if tron_pieces(hand,battlefield) == 3:
            opening[5] += 1
            stop = True
        else:
            # Crack Map
            if "map" in battlefield and available_C_mana >= 2:
                # Cost
                available_C_mana -= 2
                # Ability
                battlefield.remove("map")
                for tutored_land in ["Mine", "PP", "Tower"]:
                    if tutored_land not in battlefield and tutored_land in deck:
                        deck.remove(tutored_land)
                        hand.append(tutored_land)
            # Crack Star                
            elif "star" in battlefield and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                
                # Ability
                battlefield.remove("star")
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
                # Add G mana            
                G_mana += 1                        
            # Play Stirrings (Looking for Missing Piece > Map > Star > Prism)
            elif "stirrings" in hand and ((G_mana > 0) or (untapped_prisms_in_battlefield > 0 and available_C_mana > 0)):
                # Cost
                if G_mana > 0:
                    G_mana -= 1
                else:
                    untapped_prisms_in_battlefield -= 1
                    available_C_mana -= 1
                # Ability                                           
                hand.remove("stirrings")
                # Resolve Stirrings
                temp_cards = random.sample(deck, 5)
                card_chosen = 0
                for card in temp_cards:
                    deck.remove(card)
                    if card_chosen == 0 and card in ["Mine", "PP", "Tower"] and card not in battlefield and card not in hand:
                        card_chosen = 1
                        hand.append(card)                                                                       
            # Play Star          
            elif "star" in hand and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                                        
                # Ability
                hand.remove("star")
                battlefield.append("star")
            # Play Prism
            elif "prism" in hand and (available_C_mana + G_mana) >= 2:
                # Cost
                if available_C_mana >= 2:
                    available_C_mana -= 2
                elif available_C_mana == 1:
                    available_C_mana -= 1
                    G_mana -= 1                           
                else:
                    G_mana -= 2                                                   
                # Ability
                hand.remove("prism")
                battlefield.append("prism")
                prisms_in_battlefield += 1
                untapped_prisms_in_battlefield += 1
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
            # Nothing to do
            else:
                stop = True
        
    # If you didn't play a land you don't have Tron        
    if lands_played_this_turn == 0:
        return hand_amounts, opening

    if tron_pieces(hand,battlefield) == 3:
        stop = False
    else:
        stop = True        
    # Search for Mulldrifter (only if you already have Tron)
    while not stop:
        # Checking for Mulldrifter
        if "mull" in hand:
            stop = True
        else:
            # Crack Star
            if "star" in battlefield and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                
                # Ability
                battlefield.remove("star")
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
                # Add G mana            
                G_mana += 1                      
            # Play Star
            elif "star" in hand and (available_C_mana + G_mana) >= 1:
                # Cost
                if available_C_mana > 0:
                    available_C_mana -= 1
                else:
                    G_mana -= 1                                        
                # Ability
                hand.remove("star")
                battlefield.append("star")                
            # Play Prism
            elif "prism" in hand and (available_C_mana + G_mana) >= 2:
                # Cost
                if available_C_mana >= 2:
                    available_C_mana -= 2
                elif available_C_mana == 1:
                    available_C_mana -= 1
                    G_mana -= 1                           
                else:
                    G_mana -= 2                                                   
                # Ability
                hand.remove("prism")
                battlefield.append("prism")
                prisms_in_battlefield += 1
                untapped_prisms_in_battlefield += 1                
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)                
            # Play Stirrings (Looking for Star > Prism)
            elif "stirrings" in hand and ((G_mana > 0) or (untapped_prisms_in_battlefield > 0 and available_C_mana > 0)):
                # Cost
                if G_mana > 0:
                    G_mana -= 1
                else:
                    untapped_prisms_in_battlefield -= 1
                    available_C_mana -= 1
                # Ability                                           
                hand.remove("stirrings")
                # Resolve Stirrings
                temp_cards = random.sample(deck, 5)
                if "star" in temp_cards:
                    hand.append("star")
                elif "prism" in temp_cards:
                    hand.append("prism")                    
            # Nothing to do       
            else:
                stop = True       

    if (tron_pieces(hand,battlefield) == 3) and ("mull" in hand):
        stop = False
    else:
        stop = True
    # Try to play Mulldrifter (if you already have Tron and Mulldrifter in hand)
    while not stop:
        # If you don't have at least 5 mana in total you can't play Mulldrifter no matter what     
        if available_C_mana + G_mana < 5:
            return hand_amounts, opening
            
        # Checking if I can pay for it    
        if available_C_mana >= 4 and G_mana >= 1:
            opening[6] += 1
            return hand_amounts, opening            
        else:
            # Use Prism            
            if  untapped_prisms_in_battlefield > 0 and available_C_mana >= 1:
                # Cost
                available_C_mana -= 1          
                # Ability                
                untapped_prisms_in_battlefield -= 1
                # Add G mana            
                G_mana += 1                   
            # Crack Star
            elif "star" in battlefield and available_C_mana >= 1:
                # Cost
                available_C_mana -= 1          
                # Ability
                battlefield.remove("star")
                # Draw a card
                new_card = random.choice(deck)
                hand.append(new_card)
                deck.remove(new_card)
                # Add G mana            
                G_mana += 1                  
            # Nothing to do                      
            else:
                stop = True
                
    return hand_amounts, opening                    

####
## Run simulations
""" Other way to do the same =>
# starting_hand_analysis[different tron pieces (0 to 3)][stars (0 to 3)][maps (0 to 1)][prisms (0 to 2)][stirrings (0 to 2)][mulldrifters (0 to 1)]
starting_hand_analysis = []

for i in range(4):
    starting_hand_analysis.append([])
    for j in range(4):
        starting_hand_analysis[i].append([])
        for k in range(2):
            starting_hand_analysis[i][j].append([])
            for l in range(3):
                starting_hand_analysis[i][j][k].append([])
                for m in range(3):
                    starting_hand_analysis[i][j][k][l].append([])
                    for n in range(2):
                        starting_hand_analysis[i][j][k][l][m].append([])
                        for o in range(2):
                            starting_hand_analysis[i][j][k][l][m][n].append(0)       
"""
                                               
# starting_hand_analysis[different tron pieces (0 to 3)][stars (0 to 3)][maps (0 to 1)][prisms (0 to 2)][stirrings (0 to 2)][mulldrifters (0 to 1)][objectives (0 to 2) (0 = total, 1 = tron, 2 = mulldrifter))]                                               
starting_hand_analysis = [[[[[[[0 for o in range(3)] for n in range(2)] for m in range(3)] for l in range(3)] for k in range(2)] for j in range(4)] for i in range(4)]

for i in range(N):
    state = game(on_the_draw)
    map_opening += state[1][0]
    star_opening += state[1][1]
    other_opening += state[1][2]
    hard_opening += state[1][3]
    no_land_opening += state[1][4]
    turn_3_tron += state[1][5]
    count_turn_3_mull += state[1][6]
        
    if state[1][3] == 1:
        hard_success_3_tron += state[1][5]
        hard_success_3_mull += state[1][6]
    
    # hand_amounts = [0,0,0,0,0,0,0,0]
    # hand_amounts[0] = hand.count("Mine")
    # hand_amounts[1] = hand.count("PP")
    # hand_amounts[2] = hand.count("Tower")
    # hand_amounts[3] = hand.count("star")
    # hand_amounts[4] = hand.count("map")
    # hand_amounts[5] = hand.count("prism")
    # hand_amounts[6] = hand.count("stirrings")
    # hand_amounts[7] = hand.count("mull")
    different_tron_pieces = 0
    if state[0][0] > 0:
        different_tron_pieces += 1
    if state[0][1] > 0:
        different_tron_pieces += 1
    if state[0][2] > 0:
        different_tron_pieces += 1                        
    stars = min(3, state[0][3])
    maps = min(1, state[0][4])
    prisms = min(2, state[0][5])
    stirrings = min(2, state[0][6])
    mull = min(1, state[0][7])
        
    # starting_hand_analysis[different tron pieces (0 to 3)][stars (0 to 3)][maps (0 to 1)][prisms (0 to 2)][stirrings (0 to 2)][mulldrifters (0 to 1)][objectives (0 to 2) (0 = total, 1 = tron, 2 = mulldrifter))]
    starting_hand_analysis[different_tron_pieces][stars][maps][prisms][stirrings][mull][0] += 1    
    starting_hand_analysis[different_tron_pieces][stars][maps][prisms][stirrings][mull][1] += state[1][5]
    starting_hand_analysis[different_tron_pieces][stars][maps][prisms][stirrings][mull][2] += state[1][6]

####
## Analyze info about hands
starting_hand_analysis_coded = []

# starting_hand_analysis[different tron pieces (0 to 3)][stars (0 to 3)][maps (0 to 1)][prisms (0 to 2)][stirrings (0 to 2)][mulldrifters (0 to 1)][objectives (0 = tron, 1 = mulldrifter))]
for i in range(4):
    for j in range(4):
        for k in range(2):
            for l in range(3):
                for m in range(3):
                    for n in range(2):
                        amount_total = starting_hand_analysis[i][j][k][l][m][n][0]
                        if amount_total > 0:                            
                            amount_tron = starting_hand_analysis[i][j][k][l][m][n][1]
                            amount_mull = starting_hand_analysis[i][j][k][l][m][n][2]
                            #[i,j,k,l,m,n],
                            starting_hand_analysis_coded.append(["%d / %d / %d / %d / %d / %d" % (i,j,k,l,m,n),
                                                                 100 * float(amount_tron) / float(amount_total),
                                                                 100 * float(amount_mull) / float(amount_total),
                                                                 100 * float(amount_total)/N
                                                                 ])                                                           
 
starting_hand_analysis_coded.sort(key=lambda tup: tup[1], reverse=True)
# Filter?
# result = [a for a in starting_hand_analysis_coded if (a[1] < 100 and a[1] > 1)]
result = starting_hand_analysis_coded

output = ""

for line in result:
    output += line[0] + " / " + line[1].__str__() + " / " + line[2].__str__() + " / " + line[3].__str__() + "\n"

print(output)
    
####
## Compute percentages
percentage_turn_3_mull = 100 * float(count_turn_3_mull) / N
percentage_turn_3_tron = 100 * float(turn_3_tron) / N
percentage_map = 100 * float(map_opening) / N
percentage_star = 100 * float(star_opening) / N
percentage_other = 100 * float(other_opening) / N
percentage_no_land = 100 * float(no_land_opening) / N
percentage_hard = 100 * float(hard_opening) / N
if hard_opening > 0:
    percentage_hard_success_3_mull = 100 * float(hard_success_3_mull) / hard_opening
    percentage_hard_success_3_tron = 100 * float(hard_success_3_tron) / hard_opening
else:
    percentage_hard_success_3_mull = 0
    percentage_hard_success_3_tron = 0

#####
## Display results
print("Turn 3 Tron:", percentage_turn_3_tron)
print("Turn 3 Mull:", percentage_turn_3_mull)
print("Map Openings: ", percentage_map)
print("Star Openings: ", percentage_star)
print("Other Openings: ", percentage_other)
print("No Land Openings: ", percentage_no_land)
print("Hard Openings: ", percentage_hard)
print("Hard Openings Turn 3 Tron: ", percentage_hard_success_3_tron)
print("Hard Openings Turn 3 Mull: ", percentage_hard_success_3_mull)