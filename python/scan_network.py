#!/usr/bin/env python3

import platform    # let you get the operating system name
import subprocess  # let you execute a shell command
from progress.bar import Bar
from time import sleep


def scanning_network(base_ip = '192.168.0', show_reachable_ips=False):
    if not show_reachable_ips:
        bar = Bar('Processing', max=254)
    ips = []
    if platform.system().lower() == 'windows':
        packets_opt = '-n'
    else:
        packets_opt = '-c'

    i = 1
    while i < 255:
        new_ip = f'{base_ip}.{i}'
        command = ['ping', packets_opt, '1', '-W1', new_ip ]
        try:
            if subprocess.run(args=command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                if show_reachable_ips:
                    print(f'{base_ip}.{i} reachable')
                ips.append(new_ip)
        except KeyboardInterrupt:
            break
        if not show_reachable_ips:
            bar.next()
        i += 1
    bar.finish()
    return ips


def scanning_network_write_to_file(base_ip = '192.168.0', show_reachable_ips=False, write_to_file='reachable_ips.txt'):
    ip_hosts = scanning_network(show_reachable_ips=False)
    if len(ip_hosts) > 0:
        if write_to_file:
            with open(write_to_file, 'w+') as f:
                f.write('\n'.join(ip_hosts))
            print(f'See file {write_to_file} for output')
        else:
            sleep(2)
            print('reachable IPs:')
            for ip in ip_hosts:
                print(ip)
    else:
        print('No reachable IPs')


scanning_network_write_to_file()