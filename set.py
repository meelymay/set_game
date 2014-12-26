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

def is_set(cards, ghost=False):
    if len(cards) != 3 and (not ghost and len(cards) != 6):
        return False
    return sum(cards, ZERO) == ZERO

def is_ghost_set(cards):
    if len(cards) != 6:
        return False
    return sum([cards[i] - cards[3+i] for i in range(3)], ZERO) == ZERO

def find_set(cards, ghost=False):
    all_cards = set(cards)
    ghosts = []
    for c1 in cards:
        for c2 in cards:
            if c1 == c2:
                continue
            c3 = ZERO - (c1 + c2)
            if c3 in all_cards:
                return [c1, c2, c3]
            if ghost:
                ghosts.append(c3)
    if ghost:
        return find_set(ghosts)
    return None

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

    def compact(self):
        return ''.join([str(i) for i in self.chars])

    def __add__(self, other):
        return Card([(self.chars[x] + other.chars[x])%3 for x in range(4)])

    def __sub__(self, other):
        return Card([(self.chars[x] - other.chars[x])%3 for x in range(4)])

    def __eq__(self, other):
        return False not in [self.chars[x] == other.chars[x] for x in range(4)]

    def __hash__(self):
        return sum([self.chars[i]*10^i for i in range(len(self.chars))])

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

    def deal(self, additional=0):
        i = 0
        while len(self.deck) > 0 and (len(self.board) != 12 or i < additional):
            i += 1
            card = random.choice(self.deck)
            self.deck.remove(card)
            self.board.append(card)
        return i > 0

    def remove(self, cards):
        for card in cards:
            self.board.remove(card)

    def is_showing(self, card):
        return card in self.board

    def has_set(self):
        return find_set(self.board, ghost=True)

    def __str__(self):
        return display_cards(self.board)

ZERO = Card([0,0,0,0])

def parse_cards(s):
    return [Card([int(i) for i in list(c)]) for c in s.split(':')]

if __name__ == '__main__':
    game = Game()

    while True:
        added = game.deal()
        while not game.has_set() and added:
            added = game.deal(additional=3)
        print game
        s = raw_input('Do you see a set? ')

        if s == 'EXIT':
            break
        if s == 'NONE':
            game.has_set()
        try:
            cards = parse_cards(s)
            if False in [game.is_showing(c) for c in cards]:
                raise Exception('Not all of those cards are on the board.')
            if is_set(cards):
                game.remove(cards)
                print 'You found a set!'
            else:
                print "That's not a set; try again."
        except Exception, e:
            print e
            print 'Please indicate 3 cards. xxxx:xxxx:xxxx'

