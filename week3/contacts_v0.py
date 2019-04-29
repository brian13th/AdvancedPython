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

class Main():
    """κλάση διαχείρισης επαφών - δημιουργία - διαγραφή"""
    while True:
        command = input(f'Εισαγωγή[+] Διαγραφή[-] Επισκόπηση[?] Έξοδος[Enter]')
        if command == '': break
        elif command == "+":
            contact_details = input('Εισάγετε όνομα : τηλέφωνο ')
            if ':' in contact_details:
                try: Contact(*contact_details.split(':'))
                except IndexError: print('Σφάλμα εισαγωγής επαφής')
            else: print('Προσοχή! Δώστε όνομα : τηλέφωνο')
        elif command == "?":
            Contact.list_contacts()
        elif command == "-":
            name = input('Διαγραφή όνομα ')
            try:
                del Contact.theContacts[name.strip()]
            except IndexError:
                print('Δεν υπάρχει η επαφή που ζητήσατε')

if __name__ == '__main__': Main()