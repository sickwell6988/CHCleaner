def repeat_menu(ask_to_repeat = True):
    while ask_to_repeat:
        decision = input("Restart menu? (Y/n): ")
        if decision.lower() != "y" and decision.lower() != "n":
            print("Incorrect value. Try again...")
        elif decision.lower() == "n":
            print("Goodbye!")
            exit(0)
        else:
            ask_to_repeat = False
    return ask_to_repeat