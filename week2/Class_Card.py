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
            return f"Το φύλλο σου είναι {Card.gr_names[self.value]} {Card.gr_names[self.type]}"
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


while True:
    card = input('Δώστε φύλλο (αξία, σύμβολο): ')
    if card == '': break
    if card.count(',') == 1:
        c = Card(*card.split(','))
        for c in Card.the_cards:
            print(c, c.detailed_info())
            print(c.is_figure(), c.color())
            print('\n')