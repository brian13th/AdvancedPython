import os, random
import sqlite3 as lt

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

    db = 'contacts.database'

    @staticmethod
    def create_db():
        try:
            conn = lt.connect(Contact.db)
            with conn:
                c = conn.cursor()
                sql = 'CREATE TABLE contactstable(name TEXT PRIMARY KEY, number TEXT);'
                c.execute(sql)
                return True
        except lt.Error:
            return False # εαν ο πίνακας υπάρχει ήδη

    @staticmethod
    def count_records():
        try:
            conn = lt.connect(Contact.db)
            with conn:
                c = conn.cursor()
                sql = 'SELECT COUNT (*) FROM contactstable;'
                c.execute(sql)
                return c.fetchone()[0]
        except lt.Error as er:
            print(er)
            return 0


    @staticmethod
    def retrive_contacts(term=''):
        Contact.theContacts = {}
        try:
            conn = lt.connect(Contact.db)
            with conn:
                c = conn.cursor()
                if term:  # έχει δοθεί κλειδί αναζήτησης term
                    sql = "select * from contactsTable where name like '%{}%'; ".format(term)
                else:
                    sql = "select * from contactsTable;"
                c.execute(sql)
                records = c.fetchall()
                for rec in records:
                    Contact(rec[0], rec[1])
        except lt.Error as er:
            print(er)
        for c in sorted(Contact.theContacts, key=lambda x: x.split()[-1]):
            if term:
                if term.lower() in c.lower():
                    print(Contact.theContacts[c])
            else:
                print(Contact.theContacts[c])
    @staticmethod
    def del_contact(id):
        if  id in Contact.theContacts:
            del Contact.theContacts[id]
        try:
            conn = lt.connect(Contact.db)
            with conn:
                c = conn.cursor()
                sql = f"DELETE FROM contactstable WHERE name = '{id}';"
                c.execute(sql)

        except lt.Error as er:
            print(er)
    def insert(self):
        try:
            conn = lt.connect(Contact.db)
            with conn:
                c = conn.cursor()
                sql = 'INSERT INTO contactstable VALUES (?,?);'
                c.execute(sql, (self.name, self.number))
        except lt.Error as er:
            print(er)

    def set_number(self, number):
        self.number = number
        try:
            conn = lt.connect(Contact.db)
            with conn:
                c = conn.cursor()
                sql = 'update contactTable set number = "{}" where name = "{}";'.format(self.number, self.name)
                c.execute(sql)
        except lt.Error as er:
            print(er)

class Main():
    """κλάση διαχείρισης επαφών - δημιουργία - διαγραφή"""
    Contact.create_db()
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