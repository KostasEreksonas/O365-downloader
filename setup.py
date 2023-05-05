#!/usr/bin/env python3

def create_config():
    username = input("Enter Microsoft 365 username: ")
    password = input("Enter Microsoft 365 password: ")
    domain = input("Enter name of your sharepoint domain: ")
    site = input("Enter name of your sharepoint site: ")
    with open('config.py', 'w') as file:
        file.write(f'#!/usr/bin/env python3\n\nusername = \"{username}\"\npassword = \"{password}\"\ndomain = \"{domain}\"\nsite = \"{site}\"\n')

create_config()
