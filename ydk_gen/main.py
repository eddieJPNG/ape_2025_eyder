import json
import os
import random
from utils import *
from path import *
from ydk import *



def main():

    
    is_running = True

    while is_running is True:
        line_gen(10)


        title = ">>>MAIN MENU<<<"

        lines_titles(title)
        print(title)
        lines_titles(title)

        print("1. Ydk Generator")
        print("2. Exit")

    
    
        choice = input("Select an option(1-2): > ")

        line_gen(10)

        
        
        match choice:
            case "1":
                ydk_gen_menu()
                
            case "2":
                is_running = False


    



if __name__ == "__main__":
    main()