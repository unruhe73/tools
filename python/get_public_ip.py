#!/usr/bin/env python3

import urllib.request
import sys

get_choice = True
while (get_choice):
    print("1. ident.me")
    print("2. ifconfig.me")
    try:
        service = int(input("What service do you want to use to get your IP? "))
        if service < 1 or service > 2:
            print("*** Sorry, but your choice is not valid!")
        else:
            get_choice = False
    except ValueError:
        print("*** Sorry, but your choice is not valid!")
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(1)

if service == 1:
    external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
elif service == 2:
    external_ip = urllib.request.urlopen('https://ifconfig.me').read().decode('utf8')

print(f"Your public IP is {external_ip}")
