# XMPP Client

This project is part of the networking course at the Universidad del Valle de Guatemala.  It consists of the implementation of a client through the use of the XMPP protocol. It is a CLI program developed in python. It should be noted that it must be run with python 3.7 and not higher since a higher version has reflected conflicts with sending files to other users.

Las funcionalidades implementadas en este proyecto fueron
- Sign In
- Sign Up
- Sign Out
- Delete account
- List all contacts
- Display contact details
- Add a new contact
- Private chat(send and receive messages)
- Group chat (Join, send and receive messages)
- Change status (Presence)
- Send a file

To run the project:
1. Clone this repository or download it
2. Create a virtual environment (python3 -m venv venv)
3. Activate the virtual environment (sourcen venv/bin/activate)
4. Install dependencies:
    - pip install slixmpp
    - pip install aiohttp
    Note: if your python is higher than 3.7 you should install version 3.7 of python and then install dependencies with pip3.7
5. Run the client: python3 client.py
    Note: if your python is higher than 3.7 you should install version 3.7 of python and then run python3.7 client.py
6. Follow all the instructions in the menu that the program shows. For this project we use @ alumchat.xyz.
