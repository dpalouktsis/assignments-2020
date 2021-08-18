class Circle:

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def __repr__(self):
        return (self.__str__())

    def __str__(self):
        x1 = str(self.x)
        y1 = str(self.y)
        r1 = str(self.r)
        return (x1+" "+y1+" "+r1)

    def find_distance(self, xek, yek):
        if (xek == 0 and yek == 0):
            d = (self.x**2 + self.y**2)**(1/2)
        else:
            d = (((self.x - xek)**2 + (self.y - yek)**2)**(1/2))
        d = round(d, 2)
        return d

    def intersect(self, other):
        d = self.find_distance(other.x, other.y)
        d = round(d, 2)
        return ((self.r+other.r) - d > 0.1)

    def find_adj_circle(self, other, rk):
        dx = other.x - self.x
        dy = other.y - self.y
        d = (dx**2 + dy**2)**(1/2)
        r1 = self.r + rk
        r2 = other.r + rk
        l_index = ((r1**2 - r2**2 + d**2)/(2*d**2))
        e = (((r1**2/d**2) - l_index**2)**(1/2))
        kx = self.x + l_index*dx - e*dy
        kx = round(kx.real, 2)
        ky = self.y + l_index*dy + e*dx
        ky = round(ky.real, 2)
        c = Circle(kx, ky, rk)
        return c

    def dist_circle_segment(self, x1, y1, x2, y2):
        l2 = (x1-x2)**2 + (y1-y2)**2
        if (l2 == 0):
            d = ((x1 - self.x)**2 + (y1 - self.y)**2)**(1/2)
        else:
            t = ((self.x-x1)*(x2-x1)+(self.y-y1)*(y2-y1))/l2
            if (t < 0):
                t = 0
            if (t > 1):
                t = 1
            px = x1 + t*(x2-x1)
            py = y1 + t*(y2-y1)
            d = ((px-self.x)**2 + (py-self.y)**2)**(1/2)
        d = round(d, 2)
        return d
