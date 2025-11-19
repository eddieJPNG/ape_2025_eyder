import sqlite3

class CharacterDatabase:
    def __init__(self, name, age, height, concept):

        self.__name = name
        self.__age = age
        self.__height = height
        self.__concept = concept


        data = {
            "name": self.__name,
            "age": self.__age,
            "height": self.__height,
            "concept": self.__concept,
        }

        cnc =  sqlite3.connect("data")

        


    

        pass