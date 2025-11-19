import re


class Temperature:


    valid_units = ("K", "F", "C")
    regex = r"^[+-]?\d+\.?\d*[CKF]?$"


    def __init__(self, value, scale=None):



        if isinstance(value, (int, float)):
            if scale is None:
                value = "K"

            if scale not in Temperature.valid_units:
                raise ValueError(f"Invalid temperature unit: {scale}")
            
            value = float(value)



        elif isinstance(value, str):
            if scale is not None:
                raise ValueError("Cannot specify unit thats the value is a string")
            
            if re.match(Temperature.regex, value) is None:
                raise ValueError ("Invalid String Temperature")
            
            if value[-1].isalpha():
                scale = value[-1]
                value = float(value[0: -1])
            else:
                scale = "K"
                value = float(value)

            

            
                
            
        else:

            raise TypeError("Invalide temperature")
        

        self.__value = value
        self.__scale = scale

    def __str__(self):
        return f"{self.__value:0.2f}`{self.__scale} "

    
a = Temperature("+32.45K")