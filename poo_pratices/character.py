class Character:
    def __init__(self, name, color, murshroomQuantity, heigth, physicalType, haveMustache ): 
        # Construtor de classe
        self.__name = name
        self.color = color 
        self.murshroom = murshroomQuantity
        self.height = heigth
        self.physical = physicalType
        self.mustache = haveMustache


    def pular(self):
        print(f"{self.__name} Pulou!")




Peach = Character("Peach", "Pink", 19, 1.75, "magra", False )


Peach.pular()


            
class RpgCharacter:
    def __init__(self, name: str, chaClass: str, race: str, age: int, height: float, atk: int, hp: int, magic: int):
        self.__name = name
        self.__chaClass = chaClass
        self.__race = race
        self.__age = age
        self.__heigth = height
        self.__atk = atk
        self.__hp = hp
        self.__magic = magic
        self.__monsterList = RpgCharacter.monsterList

    monsterList = []


    def attack(self, enemy):
        print(f"{self.__name} atacou {enemy} e desferiu {self.__atk} de dano!")

    def heal(self, heal):
        self.__hp += heal
        print(f"{self.__name} se curou com +{heal} de hp!")


    def monsterPick(self, monsterName):
        self.monsterList.append(monsterName)

        print(f"{self.__name} adicionou {monsterName} a lista de monstros!")

    def monsterListView(self):
        print(self.__monsterList)

         

Darkwing = RpgCharacter("Darkwing, the shadow wolf", "Assasin", "Elf", 22, 1.87, 55, 61, 22 )

Darkwing.attack("CrunchPower")

Darkwing.heal(50)

Darkwing.monsterListView()

Darkwing.monsterPick("Wind Worm")

Darkwing.monsterListView()

Darkwing.monsterPick("Drakesand")
Darkwing.monsterPick("Dark elf")
Darkwing.monsterPick("paralex")
Darkwing.monsterPick("Abnormal monster")

Darkwing.monsterListView()



