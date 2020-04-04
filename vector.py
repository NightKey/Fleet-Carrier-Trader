import math
class vector:
    def __init__(self, x, y, z=None):
        self.x = x
        self.y = y
        self.z = z

    def set(self, *arg):
        if len(arg) == 1:
            for item in arg:
                if isinstance(item, vector):
                    self.x = item.x
                    self.y = item.y
                    self.z = item.z
                elif isinstance(item, (list, tuple)):
                    self.x = item[0]
                    self.y = item[1]
                    self.z = item[2] if len(item) > 2 else None
                else:
                    return NotImplemented
        else:
            self.x = arg[0]
            self.y = arg[1]
            self.z = arg[2] if len(arg) > 2 else None
            
    def copy(self):
        return self
    
    def add(self, *arg):
        if len(arg) == 1:
            for item in arg:
                if isinstance(item, vector):
                    x = self.x + item.x
                    y = self.y + item.y
                    z = (self.z + item.z if self.z != None and item.z != None else None)
                elif isinstance(item, (list, tuple)):
                    x = self.x + item[0]
                    y = self.y + (item[1] if len(item) > 1 else 0)
                    z = self.z + (item[2] if len(item) > 2 else 0)
                elif isinstance(item, (int, float)):
                    x = self.x + item
                    y = self.y
                    z = self.z
                else:
                    return NotImplemented
        else:
            x = self.x + arg[0]
            y = self.y + arg[1]
            z = self.z + (arg[2] if len(arg) > 2 else 0)
        return vector(x, y, z)
    
    def __add__(self, other):
        return self.add(other)
    
    def sub(self, *arg):
        if len(arg) == 1:
            for item in arg:
                if isinstance(item, vector):
                    x = self.x - item.x
                    y = self.y - item.y
                    z = (self.z - item.z if self.z != None and item.z != None else None)
                elif isinstance(item, (list, tuple)):
                    x = self.x - item[0]
                    y = self.y - (item[1] if len(item) > 1 else 0)
                    z = self.z - (item[2] if len(item) > 2 else 0)
                elif isinstance(item, (int, float)):
                    x = self.x - item
                    y = self.y
                    z = self.z
                else:
                    return NotImplemented
        else:
            x = self.x - arg[0]
            y = self.y - arg[1]
            z = self.z - (arg[2] if len(arg) > 2 else 0)
        return vector(x, y, z)
    
    def __sub__(self, other):
        return self.sub(other)
    
    def mult(self, num):
        x = self.x * num
        y = self.y * num
        if self.z != None:
            z = self.z * num
        else: z = None
        return vector(x,y,z)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.mult(other)
        else:
            return NotImplemented

    def div(self, num):
        x = self.x / num
        y = self.y / num
        if self.z != None: z = self.z / num
        else: z = None
        return vector(x,y,z)

    def mag(self):
        return math.sqrt(self.x*self.x+self.y*self.y+(self.z*self.z if self.z != None else 0))
    
    def __len__(self):
        return self.mag()

    def maqSq(self):
        return self.x*self.x+self.y*self.y+(self.z*self.z if self.z != None else 0)

    def dot(self, other):
        if isinstance(other, vector):
            return self.x*other.x + self.y*other.y + (self.z*other.z if self.z != None and other.z != None else (self.z if self.z != None else (other.z if other.z != None else 0)))
        else:
            return NotImplemented
    
    def cross(self, other):
        if self.z == None or other.z == None:
            return NotImplemented
        x = self.y*other.z - self.z*other.y
        y = self.z*other.x - self.x*other.z
        z = self.x*other.y - self.y*other.x
        return vector(x, y, z)

    def dist(self, other):
        return math.sqrt(math.pow(self.x-other.x, 2) + math.pow(self.y-other.y, 2) + (math.pow(self.z - other.z, 2) if self.z != None and other.z != None else (math.pow(self.z, 2) if self.z != None else (math.pow(other.z, 2) if other.z != None else 0))))

    def normalize(self):
        length = self.mag()
        self.x /= length
        self.y /= length
        if self.z != None:
            self.z /= length

    def lim(self, max):
        if self.mag() > max:
            max = self.mag() / (max * 1.0)
            self.x /= max
            self.y /= max
            if self.z != None:
                self.z /= max

    def __str__(self):
        return ("[x: {}, y: {}]".format(self.x, self.y) if self.z == None else "[x: {}, y: {}, z: {}]".format(self.x, self.y, self.z))

if __name__ == "__main__":
    i = vector(1, 0, 0)
    j = vector(0, 1, 0)
    k = vector(0, 0, 1)
    jk = j+k
    p = vector(12, 5, 2)
    print("i: [{}]\nj: [{}]\nk: [{}]".format(i, j, k))
    print("j+k: [{}]".format(jk))
    print("p: [{}]".format(p))
    print("Distance between p and jk: {}".format(p.dist(jk)))
    print("P length: {}".format(p.mag()))
    p.lim(4)
    print("p.lim(4): [{}]\np len: {}".format(p, p.mag()))
    p.normalize()
    print("Normalized p: [{}]".format(p))
    print("Normalized p len: {}".format(p.mag()))
    print("{}+{} = {}".format(p, jk, p+jk))
    print("{}*2 = {}".format(p, p*2))