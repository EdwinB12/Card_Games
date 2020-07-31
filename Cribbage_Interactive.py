# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 18:56:24 2020

@author: edwin
"""

import CardGameLib as CGL
from itertools import combinations
import numpy as np

               
#%%

crib_game = CGL.Cribbage() 
   
# Now play_game() method will automate a game of cribbage to the target score entered.
crib_game.start_game()
crib_game.play_game(40)

crib_game.game_plots(['y-','g-','r-','b-'])
























