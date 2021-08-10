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
            print("CONTACTS")

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
                    \r------------------------------------
                """)

            logoption = int(input("Choose an option to continue: "))
            
            if logoption == 1:
                contacts()
            elif logoption == 2:
                pass
            elif logoption == 3:
                pass
            elif logoption == 4:
                pass
            elif logoption == 5:
                pass
            elif logoption == 6:
                self.disconnect()
                loginloop = False
            elif logoption == 7:
                pass
            else:
                print("Invalid option")





    
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



# class SendMsgBot(slixmpp.ClientXMPP):

#     def __init__(self, jid, password, recipient, message):
#         slixmpp.ClientXMPP.__init__(self, jid, password)



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
        print("HOSDAGJDOIGJISDJGIJSDFGJSDFIGJIDSJGIDSJGIJSDGISJDG")
        
    elif option == 3:
        loop = False
    else:
        print("Invalid option")

