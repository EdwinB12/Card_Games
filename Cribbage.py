# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:23:33 2020

@author: edwin
"""

import CardGameLib as CBL

# Cribbage is a complex 2,3 or 4 player game. The Cribbage class uses extra methods in the Cribbage Player class to automate games of cribbage. 

# First Define your Cribbage players  
p1 = CBL.Cribbage_Player('Player 1')  
p2 = CBL.Cribbage_Player('Player 2')  
p3 = CBL.Cribbage_Player('Player 3')  
p4 = CBL.Cribbage_Player('Player 4')
p5 = CBL.Cribbage_Player('Player 5')

# First we demonstrate the start game method with different number of players. Note how 5 players are not allowed and will sys.exit. 
players2 = [p1,p2]
players3 = [p1,p2,p3]
players4 = [p1,p2,p3,p4]
players5 = [p1,p2,p3,p4,p5]

for players in [players2,players3,players4,players5]:

    Crib_Game = CBL.Cribbage(players)
    Crib_Game.start_game() # The start game method builds and shuffles the deck. 

#%% Example Game

p1 = CBL.Cribbage_Player('Player 1')  
p2 = CBL.Cribbage_Player('Player 2')  
p3 = CBL.Cribbage_Player('Player 3')  
p4 = CBL.Cribbage_Player('Player 4')
players = [p1,p2,p3,p4]    
crib_game = CBL.Cribbage(players) 
   
# Now play_game() method will automate a game of cribbage to the target score entered.
crib_game.start_game()
crib_game.play_game(100)

# Game plot method is used to plot scoring history and rank throughout the game
crib_game.game_plots(['y-','g-','r-','b-'])

# and play another game. . 
crib_game.start_game()
crib_game.play_game(20)
crib_game.game_plots(['y-','g-','r-','b-'])

# plot the win history
crib_game.plot_win_hist()


#%% Cribbage Tournament

# 3 player tournament
p1 = CBL.Cribbage_Player('Player 1')  
p2 = CBL.Cribbage_Player('Player 2')  
p3 = CBL.Cribbage_Player('Player 3')
players = [p1,p2,p3]    
crib_game = CBL.Cribbage(players) 

# We will play to 100 points
for i in range(1,11):
    print('------------ Game ' , i, '-----------------')
    crib_game.start_game() 
    crib_game.play_game(50)
    crib_game.game_plots(['y-','g-','r-'])
    
# plot the win history
crib_game.plot_win_hist()
    
    
    
    
    
    