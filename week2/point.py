class Point():
    """ Ευριστικός αλγόριθμος σημείων στο καρτεσιανό επίπεδο """
    points = []
    def __init__(self, x=0, y=0):
        self.x = int(x)
        self.y = int(y)
        Point.points.append(self)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def distance(self, p):
        return ((self.x - p.x)**2 + (self.y - p.y)**2)**0.5


while True:
    command = input('Δώστε εντολή insert x,y ή delete x,y: ')
    if command == '' : break
    if len(command.split())<2 : continue
    coords = command.split()[1]
    x,y = coords.split(',')
    if x.isdigit() and y.isdigit():
        if command.split()[0] == 'insert':
            new_point = Point(x,y)
            print(f" Υπάρχουν συνολικά {len(Point.points)} σημεία")
            for p in Point.points:
                if p != new_point:
                    print(f"Το σημείο {p} είναι σε απόσταση: {p.distance(new_point)} από το σημείο")
        elif command.split()[0] == 'delete':
            deleted = False
            new_points = []
            for p in Point.points:
                if p.x == int(x) and p.y == int(y):
                    del p
                    deleted = True
                else: new_points.append(p)
            Point.points = new_points
            if deleted:
                print(f"Τα εναπομείναντα σημεία είναι:")
                for p in Point.points: print(p)
            else: print(f"Το σημείο δεν βρέθηκε")