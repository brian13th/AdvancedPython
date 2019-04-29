import Class_Deck as cd

class Player():
    """ ο παίχτης του 31"""
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
        self.my_score = 0
    def __str__(self):
        return self.name
    def plays(self):
        card = self.deck.draw()
        print(f'Ο παίχτης {self.name} τράβηξε: {card.detailed_info()}')
        self.card_value = self.calculate_value(card)
        self.my_score += self.card_value
        self.check_if_exceeded()
        if self.my_score == -1:
            return
        else:
            reply = input(f'Σκορ: {self.my_score} συνεχίζεις (ν/ο): ')
            if not reply or reply.lower() not in 'oο': self.plays()
            else: return
    def calculate_value(self, card):
        if card.value.isdigit(): return int(card.value)
        elif card.value == 'A': return 1
        else: return 10
    def check_if_exceeded(self):
        if self.my_score > 31:
            print('Δυστυχώς κάηκες :-( ')
            self.my_score = -1
class Cpu(Player):
    """ Παίχτης που αποφασίζει μόνος του τις κινήσεις του"""
    def plays(self):
        card = self.deck.draw()
        print(f'Ο Υπολογιστής ({self.name}) τράβηξε: {card.detailed_info()}')
        self.card_value = self.calculate_value(card)
        self.my_score += self.card_value
        self.check_if_exceeded()
        if self.my_score == -1:
            return
        else:
            if self.cpu_strategy():
                print(f'Σκορ: {self.my_score}')
                self.plays()
            else: return
    def cpu_strategy(self):
        return False if self.my_score >= 25 or self.my_score == -1 else True
class Game():
    """ εκκινεί το παιχνίδι, ανακατεύει την τράπουλα, δίνει σειρά στους παίχτες και αποφασίζει ποιος θα παίξει πρώτος"""
    def __init__(self):
        print('Παίζουμε 31')
        self.d = cd.Deck()
        self.d.shuffle()
        self.n_players = self.number_of_players()
        self.players = []
        for i in range(self.n_players):
            if i == 0:
                self.players.append(Cpu('Παίχτης-'+ str(i+1), self.d))
            else:
                self.players.append(Player('Παίχτης-'+ str(i+1), self.d))
        self.show_players()
        self.play_game()

    def number_of_players(self):
        return int(input('Αριθμός παιχτών (2-8): '))
    def show_players(self):
        for p in self.players:
            print(p, end=' ')
    def play_game(self):
        print('\n')
        for p in self.players:
            print(print(50*f'*', f'\nΠαίζει ο παίχτης: {p}'))
            p.plays()
        self.show_winner()
    def show_winner(self):
        print(50*'*')
        print(f'Ο νικητής είναι: ')
        max_score = max(x.my_score for x in self.players)
        if max_score == -1:
            print('Δεν έχουμε νικητή..')
        else:
            winners = [x for x in self.players if x.my_score == max_score]
            for player in winners:
                print(player)
if __name__ == '__main__': Game()