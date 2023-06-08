#!/usr/bin/env python3

import ipaddress
import platform    # let you get the operating system name
import subprocess  # let you execute a shell command
from progress.bar import Bar
from time import sleep


def scanning_network(base_ip='192.168.0.0/24', show_reachable_ips=False):
    ips = []
    try:
        network_ipv4 = ipaddress.IPv4Network(base_ip)
    except ValueError:
        print('address/netmask is invalid for IPv4:', base_ip)
        return ips

    print(f"I'm going to scan {base_ip} network")
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
    bar.finish()
    return ips


def scanning_network_write_to_file(base_ip='192.168.0.0/24', show_reachable_ips=False, write_to_file='reachable_ips.txt'):
    ip_hosts = scanning_network(base_ip=base_ip, show_reachable_ips=False)
    if len(ip_hosts) > 0:
        if write_to_file:
            with open(write_to_file, 'w+') as f:
                f.write('\n'.join(ip_hosts))
                f.write('\n')
            print(f'See file {write_to_file} for output')
        else:
            sleep(2)
            print('reachable IPs:')
            for ip in ip_hosts:
                print(ip)
    else:
        print('No reachable IPs')


scanning_network_write_to_file()
