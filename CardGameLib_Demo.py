# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:38:40 2020

@author: edwin
"""

import CardGameLib as CGL

# --------------------- Card Class -------------------------

print('------------------ Card Class ---------------------')
print('\n')

# The card class simulates a playing card
card = CGL.Card('Hearts',12)

# We can print the card
card.show()

# We can access the cards suit, number and value. Note the number and value are different for face cards. 
print(f'The example cards suit is {card.suit}')
print(f'The example cards number is {card.num}')
print(f'The example cards value is {card.val}')

# The real intention of the card class however is to be used in further classes 

print('\n')

# ------------------ Deck Class ---------------------
print('------------------ Deck Class ---------------------')
print('\n')

# This class simulates a deck of cards
deck = CGL.Deck()

# First the deck must be built - This creates a standard deck of playing cards using the Card class
deck.build()

# We can now show the deck and count the cards
deck.show()
deck.count()

print('\n')

# The deck can be shuffled with the shuffle method
deck.shuffle()
deck.show()

print('\n')

# A card can also be turned up and returned to the deck or generally discarded 
deck.turn_up()
deck.turn_up_card # Turn up card is stored in this attribute
deck.return_turn_up()

# The cards in the deck can be accessed in the card attribute
deck.cards

print('\n')
# ------------------ Player Class ---------------------
print('------------------ Player Class ---------------------')
print('\n')


# This class represents a player. It provides the basic player methods that are inherited by specialsied players. 
player_1 = CGL.Player('Maria')
player_2 = CGL.Player('Jason')

# The deck can be dealt to a list of players - A specified number of cards or 'max' where all cards are dealt
deck.deal([player_1,player_2],4) # 4 Cards 
# or 
#deck.deal([player_1,player_2],'max') # all cards

print('\n')

# Players card are stored as a list in attribute 'hand' and the players name as 'name'
player_1.hand
player_1.name

# The player can count their cards
player_1.count_hand()

# or show their hand
player_2.show_hand()

print('\n')

# Players can discard cards
player_1.discard_hand()
player_1.count_hand()

# Players can pick new cards from a specified deck
new_deck = CGL.Deck()
new_deck.build() # Build new deck

# Draw 2 cards from new deck
player_1.draw_hand(new_deck,2)
player_1.show_hand()



# These classes are the bedrock for the simualted cribbage and snap games to be played later. 

























