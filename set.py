import random

def display_cards(cards):
    grid = [['O' for x in range(9)] for y in range(9)]
    for card in cards:
        x,y = card.position()
        grid[x][y] = 'X'

    s = ''
    for row in range(9):
        if row % 3 == 0:
            s += '\n'
        for col in range(9):
            if col % 3 == 0:
                s += ' '
            s += grid[row][col]+' '
        s += '\n'

    # '\n'.join([' '.join(x) for x in grid])
    return s

def is_set(cards):
    if len(cards) != 3:
        return False
    return sum(cards, ZERO) == ZERO

def is_ghost_set(cards):
    if len(cards) != 6:
        return False
    return sum([cards[i] - cards[3+i] for i in range(3)], ZERO) == ZERO

class Card:
    def __init__(self, chars):
        for i in chars:
            if i not in range(3):
                raise Exception('Characteristics must be in (0,1,2).')
        self.chars = chars

    def position(self):
        return (self.chars[0]+3*self.chars[2],
                self.chars[1]+3*self.chars[3])

    def __str__(self):
        return display_cards([self])

    def __add__(self, other):
        return Card([(self.chars[x] + other.chars[x])%3 for x in range(4)])

    def __sub__(self, other):
        return Card([(self.chars[x] - other.chars[x])%3 for x in range(4)])

    def __eq__(self, other):
        return False not in [self.chars[x] == other.chars[x] for x in range(4)]

class Game:
    def __init__(self):
        self.deck = self.create_deck()
        self.board = []

    def create_deck(self):
        deck = []
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        deck.append(Card([i,j,k,l]))
        return deck

    def deal(self):
        while len(self.board) != 12:
            card = random.choice(self.deck)
            self.deck.remove(card)
            self.board.append(card)

        print display_cards(self.board)

    def remove(self, cards):
        for card in cards:
            self.board.remove(card)

    def is_showing(self, card):
        return card in self.board

ZERO = Card([0,0,0,0])

def parse_cards(s):
    return [Card([int(i) for i in list(c)]) for c in s.split(':')]

if __name__ == '__main__':
    game = Game()
    game.deal()

    s = raw_input('Do you see a set? ')
    while s != 'EXIT':
        try:
            cards = parse_cards(s)
            if False not in [game.is_showing(c) for c in cards] and is_set(cards):
                game.remove(cards)
                print 'You found a set!'
                game.deal()
        except Exception, e:
            print e
            print 'Please indicate 3 cards. xxxx:xxxx:xxxx'
        s = raw_input('Do you see a set? ')
