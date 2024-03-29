
import arcade
import arcade.gui
import arcade.gui.widgets 
from Game_state import  Game_state
import db_connect
import Player
import deck
import random
import time
from cards import Card 

# Screen title and size
SCREEN_WIDTH = 1424
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Texas Hold'em Poker"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on bottom
START_X = (SCREEN_WIDTH / 2) - 50


# The Y of the top row
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row
MIDDLE_Y = SCREEN_HEIGHT / 2

# the X for player 2, middle row
MIDDLE_X_2 = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# the X for player 4, middle row
MIDDLE_X_4 = MAT_WIDTH + 1125 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# community card mats
MIDDLE_X_COMMUNITYCARDS = MAT_WIDTH + 375 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Face down image
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"




''' CREATE THE WELCOME SCREEN'''
class WelcomeView(arcade.View):


    def __init__(self):
        super().__init__()
        #TODO: We need a way to input player names in this window as well
        self.play_name = None

        # instance variables
        self.selected_players = -1  # Default to -1 player
        self.selected_host = None  # To store "Host" or "Join"
        self.players_chosen = False
        self.host_chosen = False
        self.button_change = False

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Create a vertical BoxGroup to align buttons
        self.host_join_box = arcade.gui.UIBoxLayout()
        self.player_box = arcade.gui.UIBoxLayout()


        ''' CREATING HOST AND JOIN BUTTON '''
        # creating HOST button
        host_button = arcade.gui.UIFlatButton(text="Host Game", width=200)
        host_button.text = "Host Game"
        self.host_join_box.add(host_button.with_space_around(bottom=20))

        # creating JOIN game button
        join_button = arcade.gui.UIFlatButton(text="Join Game", width=200)
        join_button.text = "Join Game"
        self.host_join_box.add(join_button.with_space_around(bottom=20))

        host_button.on_click = self.on_host_click
        join_button.on_click = self.on_join_click

        # for positioning of host join buttons
        self.manager.add(
            # Create a widget to hold the host_join_box widget, that will center the host/join buttons
            arcade.gui.UIAnchorWidget(
                anchor_x="left",
                anchor_y="center_y",
                align_x= (140),
                child=self.host_join_box)
        )

        self.pressed = {
            "font_name": ("calibri", "arial"),
            "font_size": 15,
            "font_color": arcade.color.BLACK,
            "border_width": 2,
            "border_color": None,
            "bg_color": arcade.color.WHITE,

            # used if button is pressed
            "bg_color_pressed": arcade.color.WHITE,
            "border_color_pressed": arcade.color.RED,  # also used when hovered
            "font_color_pressed": arcade.color.RED,
        }

        ''' NUMBER OF PLAYERS BUTTON '''

        # creating 1 player button
        player1_button = arcade.gui.UIFlatButton(text="1 player", width=200)
        player1_button.text = "1 player"
        self.player_box.add(player1_button.with_space_around(bottom=20))

        # creating 2 players button
        player2_button = arcade.gui.UIFlatButton(text="2 players", width=200)
        player2_button.text = "2 players"
        self.player_box.add(player2_button.with_space_around(bottom=20))

        # creating 3 players button
        player3_button = arcade.gui.UIFlatButton(text="3 players", width=200)
        player3_button.text = "3 players"
        self.player_box.add(player3_button.with_space_around(bottom=20))

        # creating 4 players button
        player4_button = arcade.gui.UIFlatButton(text="4 players", width=200)
        player4_button.text = "4 players"
        self.player_box.add(player4_button.with_space_around(bottom=20))

        player1_button.on_click = self.on_1p_click
        player2_button.on_click = self.on_2p_click
        player3_button.on_click = self.on_3p_click
        player4_button.on_click = self.on_4p_click

        # for positioning of number of players
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center",
                align_x= (470),
                align_y= (-68),
                child=self.player_box)
        )


        ''' START BUTTON '''

        #creating START button
        start_button = arcade.gui.UIFlatButton(text="START", width=200)
        start_button.text = "START"
        start_button.on_click = self.on_start_click

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=start_button)
        )



    # These functions will be called everytime the user presses a button
    def on_host_click(self, event):
        self.selected_host = True
        self.host_chosen = True
        self.button_change = True
    def on_join_click(self, event):
        self.selected_host = False
        self.host_chosen = True
        self.button_change = True
    def on_1p_click(self, event):
        self.selected_players = 1
        self.players_chosen = True
        self.button_change = True
    def on_2p_click(self, event):
        self.selected_players = 2
        self.players_chosen = True
        self.button_change = True
    def on_3p_click(self, event):
        self.selected_players = 3
        self.players_chosen = True
        self.button_change = True
    def on_4p_click(self, event):
        self.selected_players = 4
        self.players_chosen = True
        self.button_change = True
    def on_start_click(self, event):
        #if required selections have been made
        if (self.players_chosen) and (self.host_chosen):
            #launch the game
            game_view = GameView(self.selected_players, self.selected_host)
            game_view.setup()
            self.window.show_view(game_view)



    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BROWN)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_update(self, delta_time):
        pass

    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()
        arcade.draw_text("Welcome to Texas Hold'em Poker!", self.window.width / 2, self.window.height - 75,
                         arcade.color.GOLDENROD, font_size=48, anchor_x="center", font_name="Kenney Pixel Square")
        arcade.draw_text("Answer the 2 questions below, then click START !", self.window.width / 2, self.window.height - 150,
                         arcade.color.GAINSBORO, font_size=20, anchor_x="center", font_name="Kenney Pixel Square")
        arcade.draw_text("Do you want to HOST or JOIN the game?",  250 , self.window.height /2 + 100,
                         arcade.color.GOLDENROD, font_size=18, anchor_x="center", font_name="Kenney Mini Square")
        arcade.draw_text("How many people are playing?", 1170, self.window.height / 2 + 100,
                         arcade.color.GOLDENROD, font_size=20, anchor_x="center", font_name="Kenney Mini Square")
        arcade.draw_text("Press 'esc' to quit the game", 720, self.window.height / 2 - 350,
                         arcade.color.GOLDENROD, font_size=20, anchor_x="center", font_name="Kenney Mini Square")
        
        if self.selected_players != -1:
            arcade.draw_text(f'Number of Human Players: {self.selected_players}', 720, self.window.height / 2 - 160,
                         arcade.color.GOLDENROD, font_size=20, anchor_x="center", font_name="Kenney Mini Square")

        if self.selected_host == True:
            arcade.draw_text(f'I am the Host', 715, self.window.height / 2 - 100,
                         arcade.color.GOLDENROD, font_size=20, anchor_x="center", font_name="Kenney Mini Square")
        if self.selected_host == False:
            arcade.draw_text(f'I am not the Host', 715, self.window.height / 2 - 100,
                         arcade.color.GOLDENROD, font_size=20, anchor_x="center", font_name="Kenney Mini Square")


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        pass
        # pass in self.selected_host() and self.selected_players to the next window rather than using game-state
        # so that GameView can access those values and also create its own game-state object

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        # when user presses ESCAPE key, quit program
        if symbol == arcade.key.ESCAPE:
            # quit
            arcade.exit()




