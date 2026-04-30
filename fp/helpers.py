def ask_yes_no(prompt):
    """
    Repeatedly ask the user for y/n input until a valid answer is given.
    """
    while True:
        ans = input(prompt).strip().lower()
        if ans == "y" or ans == "yes":
            return True
        if ans == "n" or ans == "no":
            return False
        print("Please type y or n.")