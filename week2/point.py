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
    coords = input('Δώστε συντεταγμένες σημείου (χ,y): ')
    if coords == '': break
    x,y = coords.split(',')
    if x.isdigit() and y.isdigit():
        new_point = Point(x,y)
        for p in Point.points:
            if p != new_point:
                print(f"Η απόσταση για το σημείο {p} είναι: {p.distance(new_point)}")