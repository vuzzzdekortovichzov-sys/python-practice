class film:
    def __init__(self, name, year):
        self.name = name
        self.year = year

    def info(self):
        print("film:", self.name, "| year:", self.year)

f1 = film("john wick", 2014)
f2 = film("форсаж", 2001)

f1.info()
f2.info()