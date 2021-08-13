import slixmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

import logging
from getpass import getpass
from argparse import ArgumentParser


logging.basicConfig(level=logging.DEBUG, format="%(levelname)-8s %(message)s")

class Client(ClientXMPP):
    def __init__(self, username, password):
        ClientXMPP.__init__(self, username, password)
        self.username_ = username
        self.password = password

        self.add_event_handler("session_start", self.handleXMPPConnected)
        self.add_event_handler("register", self.signup)
        self.add_event_handler("message", self.inbox)

        # self.add_event_handler("groupchat_message", self.handleXMPPConnected.send_group_message)

    async def handleXMPPConnected(self, event):
        # Set us available
        self.send_presence()
        # We await to get our contacts
        await self.get_roster()

        def contacts():
            # Clasify our contacts in groups
            groups = self.client_roster.groups()
            # For every group we print the information available of that contact
            for group in groups:
                print(group)
                print('------------------------------------------')
                for jid in groups[group]:
                    name = self.client_roster[jid]['name']
                    if self.client_roster[jid]['name']:
                        print('\n', name, ' (',jid,')')
                    else:
                        print('\n', jid)

                    connections = self.client_roster.presence(jid)
                    for res, pres in connections.items():
                        show = 'available'
                        if pres['show']:
                            show = pres['show']
                        print('   - ',res, '(',show,')')
                        if pres['status']:
                            print('       ', pres['status'])
            print('------------------------------------------')
            
        # Add a new user to our roster.
        def new_contact():
            new_contact_user = input("New contact username: ")
            # Petition to add the contact
            self.send_presence_subscription(pto=new_contact_user)
            # Message to send to a new contact
            message="Hi new friend!"
            self.send_message(mto=new_contact_user, mbody=message, mtype="chat", mfrom=self.boundjid.bare)

        # Get the available information of a contact
        def contact_details():
            self.get_roster()

            contact_user = input("Contact username: ")

            name = self.client_roster[contact_user]['name']
            print('\n %s (%s)' % (name, contact_user))

            connections = self.client_roster.presence(contact_user)

            # If there is no recent acces que set status as xa an no recent sessio.
            if connections == {}:
                print("           xa")
                print("    No recent session")
    
            for res, pres in connections.items():
                show = 'available'
                if pres['show']:
                    show = pres['show']
                print('   - ', res, ' - ', show)
                print('       ',  pres['status'])


        # Send a direct message to a contact.
        def send_private_message():
            recipient = input("Recipient: ")
            message = input("Message: ")

            self.send_message(mto=recipient, mbody=message, mtype="chat")
            print("Message sent!")

        # Methos to join and send a message to a group chat.
        def send_group_message():
            self.register_plugin('xep_0030')
            self.register_plugin('xep_0045')
            self.register_plugin('xep_0199')

            print("""
                    \r1. Join Group
                    \r2. Send Message
            """)
            option = int(input("Choose an option: "))
            if option == 1:
                room = input("Group Name: ")
                nickname = input("Nickname: ")
                self.plugin['xep_0045'].join_muc(room+"@conference.alumchat.xyz", nickname)
            elif option == 2:
                room = input("Group name: ")
                message = input('Message: ')
                self.send_message(mto=room+"@conference.alumchat.xyz", mbody=message, mtype='groupchat')

            self.connect()
            self.process()

        def upload_file():
            self.register_plugin('xep_0363')

        # Upload the status and presence
        def change_presence():
            print("""
                    \r1.chat(available)
                    \r2.away(gone for short period of time)
                    \r3.xa(Extended away)
                    \r4.dnd(Do not disturb)
            """)
            presence_option = int(input("Choose a status: "))
            if presence_option == 1:
                show = "chat"
                status = "Available"
            elif presence_option == 2:
                show = "away"
                status = "A bit busy"
            elif presence_option == 3:
                show = "xa"
                status = "Busy"
            elif presence_option == 4:
                show = "dnd"
                status = "Do not disturb"

            self.send_presence(pshow=show, pstatus=status)

        # Opposite the register, we delete out logged account.
        def delete_account():
            self.register_plugin("xep_0030")
            self.register_plugin("xep_0004")
            self.register_plugin("xep_0199")
            self.register_plugin("xep_0066")
            self.register_plugin("xep_0077")

            delete = self.Iq()
            delete['type'] = 'set'
            delete['from'] = self.boundjid.user
            delete['register']['remove'] = True
            delete.send()

            print("Account deleted succesfully.")
            self.disconnect()
            

        loginloop = True
        while loginloop:
            print("""
                    \r------------------------------------
                    \r1. Contacts
                    \r2. Add a new contact
                    \r3. Show a user's contact details
                    \r4. Private chat
                    \r5. Send a file
                    \r6. Group chat
                    \r7. Change status
                    \r8. Log Out
                    \r9. Delete account
                    \r------------------------------------
                """)

            logoption = int(input("Choose an option to continue: "))
            
            if logoption == 1:
                contacts()
            elif logoption == 2:
                new_contact()
            elif logoption == 3:
                contact_details()
            elif logoption == 4:
                send_private_message()  
            elif logoption == 5:
                upload_file()
            elif logoption == 6:
                send_group_message()
            elif logoption == 7:
                change_presence()
            elif logoption == 8:
                self.disconnect()
                loginloop = False
            elif logoption == 9:
                delete_account()
            else:
                print("Invalid option")

            await self.get_roster()
            
    # We send the petitions of register to the server
    async def signup(self, iq):
        # We send presence to be available
        self.send_presence()
        # We get our contacts
        self.get_roster()
        
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" %
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()

    def inbox(self, message):
        print(str(message["from"]), ":  ", message["body"])

    

# Method to register a new user
def signup(username, password):
    # Instance of the Client class to continue with the request
    client = Client(username, password)

    client.register_plugin("xep_0030")
    client.register_plugin("xep_0004")
    client.register_plugin("xep_0199")
    client.register_plugin("xep_0066")
    client.register_plugin("xep_0077")

    # We force the registration
    client["xep_0077"].force_registration = True

    client.connect()
    client.process()

# Method to login
def login(username, password):
    # Instance of the Client class to continue with the request in the async method
    client = Client(username, password)
    client.register_plugin("xep_0030")
    client.register_plugin("xep_0199")

    client.connect()
    client.process(forever=False)


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
        print("Opcion 1")
        user = input("Username: ")
        password = input("Password: ")
        signup(user, password)

    elif option == 2:
        print("Opcion 2")
        user = input("Username: ")
        password = input("Password: ")
        login(user, password)
        
    elif option == 3:
        loop = False
    else:
        print("Invalid option")