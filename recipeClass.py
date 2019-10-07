
class Recipe:
    def __init__(self, name, serves=4, preptime='15m', cooktime='15m', ingriedients=[], method=[]):
        self.name = name
        self.serves = serves
        self.preptime = preptime
        self.cooktime = cooktime
        self.ingriedients = ingriedients
        self.method = method
        
    def __repr__(self):
        return(f"{self.name} is good")

    def displayDetails(self):
        print("Recipe Title: ", self.name)
        print("serves: ", self.serves)


