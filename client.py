import slixmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout

from slixmpp.stanza import StreamFeatures, Iq
from slixmpp.xmlstream import register_stanza_plugin, JID
from slixmpp.xmlstream.handler import CoroutineCallback
from slixmpp.xmlstream.matcher import StanzaPath
from slixmpp.plugins import BasePlugin
from slixmpp.plugins.xep_0077 import stanza, Register, RegisterFeature

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

        def send_private_message():
            recipient = input("Recipient: ")
            message = input("Message: ")

            self.send_message(mto=recipient, mbody=message, mtype="chat")
            print("Message sent!")

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

            # # delete['register']['remove'] == True
            # self.backend.unregister(delete['from'].bare)
            # self.xmpp.event('unregistered_user', delete)
            # delete.reply().send()

            # self["xep_0077"].user_unregister = True
            # self.api["user_remove"](None, None, delete["from"], delete)

            # delete['command']['xmlns']="http://jabber.org/protocol/commands"
            # delete['command']['action']="execute"
            # delete['command']['node']="http://jabber.org/protocol/admin#delete-user"
            delete.send()

            print("Account deleted succesfully.")
            self.disconnect()
            
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
                send_private_message()  
            elif logoption == 5:
                pass
            elif logoption == 6:
                self.disconnect()
                loginloop = False
            elif logoption == 7:
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
        print("HOSDAGJDOIGJISDJGIJSDFGJSDFIGJIDSJGIDSJGIJSDGISJDG")
        
    elif option == 3:
        loop = False
    else:
        print("Invalid option")

