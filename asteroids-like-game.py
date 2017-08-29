# http://www.codeskulptor.org/#user40_D9lSFlF4CX_22.py
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# student added
PLAYER_COUNT = 2
CARDS_INITIAL_DEAL = 2



# initialize some useful global variables
in_play = False
outcome = ""
score = 0
draw_card_back = False


# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        if draw_card_back:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []
        
    def __str__(self):
        output = ""
        if len(self.card_list) > 0:
            for card in self.card_list:
                if len(output) > 0:
                    output = output + " "
                output = output + str(card)

        return "Hand contains " + output
        
        
    def add_card(self, new_card):
        self.card_list.append(new_card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
        ace_here = False
        val_list = []
        for card in self.card_list:
            if card.rank == "A":
                ace_here = True
            val_list.append(VALUES[card.rank])
        if ace_here and sum(val_list) + 10 <= 21:
            return sum(val_list) + 10
        else:
            return sum(val_list)
   
    def draw(self, canvas, pos):
        pass    # draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop()
    
    def __str__(self):
        output = ""
        for ctr0 in range(len(self.cards)):
            if len(output) > 0:
                output = output + " "
            output = output + str(self.cards[ctr0])
        return "Deck contains " + output

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, hands, score
    deck = Deck()
    deck.shuffle()
    hands = []
    # initialize empty hand for two players
    for n0 in range(2):
        hands.append(Hand())
    # deal two cards initially
    for n0 in range(2):
        for hand in hands:
            hand.add_card(deck.deal_card())
    # if game in session player forfeits
    if in_play:
        score -= 1
    in_play = True
    outcome = " ... Hit or Stand"
    print "New Game:"
    print_a_round()

# student added
def print_a_round():
    global outcome
    if not in_play:
        print "Game over ... hit deal to play again."
    for n0 in range(len(hands)):
        if n0 == len(hands) - 1:
            player_label = "Dealer"
        else:
            player_label = "Player" + str(n0)
        print player_label, ":", hands[n0]
        print player_label + " value = ", str(hands[n0].get_value())
        if player_label == "Dealer":
            print outcome
            print "Score = ", score
    print "=============================="

def hit():
    # if the hand is in play, hit the player
    global outcome, hands, in_play, score
    if in_play:
        hands[0].add_card(deck.deal_card())
    # if busted, assign a message to outcome, update in_play and score
    if int(hands[0].get_value()) > 21:
        outcome = " ... Busted, Dealer wins."
        if in_play:
            in_play = False
            score -= 1
    print_a_round()    

    
       
def stand():
    global outcome, hands, in_play, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        while int(hands[1].get_value()) < 17:
            hands[1].add_card(deck.deal_card())
    # assign a message to outcome, update in_play and score
    if int(hands[1].get_value()) > 21:
        outcome = " ... you win, dealer busted!"
        if in_play:
            score += 1
    else:
        if in_play:
            if int(hands[1].get_value()) >= int(hands[0].get_value()):
                outcome = " ... dealer wins."
                if in_play:
                    score -= 1
            else:
                outcome = " ... You Win!"
                if in_play:
                    score += 1
    in_play = False
    print_a_round()

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # CARD_SIZE = (72, 96)
    card_pos = [60, 400]
    for draw0 in range(len(hands[0].card_list)):
        # card = Card("S", "A")
        # card.draw(canvas, [300, 300])
        # card.draw(canvas, card_pos)
        hands[0].card_list[draw0].draw(canvas, card_pos)
        card_pos[0] = card_pos[0] + CARD_SIZE[0] + 8
                       
    card_pos = [60, 100]
    for draw1 in range(len(hands[1].card_list)):
        hands[1].card_list[draw1].draw(canvas, card_pos)
        card_pos[0] = card_pos[0] + CARD_SIZE[0] + 8

    # card_pos = [60, 100]
    # card = Card("H", "A")
    # card.draw(canvas, card_pos)
    
    canvas.draw_text("Blackjack", (20,60), 36, "Black")
    canvas.draw_text("Dealer has " + str(hands[1].get_value()), (20, 240), 36, "Black")
    canvas.draw_text("You have " + str(hands[0].get_value()) + outcome, (20, 540), 36, "Black")
    canvas.draw_text("Player Score:" + str(score), (300, 60), 36, "Black")


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
in_play = False
deal()
frame.start()
