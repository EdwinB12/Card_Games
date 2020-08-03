# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 10:03:36 2020

@author: edwin
"""

import tkinter as tk


# Define First window
root = tk.Tk()
root.title('Cribbage GUI') # Title
frame = tk.LabelFrame(root) # Creating Frame
frame.pack()

# ---------------------------------------------------------------------------
# --------------------------- 1st Screen ------------------------------------

# Ask how many players are playing
num_of_players_button=tk.Label(frame,text='How many players?') 

# Player Num Command
def add_player_num(num):
    # Create global variable and assign it to the button value. Finally Delete all the widgets. 
    global player_num 
    player_num = num
    
    # Remove buttons and widgets after button is pressed
    frame.pack_forget()
    
    # Call 2nd screen function
    screen_2()

# Buttons provided for the three options
players_2 = tk.Button(frame,text='2',command = lambda: add_player_num(2))
players_3 = tk.Button(frame,text='3',command = lambda: add_player_num(3))
players_4 = tk.Button(frame,text='4',command = lambda: add_player_num(4))

# Positioning buttons
num_of_players_button.grid(row=0,column=0,columnspan=3)
players_2.grid(column=0,row=2)
players_3.grid(column=1,row=2)
players_4.grid(column=2,row=2)

    
# ---------------------------------------------------------------------------
# --------------------------- 2nd Screen ------------------------------------

def screen_2():
    # Creating list to store players names
    global players
    players = []
    
    # Create Frame2 
    global frame2
    frame2 = tk.LabelFrame(root) # Creating Frame
    frame2.pack()
    
    # Create labels asking for 1st player names
    tk.Label(frame2,text='Your Name:').grid(row=0,column=0)
    name = tk.Entry(frame2)
    players.append(name)
    name.grid(row=0,column=1)
    
    # Loop around depending on how many players there are creating a new button
    for i in range (1,player_num):
        tk.Label(frame2,text='Player ' + str(i+1) + "'s Name:").grid(row=i,column=0)
        name = tk.Entry(frame2)
        players.append(name)
        name.grid(row=i,column=1)
    
    # Creating submit button 
    tk.Button(frame2,text='Submit Names',command = submit_names_button).grid(row=i+1,column=0,columnspan=2)
    
    
    
def submit_names_button():
    
    # Save submitted name when submit name is pressed
    global player_names
    player_names = [player.get() for player in players]
    
    # Call Screen 3 function
    screen_3()
    
    
# ---------------------------------------------------------------------------
# --------------------------- 3rd Screen ------------------------------------   

def screen_3():
    
    # Remove current frame
    frame2.pack_forget()
    
    # Create New Frame
    frame3 = tk.LabelFrame(root) # Creating Frame
    frame3.pack()
    
    
    
    
    
    








root.mainloop()
