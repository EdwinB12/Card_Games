# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:23:22 2020

@author: edwin
"""

import CardGameLib as CBL
        
    
# ----------------------- Game of Snap using CardGameLib -----------------  

# The Snap player class has additional features on top of the player class needed for the game Snap. 
     
# Player 1 is a Snap Player
snap_deck = CBL.Deck()
play_1 = CBL.Snap_Player('Player 1')

# Additional methods include declaring Snap and declaring Defeat. The extra methods are largely used by the 'Snap' Class so thre user doesn't need to worry abouy them.

# Now add some more players to play Snap with
play_2 = CBL.Snap_Player('Player 2')
play_3 = CBL.Snap_Player('Player 3')
play_4 = CBL.Snap_Player('Player 4')
play_5 = CBL.Snap_Player('Player 5')
players = [play_1,play_2,play_3,play_4,play_5]

# The 'Snap' Class is a game class. This takes a list of players and governs the game of snap between the players. 
snap_game = CBL.Snap(players)

print('\n')
print('Now lets play Snap! ')
print('\n')

# A game must be began using start_game() method. This builds, shuffles and deals a deck. 
snap_game.start_game()

# Play game will then automatically play a game of snap with the included players. A commentary of the game is printed to the command line. 
snap_game.play_game()

# The plot hand_hand_count_hist method plots how each players hand size has changed throughout the game. 
snap_game.plot_hand_count_hist(['b-','g-','y-','r-','k-'])

# If multiple game are played then you can also plot the history of wins with 'plot_win_hist' between the set of players. 
print('\n')
snap_game.start_game()
snap_game.play_game()
snap_game.plot_hand_count_hist(['b-','g-','y-','r-','k-'])
snap_game.plot_win_hist()



# ----------------------------------------------------------------------
# This example plays 10 game tournament and plots the win history of the players. 
# ----------------------------------------------------------------------

tournament_play1 = CBL.Snap_Player('Bob')
tournament_play2 = CBL.Snap_Player('Janet')
tournament_play3 = CBL.Snap_Player('Viv')

tournament_players = [tournament_play1,tournament_play2,tournament_play3]
snap_game = CBL.Snap(tournament_players)


print('\n')
print('--------- Play 10 game Tournament --------------')
print('\n')

for i in range(1,11):
    print('Game', i)
    print('\n')
    snap_game.start_game()
    snap_game.play_game()
    snap_game.plot_hand_count_hist(['b-','g-','y-','r-','k-'],('Game ' + str(i)))

snap_game.plot_win_hist()