# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 16:38:40 2020

@author: edwin
"""

import random
import sys
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
import scipy.stats as ss

# -------------------------- Card Class ------------------------------

class Card:
    
    def __init__(self,suit,num,ace_high=False):
        
        self.suit = suit
        self.num = int(num)
        self.ace_high = ace_high
        
        if self.ace_high == True and self.num == 1:
            self.num = 14
            
        if self.num > 10 and self.num < 14:
            self.val = 10
            
        elif self.num == 14:
            self.val = 11
            
        else:
            self.val = self.num
        
        if self.num == 11:
            self.face = 'Jack'
        elif self.num == 12:
            self.face = 'Queen'
        elif self.num == 13:
            self.face = 'King'
        elif self.num == 1 or self.num == 14:
            self.face = 'Ace'
        else:
            self.face = self.num
        
    def show(self):
        print (f"{self.face} of {self.suit}")
    
    def return_show(self):
        return (f"{self.face} of {self.suit}")
    


# -------------------------- Deck Class ------------------------------


class Deck:
    
    def __init__(self):
        self.cards = []
        self.turn_up_card = []
        
        
    def build(self):
        
        # Loop Around Suits
        for suit in ['Clubs','Diamonds','Hearts', 'Spades']:
            # Loop around Cards
            for num in range(1,14):
                self.cards.append(Card(suit,num))
        print('Deck built')
                
    def show(self):
        
        # Loop through list of cards
        for card in self.cards:
            card.show()
    
    def shuffle(self):
        
        random.shuffle(self.cards)
        print('Deck shuffled')
        
    def draw(self,draw_size=1):
        
        for i in range(0,draw_size):
            return self.cards.pop(0)
        
        print(f'{draw_size} cards are drawn from the deck')
        
    def count(self):
        
        print(f"The deck has {len(self.cards)} cards left")
    
        
    def deal(self,players,cards_per_player):
        
        if cards_per_player == 'max':
            
            quotient = len(self.cards) // len(players)
            remainder = len(self.cards) % len(players)
            
            for i in range(0,quotient):
                for player in players:
                    player.draw_hand(self)
            
            for i in range(0,remainder):
                players[i].draw_hand(self)
            
        else: 
            
            if len(self.cards) < len(players)*cards_per_player:
                print(f'There are not enough cards in the deck to deal {cards_per_player} cards to {len(players)} players ')
                sys.exit()
            
            # Important to deal one card at a time - espeically for games that don't shuffle between rounds like cribbage
            for i in range(0,cards_per_player):
                for player in players:
                    player.draw_hand(self)
        
        print('Cards are dealt')
        
        
    def turn_up(self):
        self.turn_up_card = self.cards.pop(0)
        print('The turn up card is', self.turn_up_card.return_show())
        
        
    def return_turn_up(self):
        self.cards.append(self.turn_up_card)
        self.turn_up_card=[]
        print('Turn up card has been returned to the deck')
            
        
# -------------------------- Player Class ------------------------------
        

class Player:
    
    def __init__(self,name):
    
        self.hand=[]
        self.name=name
        self.hc_lst = [] # For keeping track of hand size throughout a game
        self.wins = 0 # For keeping track num of wins
        self.rank = 1
        self.rank_hist = []
        self.position = None
        
    def draw_hand(self,deck,draw_size=1):
        
        for i in range(0,draw_size):
            self.hand.append(deck.draw(draw_size))
        
    def show_hand(self):
        
        print(f'{self.name}''s hand contains:')
        # Loop through list of cards
        for card in self.hand:
            card.show()
            
    def play_card(self,deck):
        
        card_played =[]
        card_played = self.hand.pop(0)
        deck.cards.append(card_played)
        card_played.show()
        
        
    def discard_hand(self,deck=None):
        
        if deck == None:
            self.hand=[]
            print(f'{self.name} discards hand')
        
        else:
        
            for i in range(0,len(self.hand)):
                deck.cards.append(self.hand[i])
            self.hand=[]
            
            print(f'{self.name} discards hand to bottom of deck')
        
    def count_hand(self):
        
        print(f"{self.name}'s hand has {len(self.hand)} cards")
        
    def record_hand_count(self):
        self.hc_lst.append(len(self.hand))
        
    def record_win(self):
         self.wins+=1
    
    def update_rank(self):
        self.rank_hist.append(self.rank)
 

# -------------------------- Snap Player Class ------------------------------


class Snap_Player(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.snap = False
    
    def declare_snap(self,deck):
        if self.snap == True:
            for i in range(0,len(deck.cards)):
                self.hand.append(deck.cards[i])
                
            print(f'{self.name}: SNAP!!!!')
            print(f'{self.name} picks up {len(deck.cards)} cards')
            deck.cards=[]
            self.snap=False
        else:
            pass
        
    def declare_defeat(self):
        if not self.hand:
            print(f'{self.name} is defeated!')
            return True
            
        else:
            pass


# -------------------------- Cribbage Player Class ------------------------------


class Cribbage_Player(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.score=0
        self.score_hist = []
        self.max_hand = []
        self.max_hand_score = 0
        self.max_hand_turn_up = []
        
    def calc_score(self,deck):
        
        # Calculate cribbage count up score from 5 cards where 4 cards have been drawn and 1 card is turned up
        # 15's, straights, flushes, pairs and knobs are seperately calculated and added up for a total score. 
        
        # For the purpose of calculating the points, the turn-up card is added to the hand (it wil be removed at the end of the method)
        self.hand.append(deck.turn_up_card)
        
        # List of hand values and suits is generated
        hand_values = [c.val for c in self.hand]
        hand_suits = [c.suit for c in self.hand]
        hand_nums =  [c.num for c in self.hand]
        
        # Initialise seperate score variables
        score_total,score_15s,score_straight,score_flush,score_pair,score_knob = [0,0,0,0,0,0]
        
        
        # ------------------- Calcuating score for 15s --------------------------------
        
        # Loop around all unique hands between 2 and 5 cards.
        for i in range(2,6):
            for comb in combinations(hand_values,i):
                # If sum of any combinations equal 15, then add 2 to the score
                if sum(comb) == 15:
                    score_15s+=2
                
        
       # ------------------- Calcuating score for Pairs --------------------------------
       
        
        # Loop through a set of the hand nums
        for j in set(hand_nums):
            # count number of instances for each number in original hand
            pair = hand_nums.count(j)
            # Calculate score based on how many times a number occurs
            score_pair += (pair**2 - pair)
        
        # ------------------- Calcuating score for Straights --------------------------------
        
        # Set min length of a straight
        min_straight = 3
        
        # Loop through unique combinations of hands with 3-5 cards
        for i in range(3,6): 
            
            for comb in combinations(hand_nums,i):
                comb = sorted(comb)
                
                # Straight = True if this combination of the hand is a straight
                straight = comb == list(range(min(comb),max(comb)+1) )
                
                # Reset score and calcualte score for all straight of the same length if a straight longer than previously encountered is found 
                if straight and i > min_straight:
                    score_straight =0
                    score_straight+=i
                    min_straight+=1
                
                # Otherwise, if combination is a straight then add to score
                elif straight:
                    score_straight+=i
                
                else:
                    continue
        
        
        # ------------------- Calculating score for Flush --------------------------------
        
        # Returns true if first 4 cards are the same suit (ignore the turn over card)
        flush_4 = all(hand_suits[0] == s for s in hand_suits[0:4])
        
        if flush_4:
            # Check if flush is a five card flush. Assign score accordingly
            flush_5 = all(hand_suits[0] == s for s in hand_suits[0:5])
            if flush_5:
                score_flush = 5
            else: 
                score_flush = 4
    
        
        # Removing turn up card from hand as no longer needed
        self.hand.pop(-1)
        
        
        # ------------------- Calculating score for Knobs --------------------------------
        # This simply gives a score =1 if the hand contains a jack with the same suit as the turn up card
        
        for card in self.hand:
            if card.num== 11 and card.suit == deck.turn_up_card.suit:
                score_knob+=1
        
        # Add Score Up
        score_total = score_15s + score_straight + score_flush + score_pair + score_knob
        
        scores,names = (score_15s,score_pair,score_straight,score_flush,score_knob),('fifteens','pairs','straights','the flush','his knobs')
        for score,name in zip(scores,names):
            if score > 0:
                print(f'{score} for {name}')
        print(f'Hand Score is {score_total}')

        # Add Score to players score
        self.score += score_total
        self.score_hist.append(self.score)
       
       
        # Check if current hand is best hand yet
        if score_total > self.max_hand_score:
            self.max_hand_score = score_total
            self.max_hand = self.hand
            self.max_hand_turn_up = deck.turn_up_card
        else:
            pass            
        
        
        
    def declare_score(self):
        print(f'{self.name}s score is {self.score}')
    
    def show_max_hand(self):
        for card in self.max_hand:
            card.show()
        self.max_hand_turn_up.show()



# -------------------------- Cribbage Game Class ------------------------------

class Cribbage():
    
    def __init__(self,players):
        self.players = players # List of 'Cribbage_Player' classes
        self.deck = Deck() # Deck class
        self.is_winner = False
        
    def start_game(self):
        print(f'Cribbage Game starts with {len(self.players)} players. Their names are:')
        for player in self.players:
            print(player.name)
        
        print('\n')
       
        # Buld, shuffle deck
        self.deck.build()
        self.deck.shuffle()
        
        print('\n')
        print('Let the game begin!')
        
    def play_hand(self,player):
        
        # Start player's turn
        print(f'------- {player.name}\'s turn -------')
        player.calc_score(self.deck) # 
        player.discard_hand(self.deck)
        player.declare_score()
    
    def play_round(self,score_target):
        
        
        self.deck.deal(self.players,4)
        self.deck.turn_up()
        
        # Count up each players score
        for player in self.players:
            Cribbage.play_hand(self,player)
            if player.score >= score_target:
                return
            else:
                continue
        
        # Return turn_up card
        print('\n')
        self.deck.return_turn_up()
        
        if len(self.deck.cards) !=52:
            print(f'STOP! The deck has {len(self.deck.cards)} cards!')
            sys.exit()
        
        # Bring last member of list to the front for next round
        popped = self.players.pop(0)
        self.players.append(popped)
            
    def record_ranks(self):
        
        # Create a list of ranks 
        scores = np.array([player.score for player in self.players])
        ranks = ss.rankdata(-scores,'min')
        
        # Update player rank
        for (player,rank) in zip(self.players,ranks):
            player.rank = rank
            player.update_rank()
            
            
    def play_game(self,score_target):
        
        rnd = 1
        # Loop until a player reaches the target score
        while all(player.score < score_target for player in self.players):
            
            print('\n')
            print(f'--------------- Round {rnd} ----------------')
            print('\n')
            
            Cribbage.play_round(self,score_target)
            Cribbage.record_ranks(self)
            rnd +=1
            
        # Announce Winner 
        winning_player = self.players[np.argmax([player.score for player in self.players])]
        print('\n')
        print(f'{winning_player.name} is the winner with a score of {winning_player.score}!')
        print('\n')
   
    def game_plots(self,line_colors):
        
        # Loop through players and supplied line
        fig,[ax1,ax2] = plt.subplots(2,figsize=(6,6))
        for player,line_color in zip(self.players,line_colors):
            
            # Plot score history
            ax1.plot(range(1,len(player.score_hist)+1),player.score_hist,line_color,label=player.name)
            
            # Plot rank history
            ax2.plot(range(1,len(player.rank_hist)+1),player.rank_hist,line_color,label=player.name)
            ax2.invert_yaxis()
        
        ax1.legend()
        ax1.set_xlabel('Rounds')
        ax1.set_ylabel('Score')
        ax2.set_xlabel('Rounds')
        ax2.set_ylabel('Ranks')
        
    def max_scoring_hands(self):
        
        for player in self.players:
            print(f'{player.name}\'s highest hand of the game was:')
            player.show_max_hand()
            print(f'with a score of {player.max_hand_score}')
            print('\n')
    
    def print_stats(self):
        pass


# -------------------------- Snap Game Class ------------------------------

class Snap():
    
    def __init__(self,players):
        
        self.players_orig = players.copy() # This is the list of the starting players and is used for plots post game
        self.players = players # List of 'Snap_Player' classes. This will be edited throughout the game
        self.deck = Deck() # Deck class - This deck is where the cards are dealth from
        self.play_deck = Deck() # This deck acts as the table. This is where cards are played down
    
    def start_game(self):
        print(f'Snap Game starts with {len(self.players)} players. Their names are:')
        for player in self.players:
            print(player.name)
        
        print('\n')
       
        # Buld, shuffle deck
        self.deck.build()
        self.deck.shuffle()
        self.deck.deal(self.players,'max')
        
        print('\n')
        print('Let the game begin!')
        print('\n')
        
        
    def play_game(self):
        
        self.deck.deal(self.players,'max') # Deal cards
        
        # Initliase counts
        deck_cnt=0
        card_cnt = 0
        
     # Loop whilst there are more than 1 player
        while len(self.players) > 1:
            
            # Loop through the list of players
            for index,player in enumerate(self.players):
                
                player.record_hand_count() # records hand size for post game plots
                
                # Check if any player has no cards left. If not, then dlecare defeat and remove from player list
                if player.declare_defeat():
                    self.players.pop(index)
                    continue
                
                # Play card onto playing deck (table)
                player.play_card(self.play_deck)
                card_cnt+=1
                
                # If it is first card to be played, then it can't be snap so don't check for snap
                if deck_cnt ==0:
                    deck_cnt+=1
                    
                else:
                    # Chec if current card matches previous card
                    if self.play_deck.cards[deck_cnt].num == self.play_deck.cards[deck_cnt-1].num:
                        
                        # Calculate random winner of snap
                        self.players[random.randint(0,len(self.players)-1)].snap = True
                        deck_cnt=0
                        
                        # Loops through players to declare snap (random num has already chosen who will win, rest of logic is handled in the class)
                        for player in self.players:
                            player.declare_snap(self.play_deck)
                    
                    # If no snap, then continue
                    else:
                        deck_cnt+=1
            
        # Record player win incase multiple games are played
        self.players[0].record_win()
                
        #---------------------- Game Finished -------------------------------
        
        print(f'The winner is {self.players[0].name} with {len(self.players[0].hand)} cards left!')
        print(f'Total number of cards played was {card_cnt}')   
        
    def plot_hand_count_hist(self,line_colors):
        
        # Plot win history if multiple games have been played
        fig,ax = plt.subplots(figsize=(6,6))
        for player,line_color in zip(self.players_orig,line_colors):
            ax.plot(range(0,len(player.hc_lst)),player.hc_lst,line_color,label=player.name)        
            
        ax.legend()
        ax.set_xlabel('Turns')
        ax.set_ylabel('Cards in hand')
        
    def plot_win_hist(self):
        
        # Plot win history if multiple games have been played
        fig,ax = plt.subplots(figsize=(6,6))
        for player in self.players_orig:
            ax.scatter(player.name,player.wins)
            
        ax.set_xlabel('Players')
        ax.set_ylabel('Wins')
        
        
        
#%%  ---------- Game of Snap -----------------  
     
# Initilise players and Deck
play_1 = Snap_Player('Player 1')
play_2 = Snap_Player('Player 2')
play_3 = Snap_Player('Player 3')
play_4 = Snap_Player('Player 4')
play_5 = Snap_Player('Player 5')
players = [play_1,play_2,play_3,play_4,play_5]

# Initialise Game
snap_game = Snap(players)

# Start and play Snap Game
snap_game.start_game()
snap_game.play_game()

# Plot histories of hand count and wins
snap_game.plot_hand_count_hist(['b-','g-','y-','r-','k-'])
snap_game.plot_win_hist()


#%%  ---------- Game of Cribbage -----------------

# Initialise Players
crib_1 = Cribbage_Player('Dad')
crib_2 = Cribbage_Player('Mum')
crib_3 = Cribbage_Player('Edwin') 
crib_4 = Cribbage_Player('Frances')
crib_5 = Cribbage_Player('Esther') 

# Initlaise game class 
Crib = Cribbage([crib_1,crib_2,crib_3,crib_4,crib_5])

# Start Game
Crib.start_game() 

# Play game until someone reaches 50 points
Crib.play_game(50)

# Plot how score and rank change throughout the game
Crib.game_plots(['b-','g-','y-','r-','k-'])

# Reveal scoring hands 
Crib.max_scoring_hands()