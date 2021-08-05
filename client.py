
loop = True
while loop:
    print("""
    -------------------------------
    1. Sign Up
    2. Log In
    3. Exit
    -------------------------------

    """)
    option = input("Choose an option to continue: ")
    match option:
        case "1":
            print("QUE ONDA")
        case "2":
            loginloop = True
            while loginloop:
                print("""
    ------------------------------------
    1. Contacts
    2. New contact
    3. Show a user's contact
    4. Private chat
    5. Group chat
    6. Log Out
    7. Delete account
    8. Exit
    ------------------------------------

                """)
                logoption = input("Choose an option to continue: ")
                match logoption:
                    case "1":
                        print("Contacts")
                    case "2":
                        pass
                    case "3":
                        pass
                    case "4":
                        pass
                    case "5":
                        pass
                    case "6":
                        pass
                    case "7":
                        pass
                    case "8":
                        loginloop = False
                    case _:
                        print("Invalid option")
        case "3":
            loop = False
        case _:
            print("Invalid option")

