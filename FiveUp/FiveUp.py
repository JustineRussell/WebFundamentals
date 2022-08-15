#Imports
import arcade
import random
from Card import Card
from screeninfo import get_monitors


#Screen title and size
#Get Monitor Size
for m in get_monitors():
    MONITOR_HEIGHT = m.height
    MONITOR_WIDTH = m.width
#Set Screen Size

SCREEN_HEIGHT = MONITOR_HEIGHT * 0.5
SCREEN_WIDTH = MONITOR_WIDTH * 0.5
SCREEN_TITLE = "Five Up Five Down"

#Card Specs

#Constants for scaling
CARD_SCALE = 0.6
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE
#if we fan out cards how far apart
CARD_VERTICAL_OFFSETT = CARD_HEIGHT * CARD_SCALE * 0.3
#constants that represent "what pile is what" for the game
PILE_COUNT = 13
BOTTOM_FACE_DOWN_PILE = 0
BOTTOM_FACE_UP_PILE = 1 
PLAY_PILE_1 = 2
PLAY_PILE_2 = 3
PLAY_PILE_3 = 4
PLAY_PILE_4 = 5
PLAY_PILE_5 = 6
PLAY_PILE_6 = 7
PLAY_PILE_7 = 8
TOP_PILE_1 = 9
TOP_PILE_2 = 10
TOP_PILE_3 = 11
TOP_PILE_4 = 12
#Playmat size
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

#Mat Margins
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

#Y bottom of the row
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

#Start of X
START_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


#Position of cardpiles
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

class FiveUpFiveDown(arcade.Window):
    #initial setup
    def __init__(self):
        super().__init__(SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE)
        self.card_list = None
        arcade.set_background_color(arcade.color.AMAZON)

        #List of cards being dragged with mouse
        self.held_cards = None

        #Previous location to reset if illegal card move
        self.held_cards_original_position = None

        #Pile List
        self.pile_mat_list = None

        #create a list of list that holds each pile of cards
        self.piles = None
    def setup(self):
        #Setup game here
        #List of cards that are being dragged
        self.held_cards = []
        #Previous location to reset if illegal card move
        self.held_cards_original_position = []
        #Create the pile mats
        #Sprite List that all the cards lay on
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        #Make 7 piles
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i  * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i  * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        #Sprite list of all cards no matter where they are
        self.card_list = arcade.SpriteList()
        #Loop through values and suits
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit,card_value,CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)
        pass
        #Shuffle Cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1,pos2)
        #Create the card slots for the ace and main piles
    def on_draw(self):
        self.clear()
        self.pile_mat_list.draw()
        self.card_list.draw()
            
    def pull_to_top(self, card: arcade.Sprite):
        #Pull cards to top in rendering order
        self.card_list.remove(card)
        self.card_list.append(card)
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        #Get list of cards we've clicked
        cards = arcade.get_sprites_at_point((x,y),self.card_list)
        if len(cards) > 0:
            #Get Top Card
            primary_card = cards[-1]
            #All Other Cases grab cards 
            self.held_cards = [primary_card]
            #Save held position
            self.held_cards_original_position = [self.held_cards[0].position]
            #Put on top in drawing order
            self.pull_to_top(self.held_cards[0])
        pass
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        #if we have no cards do nothing
        if len(self.held_cards) == 0:
            return
        #Find closest pile, just in case we are in contact with more than one
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)
        reset_position = True

        #See if we are in contact with the closet card pile
        
        if arcade.check_for_collision(self.held_cards[0], pile):
            #For each card held move it to that pile
            for i, dropped_card in enumerate(self.held_cards):
                dropped_card.position = pile.center_x, pile.center_y
                #Success don't reset position
                reset_position = False
                #Release on top of file?
                if reset_position: 
                    for pile_index, card in enumerate(self.held_cards):
                        card.position = self.held_cards_original_position[pile_index]
        #We are no longer holding cards
        self.held_cards = []
        pass
    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        #If we are holding cards move with mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy
        pass

def main():
        window = FiveUpFiveDown()
        window.setup()
        arcade.run()

if __name__ == "__main__":
    main()
    