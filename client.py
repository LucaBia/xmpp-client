

loop = True
while loop:
    print("""
            \r-------------------------------
            \r1. Sign Up
            \r2. Log In
            \r3. Exit
            \r-------------------------------

        """)
    option = int(input("Choose an option to continue: "))
    if option == 1:
        print("QUE ONDA")
    elif option == 2:
        loginloop = True
        while loginloop:
            print("""
                    \r------------------------------------
                    \r1. Contacts
                    \r2. New contact
                    \r3. Show a user's contact
                    \r4. Private chat
                    \r5. Group chat
                    \r6. Log Out
                    \r7. Delete account
                    \r8. Exit
                    \r------------------------------------
                """)
            logoption = int(input("Choose an option to continue: "))
            
            if logoption == 1:
                print("Contacts")
            elif logoption == 2:
                pass
            elif logoption == 3:
                pass
            elif logoption == 4:
                pass
            elif logoption == 5:
                pass
            elif logoption == 6:
                pass
            elif logoption == 7:
                pass
            elif logoption == 8:
                loginloop = False
            else:
                print("Invalid option")
    elif option == 3:
        loop = False
    else:
        print("Invalid option")

