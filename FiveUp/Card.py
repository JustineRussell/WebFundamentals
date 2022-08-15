import arcade

class Card(arcade.Sprite):  
    #Card Sprite

    def __init__(self, suit, value, scale=1):
        #Card Constructor

        #Attributes for suites and values
        self.suit = suit
        self.value = value

        #image to use
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        #Call The Parent
        super().__init__(self.image_file_name,scale,hit_box_algorithm="None")

