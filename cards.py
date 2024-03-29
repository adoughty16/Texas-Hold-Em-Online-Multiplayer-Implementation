from enum import Enum

'''
Card class needs to interface with Card sprite in Graphics
- rather than keep file images and import arcade here, maybe just function with getters and setters
'''
# d = diamonds
# c = clubs
# h = hearts
# s = spades
suit = Enum('suit', ['d','c','h','s'])

class Card:
    
    def __init__(self, suit, value):
        self.suit=suit
        self.value=value
        # Image to use for the sprite when face up (from graphics to interface the two)
        #self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

    def __str__(self):
        return (f'{str(self.value)} of {self.suit_to_str()}')

    def to_dict(self):
        return {"suit": self.suit, "value": self.value}

    def set_suit(self, suit):
        self.suit = suit
    
    def set_value(self, value):
        self.value = value 

    #compare to function
    #if the card passed in is greater than this card, return 1
    #if the card passed in is less than this card, return -1
    #if the card passed in is equal to this card, return 0
    def compareTo(self, this_card):
        if (this_card.value>self.card.value):
            return 1
        if (this_card.value<self.card.value):
            return -1
        if (this_card.value==self.card.value):
            return 0

    #returns integer suit value
    def suit_to_str(self):
        if self.suit == 0:
            return 'Diamonds'
        if self.suit == 1:
            return 'Clubs'
        if self.suit == 2:
            return 'Hearts'
        if self.suit == 3:
            return 'Spades'

    def get_suit(self):
        return self.suit

    def get_suit_for_sprite(self):
        if self.suit == 0:
            return 'Diamonds'
        if self.suit == 1:
            return 'Clubs'
        if self.suit == 2:
            return 'Hearts'
        if self.suit == 3:
            return 'Spades'
        
    def get_value(self):
        return self.value

    def get_value_for_sprite(self):
        if self.value == 1:
            return 'A'
        if self.value > 1 and self.value < 10:
            return self.value
        if self.value > 10:
            if self.value == 11:
                return 'J'
            elif self.value == 12:
                return 'Q'
            elif self.value == 13:
                return 'K'
        else:
            return 'A'
    
    def get_filename(self):
        return f":resources:images/cards/card{self.get_suit_for_sprite()}{self.get_value_for_sprite()}.png"

    # overridden equality operator to compare card objects using == and != (useful in Game_state and maybe other game logic)
    def __eq__(self, other):
        if self.suit == other.suit and self.value == other.value:
            return True
        else:
            return False
    
    # would it help to have a draw function face up and face down? 