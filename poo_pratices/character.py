class Character:
    def __init__(self, name, color, murshroomQuantity, heigth, physicalType, haveMustache ): 
        # Construtor de classe
        self.name = name
        self.color = color 
        self.murshroom = murshroomQuantity
        self.height = heigth
        self.physical = physicalType
        self.mustache = haveMustache


    def pular(self):
        print(f"{self.name} Pulou!")




Peach = Character("Peach", "Pink", 19, 1.75, "magra", False )


Peach.pular()
            

    





# str str int float str bool