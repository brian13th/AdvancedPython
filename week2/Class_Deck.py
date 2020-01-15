import random

class Card():
    """ Κλάσση δημιουργός ενος τραπουλόχαρτου"""
    gr_names = {'s': 'Σπαθί ♣', 'c': 'Μπαστουνι ♠', 'h': 'Κούπα ♥', 'd': 'Καρό ♦',
                'A': 'Άσσος', '2': 'Δύο', '3': 'Τρία', '4': 'Τέσσερα', '5': 'Πέντε', '6': 'Έξι', '7': 'Επτά',
                '8': 'Οκτώ',
                '9': 'Εννιά', 'T': 'Δέκα', 'J': 'Βαλές', 'Q': 'Ντάμα', 'K': 'Ρήγας'}
    the_cards = []
    def __init__(self, value, symbol):
        self.value = value.strip().upper()
        self.type = symbol.strip().lower()
        Card.the_cards.append(self)
    def __str__(self):
        return self.value + self.type
    def detailed_info(self):
        if self.value in Card.gr_names and self.type in Card.gr_names:
            return f'{Card.gr_names[self.value]} {Card.gr_names[self.type]}'
        else:
            return ''
    def is_figure(self):
        if self.value == 'J' or self.value == 'Q' or self.value == 'K':
            return True
        else:
            return False
    def color(self):
        if self.value == 's' or self.value == 'c':
            return 'black'
        else:
            return 'red'

class Deck():
    """ Κλάση που δημιουργεί τράπουλα"""
    symbols = 'shcd'
    values = 'A23456789TJQK'
    def __init__(self):
        self.content = [] # χαρτιά που βρίσκονται στην τράπουλα
        self.pile = [] # χαρτιά που εχουν μοιραστεί
        for s in Deck.symbols:
            for v in Deck.values:
                self.content.append(Card(v,s))
    def shuffle(self):
        random.shuffle(self.content)
    def draw(self):
        if len(self.content) < 1 : return f"empty deck"
        drawn_card = self.content[0]
        self.content = self.content[1:]
        self.pile.append(drawn_card)
        return drawn_card
    def collect(self):
        self.content += self.pile
        self.pile= []
    def __str__(self):
        s = ''
        cnt = 0
        for i in self.content:
            s = s + str(i)+' '
            cnt += 1
            if cnt%13 == 0: s = s+'\n'
        if s[-1] != '\n': s += '\n'
        return s
    def pile_detais(self):
        print(f"Τα φύλλα στο τραπέζι είναι: ")
        [print(p.detailed_info()) for p in self.pile]
