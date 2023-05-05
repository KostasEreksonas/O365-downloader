#!/usr/bin/env python3

def create_config():
    username = input("Enter username: ")
    password = input("Enter password: ")
    with open('config.py', 'w') as file:
        file.write(f'#!/usr/bin/env python3\n\nusername = \"{username}\"\npassword = \"{password}\"\n')

create_config()
