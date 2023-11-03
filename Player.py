import cards
import random
from enum import Enum
from collections import Counter


class HandStrength(Enum):
    DEFAULT = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


class Player:
    def __init__(self):
        self.name = None
        self.hand = []
        self.stack = 0
        self.is_computer_player = True  # defaults to computer player
        self.showdown = []
        self.handStrength = HandStrength.DEFAULT

    def get_name(self):
        return self.name

    def get_hand(self):
        return self.hand

    def get_stack(self):
        return self.stack

    def get_player_type(self):
        return self.is_computer_player

    def set_stack(self, stack):
        self.stack = stack

    def set_name(self, name):
        self.name = name

    def set_hand(self, hand):
        self.hand = hand

    def set_computer_player(self, boolean_value):
        self.is_computer_player = boolean_value

    def turn(self, community_cards):
        # return decision (bet, check, fold)
        decision = self.make_decision(community_cards)
        return decision

    def evaluate_strength(self, community_cards):
        # takes community_cards, combines with self.hand, returns strength
        combined_cards = self.hand + community_cards
        hand_strength = self.calculate_strength(combined_cards)
        return hand_strength

    def evaluate_hand(self, community_cards):
        #  takes in community_cards, combines them with self.hand, and returns the ENUM for the player's hand.

        combined_cards = self.hand + community_cards
        hand_type = self.get_hand_type(combined_cards)
        return hand_type

    def make_decision(self, community_cards):
        # could use evaluate_strength and evaluate_hand as part of decision
        # random decision for now
        # EDIT needs to return a bet value if decision is bet. This can just be zero if the decision is not bet
        decisions = ["bet", "check", "fold"]
        choice = random.choice(decisions)
        if choice == "bet":
            bet_value = 5 * random.randint(1, 10)  # THIS IS A PLACEHOLDER
        else:
            bet_value = 0

        return choice, bet_value

    def calculate_strength(self, cards):
        # Implement hand strength evaluation
        # Sort the cards by rank (e.g., 2, 3, 4, ..., A)
        sorted_cards = sorted(cards, key=lambda card: Card.RANK_ORDER.index(card.rank))
        counts = Counter(card.rank for card in sorted_cards)

        if self.is_royal_flush(sorted_cards):
            return HandStrength.ROYAL_FLUSH
        elif self.is_straight_flush(sorted_cards):
            return HandStrength.STRAIGHT_FLUSH
        elif self.is_four_of_a_kind(counts):
            return HandStrength.FOUR_OF_A_KIND
        elif self.is_full_house(counts):
            return HandStrength.FULL_HOUSE
        elif self.is_flush(sorted_cards):
            return HandStrength.FLUSH
        elif self.is_straight(sorted_cards):
            return HandStrength.STRAIGHT
        elif self.is_three_of_a_kind(counts):
            return HandStrength.THREE_OF_A_KIND
        elif self.is_two_pair(counts):
            return HandStrength.TWO_PAIR
        elif self.is_one_pair(counts):
            return HandStrength.ONE_PAIR
        else:
            return HandStrength.HIGH_CARD

    def get_hand_type(self, cards):
        # Implement hand type evaluation logic
        # Return the appropriate ENUM from HandStrength
        pass

    def flushing(self,cards):

        flushing = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        flushes = 0
        flush = []

        for i in cards:
            flushing[cards[i].get_value()].append(cards[i])

        for e, i in enumerate(flushing):
            if len(i) == 0:
                pass
            if (len(flushing[e+1]>0)):
                flush.append[flushing[i[0]]]




    def matching(self, cards):
        # memory for matching cards, stores a list of a list of cards
        matching = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        # memory for number of pairs
        pairs = 0
        pair_values = []

        # iterate through given cards and sort them by adding them to matching[[],[],...[] by index of value
        for i in cards:
            matching[cards[i].get_value()].append(cards[i])

        # iterate through matching
        for e, i in enumerate(matching):

            # if the list of cards sorted by index contains
            if len(i) == 4:

                #set this players handstrength to four of a kind and set their showdown cards to these cards
                self.handStrength = HandStrength.FOUR_OF_A_KIND
                self.showdown = i
                return HandStrength.FOUR_OF_A_KIND

            if len(i) == 3:

                #same as before
                self.handStrength = HandStrength.THREE_OF_A_KIND
                self.showdown = i
                return HandStrength.THREE_OF_A_KIND

            if len(i) == 2:

                #if there is a pair, add it to a pair counter and store the value for later
                pairs = +1
                pair_values.append(e)

        if pairs == 1:
            self.handStrength = HandStrength.ONE_PAIR
            #set the showdown cards to the pair by their index as stored in pair_values[]
            self.showdown = matching[pair_values.pop()]
            return HandStrength.ONE_PAIR

        if pairs == 2:
            self.handStrength = HandStrength.TWO_PAIR
            #same as above but pop from pair values one more time
            self.showdown = matching[pair_values.pop()]
            self.showdown.append(matching[pair_values.pop()])
            return HandStrength.TWO_PAIR

