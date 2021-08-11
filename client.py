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

    async def handleXMPPConnected(self, event): 
        self.send_presence()

        await self.get_roster()

        def contacts():
            groups = self.client_roster.groups()
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
            

        def new_contact():
            new_contact_user = input("New contact username: ")
            self.send_presence_subscription(pto=new_contact_user)
            message="Hi new friend!"
            self.send_message(mto=new_contact_user, mbody=message, mtype="chat", mfrom=self.boundjid.bare)

        def contact_details():
            self.get_roster()

            contact_user = input("Contact username: ")

            name = self.client_roster[contact_user]['name']
            print('\n %s (%s)' % (name, contact_user))

            connections = self.client_roster.presence(contact_user)

            if connections == {}:
                print("           xa")
                print("    No recent session")
    
            for res, pres in connections.items():
                show = 'available'
                if pres['show']:
                    show = pres['show']
                print('   - ', res, ' - ', show)
                print('       ',  pres['status'])


        def send_private_message():
            recipient = input("Recipient: ")
            message = input("Message: ")

            self.send_message(mto=recipient, mbody=message, mtype="chat")
            print("Message sent!")

        def upload_file():
            self.register_plugin('xep_0363')

        
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
                pass
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
            
    
    async def signup(self, iq):
        self.send_presence()
        self.get_roster()

        """
        Fill out and submit a registration form.
        The form may be composed of basic registration fields, a data form,
        an out-of-band link, or any combination thereof. Data forms and OOB
        links can be checked for as so:
        if iq.match('iq/register/form'):
            # do stuff with data form
            # iq['register']['form']['fields']
        if iq.match('iq/register/oob'):
            # do stuff with OOB URL
            # iq['register']['oob']['url']
        To get the list of basic registration fields, you can use:
            iq['register']['fields']
        """
        
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


def signup(username, password):
    client = Client(username, password)

    client.register_plugin("xep_0030")
    client.register_plugin("xep_0004")
    client.register_plugin("xep_0199")
    client.register_plugin("xep_0066")
    client.register_plugin("xep_0077")

    client["xep_0077"].force_registration = True

    client.connect()
    client.process()

def login(username, password):
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
        user = input("Username (user@alumchat.xyz): ")
        password = input("Password: ")
        signup(user, password)

    elif option == 2:
        print("Opcion 2")
        user = input("Username (user@alumchat.xyz): ")
        password = input("Password: ")
        login(user, password)
        
    elif option == 3:
        loop = False
    else:
        print("Invalid option")