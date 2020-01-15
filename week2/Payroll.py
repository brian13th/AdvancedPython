class Person():
    """ υπερκλάση άνθρωπος"""
    employees = []
    def __init__(self, name, job='', salary=0):
        self.name = name
        self.job = job
        self.salary = float(salary)
        Person.employees.append(self)
    def give_raise(self, percent):
        """αύξηση στο μισθό με τιμές από 0 μέχρι 1"""
        self.salary = float(self.salary(1+ percent))
    def __str__(self):
        return f"{self.name} {self.job} {[self.salary if self.salary > 0 else ' ']} "

class Manager(Person):
    """ κλάση διευθυντή"""
    def __init__(self, name, salary=0):
        Person.__init__(self, name, 'Διευθυντής', salary )
    def give_raise(self, percent, bonus=0.10):
        Person.give_raise(self, percent+bonus)
