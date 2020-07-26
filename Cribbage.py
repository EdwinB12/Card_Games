# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 11:23:33 2020

@author: edwin
"""

import CardGameBasics as CBG
        
p1 = CBG.Cribbage_Player('Esther')  
p2 = CBG.Cribbage_Player('Edwin')  
p3 = CBG.Cribbage_Player('Bethany')  
p4 = CBG.Cribbage_Player('Sarah')
p5 = CBG.Cribbage_Player('Glenda')

#players = [p1,p2]
#players = [p1,p2,p3]
players = [p1,p2,p3,p4]
#players = [p1,p2,p3,p4,p5]

Crib_Game = CBG.Cribbage(players)

Crib_Game.start_game()
Crib_Game.play_game(200)

Crib_Game.game_plots(['y-','g-','r-','b-'])
