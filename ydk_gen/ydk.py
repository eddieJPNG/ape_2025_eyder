from path import *
from utils import *

is_running = True

def ydk_gen_menu():

    while is_running == True:

        line_gen(50)

        title = ">>> YDK GENERATOR MENU"

        lines_titles(title)
        print(title)
        lines_titles(title)

        print("1. Generate new YDK")
        print("2. View existing YDKs")
        print("0. Return to the main menu")

        choice = input("Select an option(0-2): > ")

        lines_titles(choice)
        print(choice)
        lines_titles(choice)

        line_gen(50)

        match choice:
            case "1":
                ydk_gen()
            case "2":
                pass
            case "0":
                break


def ydk_gen():
    deck_name = input("Enter the name of the deck: > ")

    choice = input("Add a card to the deck? (y/n):")

    match choice:
        case "y":
            while choice == "y":
                card_name = input("Enter the card name: > ")
                save_text(f"{deck_name}.txt", card_name)
                choice = input("Add another card to the deck? (y/n):")
        case "n":
            print("Deck generation completed.")
            

        

            

