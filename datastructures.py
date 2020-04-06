class Commoditie():
    def __init__(self, name, is_rare, max_buy, max_sell, min_buy, min_sell, avg_price):
        self.name = name
        self.is_rare = bool(is_rare)
        self.max_buy = int(max_buy or -1)
        self.min_buy = int(min_buy or -1)
        self.max_sell = int(max_sell or -1)
        self.min_sell = int(min_sell or -1)
        self.avg_price = int(avg_price or -1)

    def __str__(self):
        return self.name
    
class Station():
    def __init__(self, name, system_id, max_landing, has_docking, has_commodities):
        self.name = name
        self.system_id = system_id
        self.max_landing = max_landing
        self.has_docking = bool(has_docking)
        self.has_commodities = bool(has_commodities)

    def __str__(self):
        return self.name

class System():
    def __init__(self, name, x, y, z, population, security):
        from vector import vector
        self.name = name
        self.coord = vector(x, y, z)
        self.population = population
        self.security = security
    
    def Distance(self, other):
        return round(self.coord.dist(other.coord), 2)

    def __str__(self):
        return self.name