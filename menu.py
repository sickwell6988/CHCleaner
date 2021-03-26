main_menu_options_list = [1,2,3,4,5,6,7,8]

main_menu_options = '''
[1] Display users you follow
[2] Display mutual followers
[3] Display non-mutual followings
[4] Follow user
[5] Un-follow user
[6] List available rooms
[7] Exit Application
'''

# Error messages:
invalid_val = "Incorrect value or option provided. Try again..."
negat_val = "Positive number expected"


def repeat_menu(ask_to_repeat = True):
    while ask_to_repeat:
        decision = input("Press 'q' to open main menu: ")
        if decision.lower() != "q":
            print(invalid_val)
        else:
            ask_to_repeat = False
            return ask_to_repeat


def get_main_menu_input():
    main_menu_decision_defined = False
    while not main_menu_decision_defined:
        try:
            main_menu_decision = int(input("\n>>> "))
            if main_menu_decision in main_menu_options_list:
                main_menu_decision_defined = True
                return main_menu_decision
            else:
                print(invalid_val)
        except ValueError:
            print(invalid_val)


def start_follow_unfollow(stage):
    decision = False
    while not decision:
        if stage == "ask":
            option = input("Would you like to unfollow listed people? (Y/n): ")
        else:  # == "run":
            option = input("Start unfollowing non-mutual users? (Y/n): ")
        if option.lower() != "y" and option.lower() != "n":
            print(invalid_val)
        elif option.lower() == "n":
            return False
        else:
            decision = True
            return decision


# def get_users_count():
#     verify_integer_input = True
#     while verify_integer_input:
#         try:
#             follow_get_count = int(input("Enter # of users to get:\n>>> "))
#             if follow_get_count > 0:
#                 verify_integer_input = False
#                 return follow_get_count
#             else:
#                 print(negat_val)
#         except Exception:
#             print(negat_val)