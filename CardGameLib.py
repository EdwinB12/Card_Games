# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:11:06 2020

@author: edwin
"""


import random
import sys
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
import scipy.stats as ss



class Card:
    
    '''
    Class to represent a playing card.
    
    '''
    
    def __init__(self,suit,num,ace_high=False):
        
        self.suit = suit # Suit of Card
        self.num = int(num) # Number of card: Ace = 1, Jack = 11, Queen = 12, King = 13
        self.ace_high = ace_high # Boolean whether you want ace to be high or low. Default is False so ace is low. 
        
        # If Ace has value = 1 and user wants it to be high, make it worth 14
        if self.ace_high == True and self.num == 1: 
            self.num = 14
        
        # --------------- Setting Card Values --------------------------
        
        # if Picture card, set value = 10
        if self.num > 10 and self.num < 14:
            self.val = 10
        
        # Set Ace to 11 if its high
        elif self.num == 14:
            self.val = 11
        
        else:
            self.val = self.num
        
        # -------------- Setting Face of card (what it is called; aka 'Jack' not 11) ----------------
        
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
    
    # ------------------ Methods for showing card ------------------------
    
    def show(self):
        print (f"{self.face} of {self.suit}")
    
    def return_show(self):
        return (f"{self.face} of {self.suit}")


class Deck:
    
    def __init__(self):
        
        self.cards = [] # List of Cards - To be populated by 'Card' class Objects
        self.turn_up_card = [] # Single turn up card - required for some games
        
        
        
        
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
            

class Player:
    
    def __init__(self,name):
    
        self.hand=[] # List of Card Objects
        self.name=name # String name of the player
        self.hc_lst = [] # For keeping track of hand size throughout a game
        self.wins = 0 # For keeping track num of wins
        self.rank = 1 # Rank - Used when playing a game
        self.rank_hist = [] # History of the rank
    
    # ------------------------ Card Action Methods ------------------------
    
    def play_card(self,deck):
        
       card_played =[]
       card_played = self.hand.pop(0)
       deck.cards.append(card_played)
       print(self.name, 'plays:', card_played.return_show())
    
    # ------------------------ Hand Action Methods ------------------------

    def draw_hand(self,deck,draw_size=1):
        
        for i in range(0,draw_size):
            self.hand.append(deck.draw(draw_size))
        
    def show_hand(self):
        
        print(f'{self.name}''s hand contains:')
        # Loop through list of cards
        for card in self.hand:
            card.show()
        
    def discard_hand(self,deck=None):
        
        if deck == None:
            self.hand=[]
            print(f'{self.name} discards hand')
        
        else:
        
            for card in self.hand:
                deck.cards.append(card)
            self.hand=[]
            
            print(f'{self.name} discards hand to bottom of deck')
        
    def count_hand(self):
        
        print(f"{self.name}'s hand has {len(self.hand)} cards")
        return len(self.hand)
    # ------------------ Update record (different metrics) methods -------------------------
        
    def update_hand_count(self):
        self.hc_lst.append(len(self.hand))
        
    def update_win(self):
         self.wins+=1
    
    def update_rank(self):
        self.rank_hist.append(self.rank)


class Cribbage_Player(Player):
    
    def __init__(self,name):
        
        # Inherit from Player Class
        super().__init__(name)
        
        # Updating the Score for the 
        self.hand_score = 0 # Score for a single hand
        self.hand_score_hist = [] # History of the players hand scores
        self.game_score=0 # Overall Game Score
        self.game_score_hist = [] #  History of overall game scores (Used when multiple games are played)
        
        self.max_hand = [] # Max scoring hand of the game
        self.max_hand_score = 0 # Max score by a hand in the game 
        self.max_hand_turn_up = [] # Do I Need this? 
        
        self.box_card = [] # This is the rejected card that will be sent to the box
        self.box=[] # This is the box hand
        self.box_score = 0
        self.box_score_hist = [] # Box History
        
    def calc_score(self,hand,deck,count_up):
        
        # Calculate cribbage count up score from 5 cards where 4 cards have been drawn and 1 card is turned up
        # 15's, straights, flushes, pairs and knobs are seperately calculated and added up for a total score. 
        
        
        if count_up:
            # For the purpose of calculating the points at count up, the turn-up card is added to the hand (it wil be removed at the end of the method)
            hand.append(deck.turn_up_card)
        
        # List of hand values and suits is generated
        hand_values = [c.val for c in hand]
        hand_suits = [c.suit for c in hand]
        hand_nums =  [c.num for c in hand]
        
        # Initialise seperate score variables
        hand_score,score_15s,score_straight,score_flush,score_pair,score_knob = [0,0,0,0,0,0]
        
        
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
    
        
        
        
        # If counting up card score at the end of the round, then check for knobs
        
        
        if count_up:
            
            # Removing turn up card from hand as no longer needed
            hand.pop(-1)
        
            # ------------------- Calculating score for Knobs --------------------------------
            # This simply gives a score =1 if the hand contains a jack with the same suit as the turn up card
            
            for card in hand:
                if card.num== 11 and card.suit == deck.turn_up_card.suit:
                    score_knob+=1
        
        # ------------------- Adding score up --------------------------------
        
        # Add Score Up
        hand_score = score_15s + score_straight + score_flush + score_pair + score_knob
        
        # Only print break down of hand score if its the count up
        if count_up:
            scores,names = (score_15s,score_pair,score_straight,score_flush,score_knob),('fifteens','pairs','straights','the flush','his knobs')
            for score,name in zip(scores,names):
                if score > 0:
                    print(f'{score} for {name}')
            
    
    
        return hand_score
    
    def update_game_score(self,save=True):
        # Add hand Score to players score
        self.game_score += self.hand_score
        
        if save:
            self.game_score_hist.append(self.game_score)
            print(f'{self.name}s game score is {self.game_score}')
        else:
            pass
        
    def update_max_hand(self,deck):
        # Check if current hand is best hand yet
        if self.hand_score > self.max_hand_score:
            self.max_hand_score = self.hand_score
            self.max_hand = self.hand.copy()
            self.max_hand.append(deck.turn_up_card)
        else:
            pass
    
    def update_hand_score(self,hand_score,save=True):
        self.hand_score = hand_score
        
        if save:
            self.hand_score_hist.append(self.hand_score)
            print(f'{self.name}s hand score is {self.hand_score}')
        else: 
            pass
     
    def record_box_score(self):
        
        self.box_score_hist.append(self.box_score)
        print(f'{self.name}s box score is {self.box_score}')
        
    def discard_box(self,deck=None):
         
            if deck == None:
                self.box=[]
                print(f'{self.name} discards box')
            
            else:
                for card in self.box:
                    deck.cards.append(card)
                self.box=[]
                print(f'{self.name} discards box to bottom of deck')
                
        
    def choose_hand(self,deck):
        '''
        Choose the highest scoring combination of 4 cards out of 5 and
        discard the unwanted card to the box. 
        
        '''
        
        # Make a copy of the dealt hand
        dealt_hand = self.hand.copy()
        
        # Make list of hand combinations and scores for each combination
        hand_combinations = [comb for comb in combinations(dealt_hand,4)]
        hand_scores = [self.calc_score(hand,deck,count_up=False) for hand in hand_combinations]
        # Find index corresponding to highest scoring hand and pick combination as hand
        best_index = np.argmax(hand_scores)
        self.hand = list(hand_combinations[best_index])
        
        # Find rejected card and 
        rejected_card = list(set(dealt_hand) - set(self.hand.copy()))
        self.box_card = rejected_card

    
class Cribbage():
    
    def __init__(self,players):
        
        self.players = players # List of 'Cribbage_Player' classes
        self.deck = Deck() # Deck class
        self.is_winner = False
        
    def record_ranks(self):
        
        # Create a list of ranks 
        scores = np.array([player.game_score for player in self.players])
        ranks = ss.rankdata(-scores,'min')
      
        # Update player rank
        for (player,rank) in zip(self.players,ranks):
            player.rank = rank
            player.update_rank()
    
    def start_game(self):
        '''
        Method to start a game of Cribbage:
            Lists the players
            Builds and Shuffles the Deck

        '''
        if len(self.players) > 4 or len(self.players) < 2:
            print(f'Cribbage cannot be played with {len(self.players)} players. Number of players must be 2,3 or 4.  ')
            sys.exit()
            
        # List players
        print(f'Cribbage Game starts with {len(self.players)} players. Their names are:')
        for player in self.players:
            print(player.name)
        
        print('\n')
       
        # Buld and shuffle deck
        self.deck.build()
        self.deck.shuffle()
       
        print('Let the game begin!')
        print('\n')
    
    def play_round(self,score_target):
        
        '''
        Play a game of Cribbage
        
        '''
        # -------------------- Dealing -------------------------
        
        # Deal different number of cards depending on number of players
        if len(self.players) == 2:
             # Deal 6 cards to each player
             self.deck.deal(self.players,6)
             
        # If three players, then deal one card into the box
        elif len(self.players) == 3:
            # Deal 5 cards to each player
             self.deck.deal(self.players,5)
             # Deal card into Box
             card_for_box = self.deck.cards.pop(0)
             self.players[-1].box.append(card_for_box)
        else:   
            # Deal 5 cards to each player
             self.deck.deal(self.players,5)
            
        # Print which player has the box
        print(f'{self.players[-1].name} has the box')
        print('\n')
        
        
        # ----------------- Hand Choosing ----------------------------
        
        # Loop through the players and discard unwanted cards to last players box
        for player in self.players:
            player.choose_hand(self.deck)
            self.players[-1].box.extend(player.box_card)
            player.box_card = []
        
        # Turn up card
        self.deck.turn_up()
        
        
        # Check all hands and box have 4 cards before scoring
        num_of_cards_in_hands = [len(player.hand) for player in self.players]
        if any(num != 4 for num in num_of_cards_in_hands) or len(self.players[-1].box) != 4:
            print('Player hands and box do not all have 4 cards!!!!')
            for player in self.players:
                print(f'{player.name} has {len(player.hand)} cards in their hand')
            print(f'{self.players[-1].name}\'s box has {len(self.players[-1].box)} cards')
            sys.exit()
        else:
            pass
        
        
        # --------------- Scoring Player Hands who don't have the box ----------------------
        
        # Loop through players except for last player
        for player in self.players[:-1]:
            
            print(f'{player.name} Turn ')
            score = player.calc_score(player.hand,self.deck,count_up=True) # Calcualte hand score
            player.discard_hand(self.deck) # Discard hand
            player.update_hand_score(score) # Update hand score 
            player.update_max_hand(self.deck) # Update max hand 
            player.update_game_score() # Update game score
            print('\n')
            
            # Check if player has won
            if player.game_score >= score_target:
                return
            else:
                continue
        
        # --------------- Scoring Final Player  ----------------------

        # Calculating hand score for final player
        print(f'{self.players[-1].name} Turn ')
        score = self.players[-1].calc_score(self.players[-1].hand,self.deck,count_up=True)
        self.players[-1].discard_hand(self.deck)
        
        # Calculating box score for final player       
        print(f'{self.players[-1].name} Box ')    
        # Score the box
        self.players[-1].box_score = self.players[-1].calc_score(self.players[-1].box, self.deck, count_up=True)
        self.players[-1].discard_box(self.deck)
        
        # Record Scores for box, hand, game and max hand
        self.players[-1].record_box_score()
        self.players[-1].update_hand_score((score+self.players[-1].box_score))
        self.players[-1].update_max_hand(self.deck)
        self.players[-1].update_game_score()
        
        
    
        # Return turn_up card to deck
        self.deck.return_turn_up()
        
        # Check 52 cards are in the deck at the end of the round
        if len(self.deck.cards) != 52:
            print(f'Wrong number of cards in the deck! There are {len(self.deck.cards)} cards in the deck')
            sys.exit()
        else:
            pass
        
           
    def play_game(self,target_score):
        
        rnd = 1
        # Loop until a player reaches the target score
        while all(player.game_score < target_score for player in self.players):
            print('\n')
            print(f'--------------- Round {rnd} ----------------')
            
            self.play_round(target_score)
            self.record_ranks()
            rnd +=1
            
            # Bring last member of list to the front for next round
            popped = self.players.pop(0)
            self.players.append(popped)
        
        winning_player = self.players[np.argmax([player.game_score for player in self.players])]
        print('\n')
        print(f'{winning_player.name} is the winner with a score of {winning_player.game_score}!')
        print('\n')
            
    def game_plots(self,line_colors):
        
        # Loop through players and supplied line
        fig,[ax1,ax2] = plt.subplots(2,figsize=(6,6))
        for player,line_color in zip(self.players,line_colors):
            
            # Plot score history
            ax1.plot(range(1,len(player.game_score_hist)+1),player.game_score_hist,line_color,label=player.name)
            
            # Plot rank history
            ax2.plot(range(1,len(player.rank_hist)+1),player.rank_hist,line_color,label=player.name)
            
        
        ax1.legend()
        ax1.set_xlabel('Rounds')
        ax1.set_ylabel('Score')
        ax2.set_xlabel('Rounds')
        ax2.set_ylabel('Ranks')
        ax2.invert_yaxis()
        
        
class Snap_Player(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.snap = False
    
    # Methods for declaring Snap and Defeat
    
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
        
        # Initliase counts
        deck_cnt=0
        card_cnt = 0
        
     # Loop whilst there are more than 1 player
        while len(self.players) > 1:
            
            # Loop through the list of players
            for index,player in enumerate(self.players):
                
                player.update_hand_count() # records hand size for post game plots
                
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
                        
                        # Calculate random winner of snap and set that players self.snap = True
                        self.players[random.randint(0,len(self.players)-1)].snap = True
                        deck_cnt=0
                        
                        # Loops through players to declare snap (random num has decided which player has self.snap=True)
                        for player in self.players:
                            player.declare_snap(self.play_deck)
                    
                    # If no snap, then continue
                    else:
                        deck_cnt+=1
            
        # Record player win incase multiple games are played
        self.players[0].update_win()
                
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
