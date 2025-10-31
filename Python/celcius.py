running = True

def convert_celsius(value):

 if not isinstance(value, (int, float)):
    raise ValueError("Temperatura celsius deve ser numérico")
 return value * 9/5 + 32

def main():
  while running == True:
   try:
     

     temp = float(input("Temperatura em faireheight: >"))

     celsius = convert_celsius(temp)

     print(f"{temp: 0.2f}ºF é igual a{celsius: 0.2f}ºC")

     
   except ValueError as erro:
     print("Valor em Fº deve ser em numérico", "erro:", erro)
    



   

if __name__ == "__main__":
  main()