''' CREATE THE MAIN GAME '''

class GameView(arcade.View):
    """ Main application class. """

    def __init__(self, selected_players, selected_host):
        self.db = db_connect.init()
        self.game_state = Game_state(self.db, 'doc1')

        self.num_players = selected_players
		#shared cards on table 
        self.community_cards = []
		#list of local player objects
        self.players = [Player.Player() for _ in range(4)]
        self.hands = []
        for i in range(self.num_players):
            #This means that the real players will be the first in the list
            self.players[i].set_computer_player(False)
		#the current betting pot
        self.pot = 0
		#players[] index to track current dealer
        self.dealer = 0
		#players[] index to track the current player (whose turn it is)
		#automatically 3 because in the first round the dealer/smallblind/bigblind players are in 0,1,2
        self.current = 3
		#total call is the maximum value that has been bet in the current round by any player (this helps keep track of
		# the miniumum call values for players who have already put money into the pot for the round. So the call value for
		# a given player is the total_call minus the amount they have already bet this round)
        self.total_call = 10
		#round bets keeps track of the total money bet so far in the current round by each player (organized by index)
        self.round_bets = [0, 0, 0, 0]
		#everyone starts with 1000
        self.stacks = [1000, 1000, 1000, 1000]
		#me is my index in the player list
        self.me = None
		#host is a boolean that tells me if I am the host or not
        self.host = selected_host
		#actives is the indexes of all the players in the round who have not folded and who have not busted out of the game
        self.actives = [0, 1, 2, 3]
        #controls betting rounds
        self.all_called = False
        self.connected = False
        self.flags_not_up = True
        self.waiting_for_host = False
        self.ready = False
        self.bet_value = 0
        self.bet_value_chosen = False
        #keeps on_update from overlapping itself
        self.working = False
        #keeps draw from trying to draw an empty list of cards
        self.dealt = False
        self.draw_sd = False


        
        super().__init__()
        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        arcade.set_background_color(arcade.color.AMAZON)

        # Don't show the mouse cursor
        # self.window.set_mouse_visible(False)

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

        ''' For player decision buttons '''

        # --- BUTTONS: Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager2 = arcade.gui.UIManager()
        self.manager2.enable()

        # Create a horizontal BoxGroup to align buttons
        self.player_decision_box = arcade.gui.UIBoxLayout()


        # creating BET button
        bet_button = arcade.gui.UIFlatButton(text="bet", width=200)
        bet_button.text = "bet"
        self.player_decision_box.add(bet_button.with_space_around(bottom=10))

        # creating CHECK button
        check_button = arcade.gui.UIFlatButton(text="check", width=200)
        check_button.text = "check"
        self.player_decision_box.add(bet_button.with_space_around(bottom=10))

        # creating FOLD button
        fold_button = arcade.gui.UIFlatButton(text="fold", width=200)
        fold_button.text = "fold"
        self.player_decision_box.add(fold_button.with_space_around(bottom=10))

        # creating CALL button
        call_button = arcade.gui.UIFlatButton(text="call", width=200)
        call_button.text = "call"
        self.player_decision_box.add(call_button.with_space_around(bottom=10))

        # creating bet value buttons (increase)
        increase_bet_button = arcade.gui.UIFlatButton(text="increase", width=100)
        increase_bet_button.text = "increase"
        self.player_decision_box.add(increase_bet_button.with_space_around(bottom=10))

        # creating bet value buttons (decrease)
        decrease_bet_button = arcade.gui.UIFlatButton(text="decrease", width=100)
        decrease_bet_button.text = "decrease"
        self.player_decision_box.add(decrease_bet_button.with_space_around(bottom=10))


        bet_button.on_click = self.on_bet_click
        check_button.on_click = self.on_check_click
        fold_button.on_click = self.on_fold_click
        call_button.on_click = self.on_call_click

        increase_bet_button.on_click = self.on_increase_click
        decrease_bet_button.on_click = self.on_decrease_click

        # for positioning of bet, check, fold, call buttons
        self.manager2.add(
            # Create a widget to hold the player_decision_box widget, that will center the bet, check, fold, call buttons
            arcade.gui.UIAnchorWidget(
                anchor_x="center",
                anchor_y="center_y",
                align_y=(-205),
                align_x=(-592),
                child=self.player_decision_box)
        )


    def on_bet_click(self, event):
        self.game_state.set_player_decision('bet', self.db)
        self.game_state.set_bet(self.bet_value, self.db)
        self.game_state.flip_waiting(self.db)
    def on_check_click(self, event):
        # should only do stuff if checking is an option
        if self.game_state.get_minimum_call(self.db) == 0:
            self.game_state.set_player_decision('check', self.db)
            self.game_state.flip_waiting(self.db)
    def on_fold_click(self, event):
        # update game_state from here
        self.game_state.set_player_decision('fold', self.db)
        self.game_state.flip_waiting(self.db)
    def on_call_click(self, event):
        # update game_state from here
        self.game_state.set_player_decision('call', self.db)
        self.game_state.flip_waiting(self.db)

    def on_increase_click(self, event):
        # increase value by 10
        self.bet_value += 10

    def on_decrease_click(self, event):
        # decrease value by 10
        if self.bet_value > 5:
            self.bet_value -= 10




    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # default names for computer/real players
        self.names = [f'Player {num}' for num in range(1, self.num_players+1)]
        for num in range(1, 5-self.num_players):
            self.names.append(f'Computer Player {num}')

        # ---  Create the mats the cards go on

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()


        # Create player 1 (bottom)
        for i in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, BOTTOM_Y
            self.pile_mat_list.append(pile)

        # Create player 2 (left)
        for i in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = MIDDLE_X_2 + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create player 3 (top)
        for i in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # create player 4 (right)
        for i in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = MIDDLE_X_4 + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # create community card mats
        for i in range(5):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = MIDDLE_X_COMMUNITYCARDS + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()
        self.coins = arcade.SpriteList()
        self.total_coins = arcade.SpriteList()


    def on_update(self, delta_time):
        #GAME LOGIC SIMULATES HERE
        if not self.working:
            self.working = True
            self.game_state.download(self.db)
            
            # if I am not the host:
            if not self.host:
                if not self.connected:
                    #check flags on database
                    flag_document = self.db.collection("flags").document("flag_document").get()
                    if flag_document.exists:
                        #grab flags from db
                        flags = flag_document.to_dict()["values"]
                        self.ready = True
                    #if we haven't reserved a spot in the game
                    if not self.waiting_for_host and self.ready:
                        #look through all flags except the confirmation bit at the end until we find an opening
                        for i in range(self.num_players - 1):
                            if flags[i] == 0:
                                #reserve the opening
                                flags[i] = 1
                                #my index in the player list for this game is i + 1
                                #(host is the 0th player)
                                self.me = i + 1
                                #break to only reserve one spot
                                break
                        #update flags on the database
                        self.db.collection("flags").document("flag_document").set({"values": flags})
                        #now we just need to check for the host's confirmation bit
                        self.waiting_for_host = True
                    #if we are awaiting confirmation
                    if self.waiting_for_host and self.ready:
                        #check the confirmation bit
                        if flags[self.num_players - 1] == 1:
                            self.connected = True
                # if it is not my turn:
                    # keep waiting
                # if it is my turn
                    # clickable buttons will appear in the window and the turn logic
                    # will happen from there, including gamestate updates.
                    # so prettymuch still do nothing either way
            #if we are waiting for a guest turn, just do nothing
            elif self.host and not self.connected:
                if self.num_players == 1:
                    self.connected = True
                else:
                    # Needs to establish and confirm connection with guests VIA firestore before game loop
                    #first spots in flags hold 0s for players to flip to 1s when they connect.
                    #last spot is host confirmation bit that host will flip when all player spots are filled
                    if self.flags_not_up:
                        self.flags = [0 for _ in range(self.num_players)]
                        self.db.collection("flags").document("flag_document").set({"values": self.flags})
                        self.flag_document = self.db.collection("flags").document("flag_document").get()
                        self.flags_not_up = False
                        #reserve spot for myself
                        self.me = 0

                    #update local flags from database
                    self.flags = self.flag_document.to_dict()["values"]
                    self.connected = True
                    #for all the flags that  aren't the confirmation bit
                    for i in range(self.num_players - 1):
                        #if any are 0
                        if self.flags[i] == 0:
                            #not everyone is connected yet
                            self.connected = False
                    #if all players have connected
                    if self.connected:
                        #update and upload confirmation bit
                        self.flags[self.num_players - 1] = 1
                        self.db.collection("flags").document("flag_document").set({"values": self.flags})

            elif self.host and not self.game_state.get_waiting_ad() and self.connected:

                if self.game_state.get_round_ad() == 'dealing':
                    # init deck
                    self.deck = deck.Deck()
                    #deal from the deck
                    self.hands = self.deck.deal()
                    for player, hand in zip(self.players, self.hands):
                        player.set_hand(hand)
                    self.game_state.set_player_hands(self.hands, self.db)
                    self.dealt = True

                    #establish dealer/blinds by adding to the pot and removing the values from the players in the blind positions
                    #(blind positions are determined relative to the dealer position)
                    self.pot += 15
                    self.players[(self.dealer + 1) % 4].set_stack(self.players[(self.dealer + 1) % 4].get_stack() - 5)
                    self.round_bets[(self.dealer + 1) % 4] = 5
                    self.players[(self.dealer + 2) % 4].set_stack(self.players[(self.dealer + 2) % 4].get_stack() - 10)
                    self.round_bets[(self.dealer + 2) % 4] = 10
                    
                    self.stacks = [self.players[i].get_stack() for i in range(4)]

                    self.cycled = False
                    self.cycle = 0
                    self.target = len(self.actives)
                    
                    #now reflect those changes in the gamestate
                    self.game_state.set_round_pot(self.pot, self.db)
                    self.game_state.set_player_stacks(self.stacks, self.db)

                # if we are betting
                elif self.game_state.get_round_ad() == 'pre-flop' or 'flop' or 'turn' or 'river':

                    print(f"Player {self.current}'s turn")
                    print(f'Round: {self.game_state.get_round_ad()}')

                    if self.players[self.current].get_player_type():
                        #give the player's turn() function the community cards and it will return a decision
                        choice, value = "call", 0
                        #choice, value = self.players[self.current].turn(self.community_cards, self.game_state, self.db)
                        print(f'Computer player {self.current} decides: {choice}, {value}')
                    else:
                        choice, value = self.game_state.get_player_decision(self.db)
                        print(f'Human player {self.current} decides: {choice}, {value}')
                    #if bet
                    if choice == 'bet':
                        #compute the amount of money this player is putting into the pot:
                        bet_amount = ((self.total_call - self.round_bets[self.current]) + value)
                        #pot goes up by bet amount
                        self.pot += bet_amount
                        #total_call goes up by the bet value
                        self.total_call += value
                        #add the bet_amount to the round_bets for the current player
                        self.round_bets[self.current] += bet_amount
                        #subtract that amount from the player's stack
                        self.players[self.current].set_stack(self.players[self.current].get_stack() - bet_amount)
                        #update local stacks
                        self.stacks[self.current] = self.players[self.current].get_stack()
                        #now reflect those changes in the gamestate
                        self.game_state.set_player_stacks(self.stacks, self.db)
                        self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + bet_amount, self.db)
                        self.game_state.set_bet(value, self.db)
                        self.game_state.set_total_call(self.game_state.get_total_call(self.db) + value, self.db)
                        self.game_state.set_player_decision(choice, self.db)
                        self.game_state.increment_whose_turn(self.db)
                    
                    #if check
                    elif choice == 'check':
                        #basically just skipping their turn
                        self.game_state.increment_whose_turn(self.db)
                    
                    #if fold
                    elif choice == 'fold':
                        #remove their index from actives[]
                        # THIS IS THROWING AN ERROR! 
                        self.actives.remove(self.current)
                        #tell gamestate
                        self.game_state.remove_player(self.current, self.db)

                    # if call
                    elif choice == 'call':
                        print(f'Player {self.current} calls')
                        # add to the pot the call amount (based on the amount below the total_call the current player
                        # has already bet in round_bets)
                        self.pot += (self.total_call - self.round_bets[self.current])
                        #reflect that in the player's stack
                        self.players[self.current].set_stack(self.players[self.current].get_stack() - (self.total_call - self.round_bets[self.current]))
                        #set that players round_bets to the call value
                        self.round_bets[self.current] = self.total_call
                        #update local stacks with the new player stack
                        self.stacks[self.current] = self.players[self.current].get_stack()
                        #reflect the changes in the gamestate
                        self.game_state.set_player_stacks(self.stacks, self.db)
                        self.game_state.set_round_pot(sum(self.round_bets), self.db)
                        self.game_state.set_player_decision(choice, self.db)
                        self.game_state.increment_whose_turn(self.db)
                            
                    self.current = (self.current + 1) % 4
                    while self.current not in self.actives:
                        self.current += 1
                        self.current = self.current % 4
                    self.cycle += 1
                    
                    #if at any point only one player is active
                    if len(self.actives) == 1:
                        #everyone else folded and the last one is the winner
                        #award the pot to the winner
                        self.players[self.actives[0]].set_stack(self.players[self.actives[0]].get_stack() + self.pot)
                        self.stacks[self.actives[0]] = self.players[self.actives[0]].get_stack()
                        #reset the game to dealing values
                        self.round_bets = [0, 0, 0, 0]
                        self.actives = [1, 2, 3, 4] #NOTE: THIS IS A PLACEHOLDER AND WILL NOT WORK AFTER SOMEONE 
                                                    # HAS BUSTED OUT OF THE GAME
                        self.pot = 0
                        self.set_player_stacks(self.stacks)
                        self.game_state.set_total_pot(0, self.db)
                        self.game_state.set_round('dealing', self.db)
                    
                    #if at any point all the round bets of the active players are all equal then everyone has called
                    if self.cycle == self.target:
                        self.cycled = True
                    
                    if self.cycled:
                        self.all_called = True
                        active_bets = []
                        for i in self.actives:
                            active_bets.append(self.round_bets[i])
                        for i in range(1,len(active_bets)):
                            if active_bets[i-1] != active_bets[i]:
                                self.all_called = False
                    
                    if self.all_called:
                        #merge round pot and total pot
                        #also deal more cards
                        #also change round
                        # this would be more efficient if we get_round from the db once and then compare that stored value
                        # DONE 
                        round = self.game_state.get_round_ad()
                        self.game_state.set_total_pot(self.game_state.get_total_pot(self.db) + self.game_state.get_round_pot(self.db), self.db)
                        self.game_state.set_round_pot(0, self.db)
                        if round == 'pre-flop':
                            self.game_state.set_round('flop', self.db)
                            self.community_cards = self.deck.flop()
                            self.game_state.set_community_cards(self.community_cards, self.db)
                            self.cycled = False
                            self.cycle = 0
                            self.target = len(self.actives)
                        elif round == 'flop':
                            self.game_state.set_round('turn', self.db)
                            self.community_cards.append(self.deck.turn())
                            self.game_state.set_community_cards(self.community_cards, self.db)
                            self.cycled = False
                            self.cycle = 0
                            self.target = len(self.actives)
                        elif round == 'turn':
                            self.game_state.set_round('river', self.db)
                            self.community_cards.append(self.deck.turn())
                            self.game_state.set_community_cards(self.community_cards, self.db)
                            self.cycled = False
                            self.cycle = 0
                            self.target = len(self.actives)
                        elif round == 'river':
                            self.game_state.set_round('showdown', self.db)

                        #reset betting/round values
                        self.current = (self.dealer + 3) % 4
                        self.game_state.set_whose_turn(self.current, self.db)
                        self.total_call = 0
                        self.round_bets = [0, 0, 0, 0]
                        self.all_called = False
                
                # need to do this after the betting loop but before the showdown
                if self.game_state.get_round_ad() == "dealing":
                    self.game_state.set_round("pre-flop", self.db)
                
                if self.game_state.get_round(self.db) == 'showdown':

                    print(f'Round: {self.game_state.get_round_ad()}')

                    final_hands = [self.players[idx].possible_hands(self.community_cards) for idx in self.actives]

                    print("---------------------------------------------------------------------------")
                    print("Final hands! ", final_hands)
                    print("---------------------------------------------------------------------------")

                    self.draw_sd = True

                    #award winner stack from pot
                    best_index = max(range(len(final_hands)), key=lambda i: final_hands[i][1])
                    self.players[best_index].set_stack(self.players[best_index].get_stack() + self.pot)
                    self.stacks[best_index] = self.players[best_index].get_stack()
                    self.game_state.set_player_stacks(self.stacks, self.db)

                if self.game_state.get_round(self.db) == 'sleeping':
                    time.sleep(10)

                    #reset values and change the round
                    self.draw_sd = False
                    self.setup()
                    self.community_cards = []
                    self.game_state.clear_community_cards(self.db)
                    self.game_state.clear_player_hands(self.db)
                    self.hands = []
                    self.game_state.set_player_stacks(self.stacks, self.db)
                    self.game_state.set_round('dealing', self.db)
                    self.game_state.set_total_pot(0, self.db)
                    self.game_state.set_round_pot(0, self.db)
                    self.pot = 0
                    self.dealer = (self.dealer + 1) % 4
                    self.current = (self.dealer + 3) % 4
                    self.game_state.set_dealer(self.dealer, self.db)
                    self.game_state.set_whose_turn(self.current + 1, self.db)
                    self.total_call = 10
                    self.round_bets = [0, 0, 0, 0]
                    self.actives = [0, 1, 2, 3]
                
                if self.game_state.get_round_ad() == "showdown":
                    self.game_state.set_round("sleeping", self.db)
        
                #num_busts = 0
                #for stack in self.stacks:
                #	if stack == 0:
                #		num_busts += 1
                #if num_busts == 3:
                    #Display some kind of winner screen
                print("current player: ",self.current)
                print("whose turn in db: ", self.game_state.get_whose_turn_ad())
                print("actives:",self.actives)
                print('-------------------')
                if not self.players[self.current].get_player_type():
                        self.game_state.set_waiting(True, self.db)
                else:
                    self.game_state.set_waiting(False, self.db)
                
                if self.game_state.get_round_ad() == 'dealing':
                    self.game_state.set_waiting(False, self.db)
            self.working = False
                

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        pass


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        pass

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        pass

    def draw_community(self, flop):
        position_x = MIDDLE_X_COMMUNITYCARDS
        position_y = MIDDLE_Y
        # 0, 1, 2 need to be at middle_x - 2*mat_width, middle_x - 1*mat_width, middle_x - 0*mat_width
        for i in range(len(flop)):
            card_arc = Card_arcade(flop[i], True)
            card_arc.position = position_x + (i)*(X_SPACING), position_y
            self.card_list.append(card_arc)

    def draw_turn_round(self, card):
        card_arc = Card_arcade(card, True)
        card_arc.position = MIDDLE_X_COMMUNITYCARDS + 3*X_SPACING, MIDDLE_Y
        self.card_list.append(card_arc)

    def draw_river_round(self, card):
        card_arc = Card_arcade(card, True)
        card_arc.position = MIDDLE_X_COMMUNITYCARDS + 4*X_SPACING, MIDDLE_Y
        self.card_list.append(card_arc)

    def draw_deal(self, hands):
        # for every hand (1-4) 
        # should this somehow connect to our list of cards ? 
        position_x = [START_X, MIDDLE_X_2, START_X, MIDDLE_X_4]
        position_y = [BOTTOM_Y, MIDDLE_Y, TOP_Y, MIDDLE_Y]
        self.me = 0
        up = True
        for i in range(len(hands)):
            # for every card 
            for j in range(len(hands[i])):
                # hands[i][j] is a Card object
                if i != self.me:
                    up = False
                card_arc = Card_arcade(hands[i][j], up)
                card_arc.position = position_x[i] + j*X_SPACING, position_y[i]
                # the way the superconstructor is called after the filename makes this difficult to change 
                self.card_list.append(card_arc)

    def draw_showdown(self, hands):
        position_x = [START_X, MIDDLE_X_2, START_X, MIDDLE_X_4]
        position_y = [BOTTOM_Y, MIDDLE_Y, TOP_Y, MIDDLE_Y]
        up = True
        for i in range(len(hands)):
            # for every card 
            for j in range(len(hands[i])):
                # hands[i][j] is a Card object
                card_arc = Card_arcade(hands[i][j], up)
                card_arc.position = position_x[i] + j*X_SPACING, position_y[i]
                # the way the superconstructor is called after the filename makes this difficult to change 
                self.card_list.append(card_arc)

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()
        self.manager2.draw()
        # dependning on game logic and where game_state updates, download may need to be called before drawing 
        #self.game_state.download_wph(self.db)

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # draw the cards - certain things like hands will not need to be accessed every time 
        if self.dealt:
            self.draw_deal(self.hands)
        # technically after flop the three ccs should be stored locally and can be accessed that way 
        comm_cards = self.community_cards 
        #comm_cards = self.game_state.get_community_cards_ad()
        if len(comm_cards) == 3:
            self.draw_community(comm_cards)
        elif len(comm_cards) == 4:
            self.draw_community([comm_cards[0], comm_cards[1], comm_cards[2]])
            self.draw_turn_round(comm_cards[3])
        elif len(comm_cards) == 5:
            self.draw_community([comm_cards[0], comm_cards[1], comm_cards[2]])
            self.draw_turn_round(comm_cards[3])
            self.draw_river_round(comm_cards[4])

        #if self.game_state.get_round_ad() == "showdown":
        if self.draw_sd:
            self.draw_showdown(self.hands)
        
        self.card_list.draw()

        bet_to_draw = self.game_state.get_bet_ad() + self.bet_value
        # draw bet value word
        arcade.draw_text("Bet Value:", MIDDLE_X_2 + 175, BOTTOM_Y + 10, arcade.color.WHITE, font_size=14, anchor_x="center", anchor_y="center")
        # draw bet value
        arcade.draw_text(str(bet_to_draw), MIDDLE_X_2 + 175, BOTTOM_Y - 22, arcade.color.WHITE, font_size=24, anchor_x="center", anchor_y="center")

        # draw player names (and gray for those that are inactive) 
        self.actives = self.game_state.get_actives_ad()
        # short cut: draw them all in gray, then draw over them in white! 

        # player "2" is actually index 1 since indexing starts at 0 
        arcade.draw_text(f'{"Round bet"} : {self.round_bets[1]}', MIDDLE_X_2 + 50, SCREEN_HEIGHT / 2 + (MAT_HEIGHT/2) + 50 , arcade.color.GRAY, font_size=15, anchor_x="center")
        # player "4" is actually index 3 
        arcade.draw_text(f'{"Round bet"} : {self.round_bets[3]}', MIDDLE_X_4 - 50, SCREEN_HEIGHT / 2 + (MAT_HEIGHT/2) + 50 , arcade.color.GRAY, font_size=15, anchor_x="center")
        # player "1" is 0 - whatever is drawn on the bottom should be the current player 
        arcade.draw_text(f'{"Round bet"} : {self.round_bets[0]}', SCREEN_WIDTH / 2, MAT_HEIGHT + 50 , arcade.color.GRAY, font_size=15, anchor_x="center")
        # player "3" is actually index 2 
        arcade.draw_text(f'{"Round bet"} : {self.round_bets[2]}', SCREEN_WIDTH / 2, SCREEN_HEIGHT - MAT_HEIGHT -  55 , arcade.color.GRAY, font_size=15, anchor_x="center")

        for index in self.actives:
            if index == 0:
                arcade.draw_text(f'{"Round bet"} : {self.round_bets[0]}', SCREEN_WIDTH / 2, MAT_HEIGHT + 50 , arcade.color.WHITE, font_size=15, anchor_x="center")
            elif index == 1:
                arcade.draw_text(f'{"Round bet"} : {self.round_bets[1]}', MIDDLE_X_2 + 50, SCREEN_HEIGHT / 2 + (MAT_HEIGHT/2) + 50 , arcade.color.WHITE, font_size=15, anchor_x="center")
            elif index == 2:
                arcade.draw_text(f'{"Round bet"} : {self.round_bets[2]}', SCREEN_WIDTH / 2, SCREEN_HEIGHT - MAT_HEIGHT -  55 , arcade.color.WHITE, font_size=15, anchor_x="center")
            elif index == 3:
                arcade.draw_text(f'{"Round bet"} : {self.round_bets[3]}', MIDDLE_X_4 - 50, SCREEN_HEIGHT / 2 + (MAT_HEIGHT/2) + 50 , arcade.color.WHITE, font_size=15, anchor_x="center")


            arcade.draw_text(f'{self.names[1-1]} : {self.stacks[0]}', SCREEN_WIDTH / 2, MAT_HEIGHT + 70 , arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(f'{self.names[2-1]} : {self.stacks[1]}', MIDDLE_X_2 + 80, SCREEN_HEIGHT / 2 + (MAT_HEIGHT/2) + 70 , arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(f'{self.names[3-1]} : {self.stacks[2]}', SCREEN_WIDTH / 2, SCREEN_HEIGHT - MAT_HEIGHT -  35 , arcade.color.BLACK, font_size=20, anchor_x="center")
            arcade.draw_text(f'{self.names[4-1]} : {self.stacks[3]}', MIDDLE_X_4 - 50, SCREEN_HEIGHT / 2 + (MAT_HEIGHT/2) + 70 , arcade.color.BLACK, font_size=20, anchor_x="center")


        #NOTE! To draw the table from this player's perspective, self.me holds the correct index in the player list.
        #It should draw the 'me'th player on the bottom, and then go clockwise from there (will need to mod by 4)

        # self.me is bottom ((self.me + 1) % 4) is middle left ((self.me + 2) % 4) is top and ((self.me + 3) % 4) is middle right 
        
        # who the dealer is 
        self.dealer = self.game_state.get_dealer_ad() 
        if self.dealer == 0:
            arcade.draw_circle_filled((SCREEN_WIDTH/2)-(MAT_WIDTH) - 25, MAT_HEIGHT + 25, 15, arcade.color.RED)
            arcade.draw_circle_filled((SCREEN_WIDTH/2)-(MAT_WIDTH) - 25, MAT_HEIGHT + 25, 12, arcade.color.WHITE)
            arcade.draw_text('D', (SCREEN_WIDTH/2)-(MAT_WIDTH) - 30, MAT_HEIGHT + 20, arcade.color.RED, 11)
        elif self.dealer == 1:
            arcade.draw_circle_filled((MIDDLE_X_2)+ (MAT_WIDTH) + 25, (SCREEN_HEIGHT/2) - (MAT_HEIGHT/2) - 25, 15, arcade.color.RED)
            arcade.draw_circle_filled((MIDDLE_X_2)+ (MAT_WIDTH) + 25, (SCREEN_HEIGHT/2) - (MAT_HEIGHT/2) - 25, 12, arcade.color.WHITE)
            arcade.draw_text('D', (MIDDLE_X_2)+ (MAT_WIDTH) + 20, (SCREEN_HEIGHT/2) - (MAT_HEIGHT/2) - 30, arcade.color.RED, 11)
        elif self.dealer == 2:
            arcade.draw_circle_filled((SCREEN_WIDTH/2)-(MAT_WIDTH) - 25, SCREEN_HEIGHT - MAT_HEIGHT -  25, 15, arcade.color.RED)
            arcade.draw_circle_filled((SCREEN_WIDTH/2)-(MAT_WIDTH) - 25, SCREEN_HEIGHT - MAT_HEIGHT -  25, 12, arcade.color.WHITE)
            arcade.draw_text('D',(SCREEN_WIDTH/2)-(MAT_WIDTH) - 30, SCREEN_HEIGHT - MAT_HEIGHT -  30, arcade.color.RED, 11)

        else:
            arcade.draw_circle_filled((MIDDLE_X_4)-(MAT_WIDTH) - 25, (SCREEN_HEIGHT/2) - (MAT_HEIGHT/2) - 25, 15, arcade.color.RED)
            arcade.draw_circle_filled((MIDDLE_X_4)-(MAT_WIDTH) - 25, (SCREEN_HEIGHT/2) - (MAT_HEIGHT/2) - 25, 12, arcade.color.WHITE)
            arcade.draw_text('D', (MIDDLE_X_4)-(MAT_WIDTH) - 30, (SCREEN_HEIGHT/2) - (MAT_HEIGHT/2) - 30, arcade.color.RED, 11)
        
        # arrow for whose_turn and minimum_call
        arrow_to = (self.game_state.get_whose_turn_ad() - 1) % 4
        arrow_amount = self.game_state.get_minimum_call_ad()
        self.draw_turn_arrow(arrow_to, arrow_amount) 

        # round_pot
        round_pot = self.game_state.get_round_pot_ad() 
        arcade.draw_text(f'Round pot: {round_pot}', MIDDLE_X_COMMUNITYCARDS + MAT_WIDTH/2, MIDDLE_Y - (MAT_HEIGHT / 2) - 30,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        self.round_coins()
        # total pot 
        total_pot = self.game_state.get_total_pot_ad()
        arcade.draw_text(f'Total pot: {total_pot}', MIDDLE_X_COMMUNITYCARDS + 3*MAT_WIDTH, MIDDLE_Y - (MAT_HEIGHT / 2) - 30,
                    arcade.color.WHITE, font_size=15, anchor_x="center")
        self.total_pot_coins(total_pot)
        self.coins.draw()
        self.total_coins.draw()
    
    # function to draw coin objects depending on how much the round pot is 
    def round_coins(self):
        for coin in self.coins:
            self.coins.remove(coin)
        if self.pot > 0:
            # draw one coin 
            coin_1 = Coin()
            coin_1.position = MIDDLE_X_COMMUNITYCARDS + 1.5*MAT_WIDTH, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.coins.append(coin_1)
        if self.pot > 100:
            # draw two coins
            coin_2 = Coin()
            coin_2.position = MIDDLE_X_COMMUNITYCARDS + 1.5*MAT_WIDTH + 14, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.coins.append(coin_2)
        if self.pot > 500:
            coin_3 = Coin()
            coin_3.position = MIDDLE_X_COMMUNITYCARDS + 1.5*MAT_WIDTH + 14, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.coins.append(coin_3)
        else:
            pass

    # function to draw coins next to total pot amount display depending on amount 
    def total_pot_coins(self, total):
        for coin in self.total_coins:
            self.total_coins.remove(coin)
        if total > 700:
            coin_8 = Coin_t()
            coin_8.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 40, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_8)
        if total > 600:
            coin_7 = Coin_t()
            coin_7.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 35, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_7)
        if total > 500:
            coin_6 = Coin_t()
            coin_6.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 30, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_6)
        if total > 400:
            coin_5 = Coin_t()
            coin_5.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 25, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_5)
        if total > 300:
            coin_4 = Coin_t()
            coin_4.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 20, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_4)
        if total > 200:
            coin_3 = Coin_t()
            coin_3.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 15, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_3)
        if total > 100:
            # draw two coins
            coin_2 = Coin_t()
            coin_2.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH + 5, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_2)
        if total > 0:
            # draw one coin 
            coin_1 = Coin_t()
            coin_1.position = MIDDLE_X_COMMUNITYCARDS + 4*MAT_WIDTH, MIDDLE_Y - (MAT_HEIGHT/2) - 25
            self.total_coins.append(coin_1)
        else:
            pass

    # draws turn arrow for graphics 
    def draw_turn_arrow(self, to, amount):
        if to == 0:
            start_x = MIDDLE_X_4 - MAT_WIDTH - 65
            start_y = (SCREEN_HEIGHT / 2)
            end_x = (SCREEN_WIDTH / 2) + MAT_WIDTH + 65
            end_y = MAT_HEIGHT/2
        if to == 1:
            start_x = (SCREEN_WIDTH / 2) - MAT_WIDTH - 65
            start_y = MAT_HEIGHT/2
            end_x = MIDDLE_X_2 + MAT_WIDTH + X_SPACING
            end_y = (SCREEN_HEIGHT / 2)
        if to == 2:
            start_x = MIDDLE_X_2 + MAT_WIDTH + X_SPACING
            start_y = (SCREEN_HEIGHT / 2)
            end_x = (SCREEN_WIDTH / 2) - MAT_WIDTH - 65
            end_y = SCREEN_HEIGHT - (MAT_HEIGHT/2)
        if to == 3:
            start_x = (SCREEN_WIDTH / 2) + MAT_WIDTH + 65
            start_y = SCREEN_HEIGHT - (MAT_HEIGHT/2)
            end_x = MIDDLE_X_4 - MAT_WIDTH - 65
            end_y = (SCREEN_HEIGHT / 2)
        rise = end_y - start_y
        run = end_x - start_x 
        #adding triangle to line 
        arcade.draw_line(start_x, start_y, end_x, end_y, arcade.color.WHITE, 3)
        point_list = ((end_x + 0.03*run, end_y + 0.03*rise),
              (end_x + 0.03*rise, end_y - 0.03*run),
              (end_x - 0.03*rise, end_y + 0.03*run))
        arcade.draw_polygon_filled(point_list, arcade.color.WHITE)
        arcade.draw_text(f'{amount}', start_x + ((end_x - start_x) /2), start_y + 1.5*((end_y - start_y)/2), arcade.color.WHITE, 15) 

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        # when user presses ESCAPE key, quit program
        if symbol == arcade.key.ESCAPE:
            # quit
            arcade.exit()

class Card_arcade(arcade.Sprite):
    """ Card sprite """

    def __init__(self, card, up, scale=CARD_SCALE):
        """ Card constructor """

        # Attributes for suit and value (when converting to external Card class these are already included)
        self.suit = card.get_suit_for_sprite()
        self.value = card.get_value_for_sprite()
        # Image to use for the sprite when face up
        if up:
            self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        else:
            self.image_file_name = FACE_DOWN_IMAGE

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")

# classes of coins and total coins to display on graphics 
class Coin(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/items/gold_2.png", 0.5, hit_box_algorithm="None")

class Coin_t(arcade.Sprite):
    def __init__(self):
        super().__init__(":resources:images/items/gold_3.png", 0.5, hit_box_algorithm="None")

# add parameters to main: num_players, host, game_state, ready, lock
def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, update_rate = 1)
    start_view = WelcomeView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()

