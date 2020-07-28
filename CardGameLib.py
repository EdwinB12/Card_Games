# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 15:11:06 2020

@author: edwin

Module for playing games of Snap and Cribbage. 

Classes 
-------

Card
    Class representing a playing card
Deck
    Class representing a deck of cards
Player
    Class representing a basic card player
Snap Player
    Class specialised for players playing Snap. Inherits from Player Class
Cribbage Player
    Class specialised for players playing Cribbage. Inherits from Player Class
Snap
    Class governing game of Snap
Cribbage
    Class governing game of Cribbage
"""


import random
import sys
import matplotlib.pyplot as plt
from itertools import combinations
import numpy as np
import scipy.stats as ss



class Card:

    """
    Class for representing a playing Card
    
    Attributes
    ----------
    suit: str
        Suit of the Card: 'Clubs', 'Hearts', 'Spades' or 'Diamonds'
    num: int
        Number represented by the card: Ace, Jack, Queen and King should be 1,11,12,13 respectively. 
    val: int
        Value represented by the card: Picture cards are usually 10 and Ace can be 1 or 11. Automatically set in the Class from the num attribute. 
    face: int or str
        Name of the card: 10 would be a 10 and a 11 would be 'Jack'. Automatically set in the Class from the num attribute. 
    ace_high: Bool  Optional: Default = False
        If True, then Ace is set to a value of 11 and a number of 14 rather than 1 for both. 
        
    Methods
    -------
    show
        Prints a string in the format '{face} of {suit}'
    return_show
        Returns a string in the format '{face} of {suit}'
        
    """
    
    def __init__(self,suit,num,ace_high=False):
        
        """
        
        Parameters
        ----------
        suit: str
            Suit of the Card: 'Clubs', 'Hearts', 'Spades' or 'Diamonds'
        num: int
            Number represented by the card: Ace, Jack, Queen and King should be 1,11,12,13 respectively.
        ace_high: Bool  Optional: Default = False
            If True, then Ace is set to a value of 11 and a number of 14 rather than 1 for both.
        """
        
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
        """
        
        Prints a string describing the card
        
        Prints
        -------
        String in the format '{face} of {suit}'

        """
        
        print (f"{self.face} of {self.suit}")
    
    def return_show(self):
        """
        
        Return a string describing the card

        Returns
        -------
        str
            String in the format '{face} of {suit}'

        """
        
        return (f"{self.face} of {self.suit}")


class Deck:
    
    """
    Class representing a standard deck of playing cards: 52 Cards, 4 suits etc. 
    
    Attributes
    ----------
    cards: list of card objects
        Cards currently in the deck
    turn_up_card: Card Object
        Single turned up card from the deck.
        
    Methods
    -------
    build
        Create a 52 card deck. Card objects are stored as a list in the 'cards' attribute
    show
        Prints a string in the format '{face} of {suit}' for each card in the deck
    shuffle
        Randomly orders the cards
    draw
        Returns card taken from the top of the deck
    count
        Prints a the number of cards in the deck: "The deck has {len(self.cards)} cards left"
    deal
        Deals cards to a given list of players. User can specify how many cards each player recieves or the deal the max number of cards, i.e. Keep dealing until deck runs out. 
    turn_up
        Takes top card from deck and moves to turn_up_card attribute
    return_turn_up
        Moves turn_up_card attribute to the bottom of the deck
        
    """
    
    def __init__(self):
        
        self.cards = [] # List of Cards - To be populated by 'Card' class Objects
        self.turn_up_card = [] # Single turn up card - required for some games
        
        
    def build(self):
        
        """
        Creates a 52 card deck. List of card objects found in 'cards' attribute. 
        """
        
        # Loop Around Suits
        for suit in ['Clubs','Diamonds','Hearts', 'Spades']:
            # Loop around Cards
            for num in range(1,14):
                self.cards.append(Card(suit,num))
        print('Deck built')
                
    def show(self):
        
        """
        Prints a string in the format '{face} of {suit}' for each card in the deck.
        
        """
        
        # Loop through list of cards
        for card in self.cards:
            card.show()
    
    def shuffle(self):
        
        """
        Randomly orders the cards
        """
        
        random.shuffle(self.cards)
        print('Deck shuffled')
        
    def draw(self,draw_size=1):
        
        """
        Returns card taken from the top of the deck. Used by the Player Class. 
        """
        
        for i in range(0,draw_size):
            return self.cards.pop(0)
        
        print(f'{draw_size} cards are drawn from the deck')
        
    def count(self):
        
        """
        Prints a the number of cards in the deck: "The deck has {len(self.cards)} cards left"
        """
        
        print(f"The deck has {len(self.cards)} cards left")
    
        
    def deal(self,players,cards_per_player):
        
        """
        Deals cards to a given list of players. User can specify how many cards each player recieves or the deal the max number of cards, i.e. Keep dealing until deck runs out.
        
        Parameters
        ----------
        players : List containing player objects
            List of players to be dealt cards
        cards_per_player: int or 'max'
            Number of cards to be dealt to each player. Error will be thrown if cards_per_player*len(players) > 52
            'max' will deal all cards in the deck until there are no cards left. Note this does not neccessarily mean each player will have an equal number of cards
        
        """
        
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
        """
        Takes top card from deck and moves to turn_up_card attribute

        """
        
        self.turn_up_card = self.cards.pop(0)
        print('The turn up card is', self.turn_up_card.return_show())
        
        
    def return_turn_up(self):
        """
        Moves turn_up_card attribute to the bottom of the deck

        """
        self.cards.append(self.turn_up_card)
        self.turn_up_card=[]
        print('Turn up card has been returned to the deck')
            

class Player:
    
    """
    Class representing a game player. This class provides the back-bone for more specialised player classes. 
    
    Attributes
    ----------
    hand: List of Card Objects
        Cards currently in the players hand
    name: Str
        Player's Name
    wins: int
        Number of wins the player has over multiple games
    rank: int
        Postion in the game for the current round, i.e. in cribbage, if player has the most points they are rank 1. If they have the 2nd most points, they are 2nd, etc. Not all games will ustilise rank
    rank_hist: List of ints
        History of ranks for each round throughout a game 
        
    Methods
    --------
    play_card
        Play a card from hand to a deck object. 
    draw_hand
        Draw cards from deck to hand
    show_hand
        Prints the contents of the players hand
    discard_hand
        Discard the players hand to a deck or generally discarded
    count_hand
        Prints number of the cards in the player's hand
    update_win
        adds 1 to wins attribute 
    update_rank
        adds rank to rank_hist
    
    """
    
    def __init__(self,name):
        
        """
        Parameters
        ----------
        name: Str
            Player's Name
        """
    
        self.hand=[] # List of Card Objects
        self.name=name # String name of the player
        self.wins = 0 # For keeping track num of wins
        self.rank = 1 # Rank - Used when playing a game
        self.rank_hist = [] # History of the rank
        
    # ------------------------ Card Action Methods ------------------------
    
    def play_card(self,deck):
        """
        Play a card from hand to a deck object. 

        Parameters
        ----------
        deck : Deck Object
            Deck to play the cards to. Often this deck would act as the table where all players play cards too. 

        """
        card_played =[]
        card_played = self.hand.pop(0)
        deck.cards.append(card_played)
        print(self.name, 'plays:', card_played.return_show())
    
    # ------------------------ Hand Action Methods ------------------------

    def draw_hand(self,deck,draw_size=1):
        
        """
        Draw cards from deck to hand
        
        Parameters
        ----------
        deck: Deck Object
            Deck to draw cards from to the players hand
        draw_size: int, default =1
            Number of cards to be drawn from the deck
        """
        
        for i in range(0,draw_size):
            self.hand.append(deck.draw(draw_size))
        
    def show_hand(self):
        
        """
        Prints the contents of the players hand

        """
        
        print(f'{self.name}''s hand contains:')
        # Loop through list of cards
        for card in self.hand:
            card.show()
        
    def discard_hand(self,deck=None):
        
        """
        Discard the players hand to a deck or generally discarded
        
        Parameters
        -----------
        deck: Deck Object, Default is None
            If None,then hand is simply cleared. If deck is specified, then hand will be moved to the deck. 
        """
        
        if deck == None:
            self.hand=[]
            print(f'{self.name} discards hand')
        
        else:
        
            for card in self.hand:
                deck.cards.append(card)
            self.hand=[]
            
            print(f'{self.name} discards hand to bottom of deck')
        
    def count_hand(self):
        
        """
        Prints number of the cards in the player's hand
        """
        
        print(f"{self.name}'s hand has {len(self.hand)} cards")
        return len(self.hand)
    # ------------------ Update record (different metrics) methods -------------------------
        
    def update_win(self):
        """
        Adds 1 to wins attribute
        """
        self.wins+=1
    
    def update_rank(self):
        '''
        Adds rank to rank_hist

        '''
        self.rank_hist.append(self.rank)


class Cribbage_Player(Player):
    
    """
    Class specialised for players playing Cribbage. Inherits from Player Class
    
    Attributes
    ----------
    hand_score: int
        Score the player gets for their current hand
    hand_score_hist: List
        History of hand_scores for each round
    game_score: int
        Total score accumulated throughout the game
    game_score_hist: List
        History of Game scores (only important if multiple games are played). 
    max_hand: List of card objects
        Players max scoring hand of the game
    max_hand_score: int
        The score the max_hand earned
    box_card: Card(s) Object
        Rejected card(s) from hand to be sent to the box
    box: List of Cards
        Box for the round. Only one player in the game will have a box so often this will be an empty list
    box_score: int
        Score the box earns
    box_score_hist: List of int
        History of the box score throughout the game
        
    Methods
    -------
    reset_attribs:
        Resets specific attributes back to initial values
    calc_score:
        Calculates the score earned by a hand or box
    update_game_score:
        Adds hand_score to game_score
    update_max_hand:
        Check if current hand is the max scoring hand of the game so far and if true, save hand to max hand
    update_hand_score:
        Passes given score to players hand_score
    record_box_score:
        Add box_score to box_score_hist
    discard_box:
        Discard box to user defined deck
    choose_hand:
        Chooses highest scoring 4 card combination from hand and sends rejected card(s) to box_card attribute. 
        
    """
    
    def __init__(self,name):
        
        '''
        Parameters
        ----------
        name: str
            Player Name
        '''
        
        # Inherit from Player Class
        super().__init__(name)
        
        # Updating the Score for the 
        self.hand_score = 0 # Score for a single hand
        self.hand_score_hist = [] # History of the players hand scores
        self.game_score=0 # Overall Game Score
        self.game_score_hist = [] #  History of overall game score
        
        self.max_hand = [] # Max scoring hand of the game
        self.max_hand_score = 0 # Max score by a hand in the game 
        
        self.box_card = [] # This is the rejected card that will be sent to the box
        self.box=[] # This is the box hand
        self.box_score = 0
        self.box_score_hist = [] # Box History
        
    def reset_attribs(self):
        
        '''
        Resets specific attributes back to initial values
        '''
        
        self.hand = []
        self.rank = 1 
        self.rank_hist = [] 
        
        self.hand_score = 0 # Score for a single hand
        self.hand_score_hist = [] # History of the players hand scores
        self.game_score=0 # Overall Game Score
        self.game_score_hist= []
        
        self.max_hand = [] # Max scoring hand of the game
        self.max_hand_score = 0 # Max score by a hand in the game 
        self.max_hand_turn_up = [] # Do I Need this? 
        
        self.box_card = [] # This is the rejected card that will be sent to the box
        self.box=[] # This is the box hand
        self.box_score = 0
        self.box_score_hist = [] # Box History
        
    def calc_score(self,hand,deck,count_up):
        
        '''
        Calculates the score earned by a hand or box. Calculate cribbage count up score from 5 cards where 4 cards have been drawn and 1 card is turned up
        15's, straights, flushes, pairs and knobs are seperately calculated and added up for a total score.
        
        Parameters
        ----------
        hand: List of Card Objects
            Can be either a players hand or a box
        deck: Deck Object
            Deck 
        count_up: bool
            If True, then the deck's turn_up_card is counted in the calculation of the score. If False, then turn_up_card is not included. Also points for Knobs is not counted.  '
        
        Return
        -------
        hand_score: int
            Score for the hand
        '''
        
        
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
        
        '''
        Adds hand_score to game_score. game_score is added to history if save=True
        
        Parameters
        ----------
        save: bool, Default: True
            If True, game_score_hist is updated. If False, game_score is not passed to game_score_hist
        '''
        
        # Add hand Score to players score
        self.game_score += self.hand_score
        
        if save:
            self.game_score_hist.append(self.game_score)
            print(f'{self.name}s game score is {self.game_score}')
        else:
            pass
        
    def update_max_hand(self,deck):
        
        '''
        Check if current hand is the max scoring hand of the game so far and if true, save hand to max hand
        
        Parameters
        ----------
        deck: 
            Deck being used
        '''
        
        # Check if current hand is best hand yet
        if self.hand_score > self.max_hand_score:
            self.max_hand_score = self.hand_score
            self.max_hand = self.hand.copy()
            self.max_hand.append(deck.turn_up_card)
        else:
            pass
    
    def update_hand_score(self,hand_score,save=True):
        
        '''
        Passes given score to players hand_score
        
        Parameters
        ----------
        hand_score: int
            Score for the hand
        save: bool, default=True
            if True, hand score is added to hand_score_hist. If False, it is not passed to hist. 
        '''
        
        self.hand_score = hand_score
        
        if save:
            self.hand_score_hist.append(self.hand_score)
            print(f'{self.name}s hand score is {self.hand_score}')
        else: 
            pass
     
    def record_box_score(self):
        
        '''
        '''
        
        self.box_score_hist.append(self.box_score)
        print(f'{self.name}s box score is {self.box_score}')
        
    def discard_box(self,deck=None):
        
        '''
        Discard box to user defined deck
        
        Parameters
        -----------
        deck: Deck Object, Default is None
            If None,then box is simply cleared. If box is specified, then box will be moved to the deck.
        '''
         
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
        
        Parameters
        deck: Deck Object
            deck in use
        
        '''
        
        # Make a copy of the dealt hand
        dealt_hand = self.hand.copy()
        
        # Make list of hand combinations and scores for each combination
        hand_combinations = [comb for comb in combinations(dealt_hand,4)]
        hand_scores = [self.calc_score(hand,deck,count_up=False) for hand in hand_combinations]
        # Find index corresponding to highest scoring hand and pick combination as hand
        best_index = np.argmax(hand_scores)
        self.hand = list(hand_combinations[best_index])
    
        # Find rejected card 
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
            player.reset_attribs() # Reset all attributes 
            print(player.name)
        
        print('\n')
       
        # Buld and shuffle deck
        self.deck = Deck() # Deck class
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
            
        # ----------------- Hand Choosing ----------------------------
        
        # Loop through the players and discard unwanted cards to last players box
        for player in self.players:
            player.choose_hand(self.deck)
            self.players[-1].box.extend(player.box_card)
            player.box_card = []
            print(f'{player.name} has chosen their hand')
        
        # Print which player has the box
        print(f'{self.players[-1].name} has the box')
        
        
        # Turn up card
        self.deck.turn_up()
        print('\n')
        
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
        
        # Record Winning Player win
        winning_player.update_win()
            
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
    
    def plot_win_hist(self):
        
        # Plot win history if multiple games have been played
        fig,ax = plt.subplots(figsize=(6,6))
        for player in self.players:
            ax.scatter(player.name,player.wins)
            
        ax.set_xlabel('Players')
        ax.set_ylabel('Wins')
        ax.set_title('Win Record')
    
        
class Snap_Player(Player):
    
    def __init__(self,name):
        super().__init__(name)
        self.snap = False
        self.hc_hist = [] # For keeping track of hand size throughout a game
    
    def update_hand_count(self):
        self.hc_hist.append(len(self.hand))
    
    
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
        
        self.players = self.players_orig.copy()
        print(f'Snap Game starts with {len(self.players)} players. Their names are:')
        for player in self.players:
            print(player.name)
            player.hand=[] # Reset players hands
            player.hc_hist = []# Reset player hand count history
            
        print('\n')
        
        # Buld, shuffle deck
        self.deck = Deck() # Create new Deck and play deck. 
        self.play_deck = Deck()
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
        
    def plot_hand_count_hist(self,line_colors,title=None):
        
        # Plot win history if multiple games have been played
        fig,ax = plt.subplots(figsize=(6,6))
        for player,line_color in zip(self.players_orig,line_colors):
            ax.plot(range(0,len(player.hc_hist)),player.hc_hist,line_color,label=player.name)        
            
        ax.legend(loc = 'upper left')
        ax.set_xlabel('Turns')
        ax.set_ylabel('Cards in hand')
        ax.set_title(title)
        
    def plot_win_hist(self):
        
        # Plot win history if multiple games have been played
        fig,ax = plt.subplots(figsize=(6,6))
        for player in self.players_orig:
            ax.scatter(player.name,player.wins)
            
        ax.set_xlabel('Players')
        ax.set_ylabel('Wins')
        ax.set_title('Win Record')
