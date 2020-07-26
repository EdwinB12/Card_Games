# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:23:22 2020

@author: edwin
"""

import CardGameBasics as CBG
        
    
# ---------- Game of Snap -----------------  
     
# Initilise players and Deck
play_1 = CBG.Snap_Player('Esther')
play_2 = CBG.Snap_Player('Edwin')
play_3 = CBG.Snap_Player('Sarah')
play_4 = CBG.Snap_Player('Gavin')
play_5 = CBG.Snap_Player('Glenda')
players = [play_1,play_2,play_3,play_4,play_5]

# Initialise Game
snap_game = CBG.Snap(players)

# Start and play Snap Game
snap_game.start_game()
snap_game.play_game()

# Plot histories of hand count and wins
snap_game.plot_hand_count_hist(['b-','g-','y-','r-','k-'])
snap_game.plot_win_hist()