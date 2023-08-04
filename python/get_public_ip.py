#!/usr/bin/env python3

import urllib.request
import re
import sys

if __name__ == '__main__':
    get_choice = True
    while (get_choice):
        print("1. ident.me")
        print("2. ifconfig.me")
        print("3. dyndns.com")
        try:
            service = int(input("What service do you want to use to get your IP? "))
            if service < 1 or service > 3:
                print("*** Sorry, but your choice is not valid!")
            else:
                get_choice = False
        except ValueError:
            print("*** Sorry, but your choice is not valid!")
        except KeyboardInterrupt:
            print("\nBye!")
            sys.exit(1)

    try:
        if service == 1:
            external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        elif service == 2:
            external_ip = urllib.request.urlopen('https://ifconfg.me').read().decode('utf8')
        elif service == 3:
            data = urllib.request.urlopen('http://checkip.dyndns.com/').read().decode('utf8')
            external_ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)

        print(f"Your public IP is {external_ip}")

    except urllib.error.URLError:
        print("The service you are requesting seems to be off-line. Are you sure you're connected to the Internet?")
