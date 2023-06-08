#!/usr/bin/env python3

import argparse               # let you get parameters from the command line
import sys                    # let you access to system stuff as argv command line parameters
import ipaddress              # let you use IP addresses for hosts/networks
import platform               # let you get the operating system name
import subprocess             # let you execute a shell command
from progress.bar import Bar  # let you use a progress bar
from time import sleep        # let you use sleep to delay


def scanning_network(network_ip='192.168.0.0/24', show_reachable_ips=False):
    ips = []
    try:
        network_ipv4 = ipaddress.IPv4Network(network_ip)
    except ValueError:
        print('address/netmask is invalid for IPv4:', base_ip)
        return ips

    print(f"I'm going to scan {network_ip} network")
    if not show_reachable_ips:
        bar = Bar('Processing', max=len(list(network_ipv4.hosts())))

    if platform.system().lower() == 'windows':
        packets_opt = '-n'
    else:
        packets_opt = '-c'

    for ip in network_ipv4.hosts():
        command = ['ping', packets_opt, '1', '-W1', str(ip) ]
        try:
            if subprocess.run(args=command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                if show_reachable_ips:
                    print(f'{str(ip)} is reachable')
                ips.append(str(ip))
        except KeyboardInterrupt:
            break
        if not show_reachable_ips:
            bar.next()
    if not show_reachable_ips:
        bar.finish()
    return ips


def scanning_network_write_to_file(network_ip='192.168.0.0/24', show_reachable_ips=False, write_to_file='reachable_ips.txt'):
    ip_hosts = scanning_network(network_ip=network_ip, show_reachable_ips=show_reachable_ips)
    if len(ip_hosts) > 0:
        if write_to_file:
            with open(write_to_file, 'w+') as f:
                f.write('\n'.join(ip_hosts))
                f.write('\n')
            print(f'\nI saved on-line hosts on the text file {write_to_file}')
        else:
            sleep(2)
            print('reachable IPs:')
            for ip in ip_hosts:
                print(ip)
    else:
        print('No reachable IPs')


def get_parameters():
    network_ip = '192.168.0.0/24'
    show_reachable_ips = False
    write_to_file = 'reachable_ips.txt'

    parser = argparse.ArgumentParser(description='A python script to scan on-line hosts into a LAN')
    pyname = sys.argv[0]
    parser.add_argument('-n', '--network', help='assign the network to scan, example: 192.168.0.0/24', type=str)
    parser.add_argument('-o', '--output-file', help='write on-line hosts to a file', type=str)
    parser.add_argument('-s', '--show-reachable-ips', help='you want to get the on-line hosts on the terminal', action="store_true")
    args = parser.parse_args()

    if args.network:
        network_ip = args.network

    if args.output_file:
        write_to_file = args.output_file

    if args.show_reachable_ips:
        show_reachable_ips = True

    return network_ip, show_reachable_ips, write_to_file


if __name__ == '__main__':
    network_ip, show_reachable_ips, filename = get_parameters()
    scanning_network_write_to_file(network_ip=network_ip, show_reachable_ips=show_reachable_ips, write_to_file=filename)
