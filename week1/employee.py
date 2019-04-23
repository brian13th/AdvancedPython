class Employee():
    """Defines a corporation employee"""
    theEmployees = []
    def __init__(self, name, payment):
        self.name = name
        self.payment = payment
        Employee.theEmployees.append(self)


while True:
    n = input('Employee name please? ')
    if n == '': break
    p = input('... and paycheck ?')
    Employee(n, p)

for empl in sorted(Employee.theEmployees, key=lambda x:x.payment):
    print(empl.name,',',empl.payment)