import os, random, shelve

class Contact():
    """κάθε επαφή είναι όνομα και τηλέφωνο"""
    theContacts = {}
    def __init__(self, name, number):
        self.name = name.strip()
        self.number = number.strip()
        Contact.theContacts[self.name]=self
    def __repr__(self):
        return self.name + ' : ' + self.number
    def list_contacts():
        for c in sorted(Contact.theContacts):
            print(Contact.theContacts[c])

class Persistant():
    """κλάση μόνιμης αποθήκευσης των αντικειμένων της Contact"""
    def __init__(self):
        self.db = 'contacts'
    def store(self):
        if os.path.isfile(self.db): os.remove(self.db)
        with shelve.open(self.db) as db:
            for c, contact in Contact.theContacts.items():
                db[c] = contact
    def retrive(self):
        with shelve.open(self.db) as db:
            for k in db:
                Contact(db[k].name, db[k].number)

class Main():
    """κλάση διαχείρισης επαφών - δημιουργία - διαγραφή"""
    def __init__(self):
        persist = Persistant()
        persist.retrive()
        while True:
            command = input(f'\nΕπαφές {len(Contact.theContacts)}\nΕισαγωγή[+] Διαγραφή[-] Επισκόπηση[?] Έξοδος[Enter]')
            if command == '': break
            elif command == "+":
                contact_details = input('Εισάγετε όνομα : τηλέφωνο ή πλήθος επαφών αυτόματης εισαγωγής ')
                if ':' in contact_details:
                    try: Contact(*contact_details.split(':'))
                    except IndexError: print('Σφάλμα εισαγωγής επαφής')
                elif contact_details.isdigit():
                    if int(contact_details) < 500:
                        self.create_contacts(int(contact_details))
                    else:  print('Σφάλμα: Δώσατε πολύ μεγάλο αριθμό επαφών..')
                else: print('Προσοχή! Δώστε όνομα (:) τηλέφωνο')
            elif command == "?":
                Contact.list_contacts()
            elif command == "-":
                name = input('Διαγραφή όνομα ')
                try:
                    del Contact.theContacts[name.strip()]
                except KeyError:
                    print('Δεν υπάρχει η επαφή που ζητήσατε')
        persist.store()
    def create_contacts(self, size):
        """Δημιουργεί τυχαίο δείγμα επαφών και τηλεφώνων"""
        dir = './data'
        act_names_files = [os.path.join(dir,x) for x in ('gr_actresses.txt', 'gr_actors.txt')]
        names = []
        for f in act_names_files:
            with open(f, 'r', encoding='utf-8') as fin:
                for name in fin:
                    if len(name) > 2:
                        if len(name.split()) > 1:
                            names.append(name.strip())
        if size < len(names):
            contact_names = random.sample(names, size)
        else:
            contact_names = names
        for contact in contact_names:
            Contact(contact, str(random.randint(6900000000, 6999999999)))

if __name__ == '__main__': Main()