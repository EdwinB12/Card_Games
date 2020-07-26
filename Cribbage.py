# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:23:33 2020

@author: edwin
"""

import CardGameBasics as CBG
        
p1 = CBG.Cribbage_Player('Player 1')  
p2 = CBG.Cribbage_Player('Player 2')  
p3 = CBG.Cribbage_Player('Player 3')  
p4 = CBG.Cribbage_Player('Player 4')
p5 = CBG.Cribbage_Player('Player 5')

#players = [p1,p2]
#players = [p1,p2,p3]
players = [p1,p2,p3,p4]
#players = [p1,p2,p3,p4,p5]

Crib_Game = CBG.Cribbage(players)

Crib_Game.start_game()
Crib_Game.play_game(200)

Crib_Game.game_plots(['y-','g-','r-','b-'])
