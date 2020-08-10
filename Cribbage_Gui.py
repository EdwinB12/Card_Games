# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 10:03:36 2020

@author: edwin
"""

import tkinter as tk
import CardGameLib as CGL

from PIL import Image,ImageTk






# Define First window
root = tk.Tk()
root.title('Cribbage GUI') # Title
root.geometry('500x500')
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

def get_card_path(card):
    '''
    Get relative path to card
    '''
    card_name = (str(card.face) + '_of_' + card.suit + '.png').lower()
    card_path = 'Images/Cards/' +  card_name
    return card_path

def prep_img(card_path, dims=(50,75)):
    '''
    Prep image for GUI
    '''
    img = Image.open(card_path)
    img = img.resize(dims,Image.ANTIALIAS)
    card_img = ImageTk.PhotoImage(img)
    return card_img

def button_position(button,card_img,column,row):
    
    # Positon button and set switch attribute
    button.image = card_img
    button.grid(column = column, row = row)
    button.on = False

def screen_3():
    
    # Remove current frame
    frame2.pack_forget()
    
    # Create New Frame for cards
    card_frame = tk.LabelFrame(root) # Creating Frame
    card_frame.grid(row = 1, column = 2)
    
    # Creating list of cribbage players
    crib_players = [CGL.Cribbage_Player(name) for name in player_names]
    
    # Create and start game    
    crib_game = CGL.Cribbage(crib_players,'No') 
    crib_game.start_game()
    
    # Deal to players
    crib_game.deal()
    
    # Loop through the active players hand
    global hand
    hand = crib_game.players[0].hand
    
    #create list of card buttons
    card_imgs = []
    
    for i,card in enumerate(hand):
        
        # Create Card Path
        card_path = get_card_path(card)
    
        # Prep Cards image
        card_imgs.append(prep_img(card_path))
    
    # Create Card Buttons
    c0 = tk.Button(card_frame,image=card_imgs[0],bg = 'White',command = lambda: card_discard(c0))
    c1 = tk.Button(card_frame,image=card_imgs[1],bg = 'White',command = lambda: card_discard(c1))
    c2 = tk.Button(card_frame,image=card_imgs[2],bg = 'White',command = lambda: card_discard(c2))
    c3 = tk.Button(card_frame,image=card_imgs[3],bg = 'White',command = lambda: card_discard(c3))
    c4 = tk.Button(card_frame,image=card_imgs[4],bg = 'White',command = lambda: card_discard(c4))
    c5 = tk.Button(card_frame,image=card_imgs[5],bg = 'White',command = lambda: card_discard(c5))
    
    # Position Button
    button_position(c0,card_imgs[0],0,1)
    button_position(c1,card_imgs[1],1,1)
    button_position(c2,card_imgs[2],2,1)
    button_position(c3,card_imgs[3],3,1)
    button_position(c4,card_imgs[4],4,1)
    button_position(c5,card_imgs[5],5,1)

    # Create Player 1 and 2 Box
    p1 = tk.Label(root,text=player_names[0],background='White', font=('Courier',20))
    p2 = tk.Label(root,text=player_names[1],background='White', font=('Courier',20))
    p2.grid(row = 0, column = 2, pady = 50)
    p1.grid(row = 5, column = 2)
    

def card_discard(button):
    '''
    Highlight cards and then discard when two have been selected
    '''
    button.on = not button.on
    
    if button.on is True: 
        button.configure(bg= '#00ff00') 
    else:
        button.configure(bg= 'White')
   
    
    

root.mainloop()




#%%
































