import os, random, shelve

class Contact():
    """κάθε επαφή είναι όνομα και τηλέφωνο"""
    theContacts = {}

    def __init__(self, name, number='', new=False):
        self.name = name.strip()
        self.number = number.strip()
        Contact.theContacts[self.name]=self
        if new: self.insert()

    def __repr__(self):
        return self.name + ' : ' + self.number

    db = 'contacts'

    @staticmethod
    def retrive_contacts(term=''):
        Contact.theContacts = {}
        with shelve.open(Contact.db) as db:
            for k in db:
                if not term or term.lower() in k.lower():
                    Contact(db[k].name, db[k].number)
        # print the retrived contacts
        for c in sorted(Contact.theContacts, key=lambda x : x.split()[-1]):
            if term:
                if term.lower() in c.lower():
                    print(Contact.theContacts[c])
            else:
                print(Contact.theContacts[c])
    @staticmethod
    def del_contact(id):
        if  id in Contact.theContacts:
            del Contact.theContacts[id]
            with shelve.open(Contact.db) as db:
                if id in db: del db[id]
    @staticmethod
    def count_records():
        with shelve.open(Contact.db) as db:
            return len(db)
    def insert(self):
        with shelve.open(Contact.db) as db:
            db[self.name] = self
    def set_number(self, number):
        self.number = number
        with shelve.open(Contact.db) as db:
            if self.number in db.keys():
                db[self.name] = self

class Main():
    """κλάση διαχείρισης επαφών - δημιουργία - διαγραφή"""
    def __init__(self):
        while True:
            command = input(f'\nΕπαφές {Contact.count_records()}\nΕισαγωγή[+] Διαγραφή[-] Επισκόπηση[?] Έξοδος[Enter]')
            if command == '': break
            elif command == "+":
                contact_details = input('Εισάγετε όνομα : τηλέφωνο ή πλήθος επαφών αυτόματης εισαγωγής ')
                if ':' in contact_details:
                    try:
                        id = contact_details.split(':')[0].strip()
                        if id in Contact.theContacts: # τροποποίηση εγγραφής
                            Contact.theContacts[id].set_number(contact_details.split(':')[1].strip())
                        else:
                            Contact(*contact_details.split(':'), new=True)
                    except IndexError: print('Σφάλμα εισαγωγής επαφής')
                elif contact_details.isdigit():
                    if int(contact_details) < 500:
                        self.create_contacts(int(contact_details))
                    else:  print('Σφάλμα: Δώσατε πολύ μεγάλο αριθμό επαφών..')
                else: print('Προσοχή! Δώστε όνομα (:) τηλέφωνο')
            elif command == "?":
                Contact.retrive_contacts(command[1:])
            elif command == "-":
                name = input('Διαγραφή όνομα ')
                try:
                    Contact.del_contact(name.strip())

                except KeyError:
                    print('Δεν υπάρχει η επαφή που ζητήσατε')

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
            Contact(contact, str(random.randint(6900000000, 6999999999)), new=True)

if __name__ == '__main__': Main()