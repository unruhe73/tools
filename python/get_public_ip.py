#!/usr/bin/env python3

import urllib.request
import re
import sys
import argparse               # let you get parameters from the command line
from random import choice
from random import randint


service = ['ident.me', 'ifconfig.me', 'icanhazip.com', 'dyndns.com']
get_ip_service = {}
get_ip_service[service[0]] = 'https://ident.me'
get_ip_service[service[1]] = 'https://ifconfig.me'
get_ip_service[service[2]] = 'https://icanhazip.com'
get_ip_service[service[3]] = 'http://checkip.dyndns.com'
id_dyndns = 3


def get_parameters():
    parser = argparse.ArgumentParser(description='A python script to detect your public IP address')
    pyname = sys.argv[0]
    parser.add_argument('-k', '--ask', help='let user choose the service to use to get you public IP address', action="store_true")
    args = parser.parse_args()

    what_service = choice(service)
    what_service_url = get_ip_service[what_service]
    if args.ask:
        ask_service = True
    else:
        ask_service = False

    return ask_service, what_service, what_service_url


def get_ip_address(ask_service, what_service, what_service_url):
    if ask_service:
        get_choice = True
        while (get_choice):
            n = 1
            for s in get_ip_service:
                print(f"{n}. {s}")
                n += 1
            try:
                c_service = int(input("What service do you want to use to get your IP? "))
                if c_service < 1 or c_service > id_dyndns + 1:
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
        c_service = randint(0, id_dyndns)
        print(f"I'm using {service[c_service]} service.")

    url = get_ip_service[service[c_service]]
    try:
        data = urllib.request.urlopen(url).read().decode('utf8')
        if c_service == id_dyndns:
            external_ip = re.compile(r'Address: (\d+\.\d+\.\d+\.\d+)').search(data).group(1)
        else:
            external_ip = data

        print(f"Your public IP is {str.strip(external_ip)}.")

    except urllib.error.URLError:
        print("The service you are requesting seems to be off-line. Are you sure you're connected to the Internet?")


if __name__ == '__main__':
    ask_service, what_service, what_service_url = get_parameters()
    get_ip_address(ask_service, what_service, what_service_url)
