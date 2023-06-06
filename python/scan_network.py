#!/usr/bin/env python3

import platform    # let you get the operating system name
import subprocess  # let you execute a shell command

if platform.system().lower() == 'windows':
    packets_opt = '-n'
else:
    packets_opt = '-c'

base_ip = '192.168.0'
i = 1
while i < 255:
    command = ['ping', packets_opt, '1', f'{base_ip}.{i}']
    try:
        if subprocess.run(args=command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            print(f'{base_ip}.{i} reachable')
    except KeyboardInterrupt:
        break
    i += 1
