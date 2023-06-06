#!/usr/bin/env python3

import platform    # let you get the operating system name
import subprocess  # let you execute a shell command


def scanning_network(base_ip = '192.168.0', show_reachable_ips=False):
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
            print(end='.', flush=True)
        i += 1
    print()
    return ips


ip_hosts = scanning_network(show_reachable_ips=False)
print('reachable IPs:')
for ip in ip_hosts:
    print(ip)