#!/usr/bin/env python3

import urllib.request
import re
import sys
import argparse               # let you get parameters from the command line
from random import choice
from random import randint


service = ['ident.me', 'ifconfig.me', 'dyndns.com']
get_ip_service = {}
get_ip_service[service[0]] = 'https://ident.me'
get_ip_service[service[1]] = 'https://ifconfig.me'
get_ip_service[service[2]] = 'http://checkip.dyndns.com/'


def get_parameters():
    parser = argparse.ArgumentParser(description='A python script to detect your public IP address')
    pyname = sys.argv[0]
    parser.add_argument('-y', '--any', help='let choose to the scritp the service to use to get you public IP address', action="store_true")
    args = parser.parse_args()

    what_service = choice(service)
    what_service_url = get_ip_service[what_service]
    if args.any:
        use_any_service = True
    else:
        use_any_service = False

    return use_any_service, what_service, what_service_url


def get_ip_address(use_any_service, what_service, what_service_url):
    if not use_any_service:
        get_choice = True
        while (get_choice):
            n = 1
            for s in get_ip_service:
                print(f"{n}. {s}")
                n += 1
            try:
                c_service = int(input("What service do you want to use to get your IP? "))
                if c_service < 1 or c_service > 3:
                    print("*** Sorry, but your choice is not valid!")
                else:
                    get_choice = False
            except ValueError:
                print("*** Sorry, but your choice is not valid!")
            except KeyboardInterrupt:
                print("\nBye!")
                sys.exit(1)
        c_service -= 1
    else:
        c_service = randint(0, 2)
        print(f"I'm using {service[c_service]} service.")

    url = get_ip_service[service[c_service]]
    try:
        data = urllib.request.urlopen(url).read().decode('utf8')
        if c_service == 2:
            external_ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
        else:
            external_ip = data

        print(f"Your public IP is {external_ip}.")

    except urllib.error.URLError:
        print("The service you are requesting seems to be off-line. Are you sure you're connected to the Internet?")


if __name__ == '__main__':
    use_any_service, what_service, what_service_url = get_parameters()
    get_ip_address(use_any_service, what_service, what_service_url)
