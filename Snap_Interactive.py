# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:29:02 2020

@author: edwin
"""
import pygame
import CardGameLib as CGL
import inspect


#%%

# Prompt user for players
name = ''

user_name = input('Enter your user name:')
active_player = CGL.Snap_Player(user_name)
players = [active_player]


for i in range(0,9):
    name = input('Enter automated opponents name or start the game:')
    if name == 'start':
        break
    else:
        players.append(CGL.Snap_Player(name))


#%%

snap = CGL.Snap(players)

snap.start_game()

snap.play_game_interactive(active_player)


#%%

from func_timeout import FunctionTimedOut, func_timeout

try:
   ans = func_timeout(3, lambda: int(input('What is the sum of 2 and 3?\n')))
except FunctionTimedOut:
   pass


