#!/usr/bin/env python3

import subprocess
import json

bitcoin_cli = '/usr/local/bin/bitcoin-cli'

command = [bitcoin_cli, '-conf=/etc/bitcoin.conf', '-getinfo']
try:
    res = subprocess.run(args=command, capture_output=True)
    output = res.stdout.decode('UTF-8')
    ret_value = res.returncode

    getinfo = {}
    if ret_value == 0:
        lines = output.split('\n')
        for line in lines:
            if line:
                item = line.split(':')
                getinfo[item[0].strip()] = item[1].strip()
        print(5*'*' + ' getinfo:')
        for i in getinfo.keys():
            print(i + ': ' + str(getinfo[i]))
    else:
        print('Error!')
except FileNotFoundError:
    print(bitcoin_cli + ': command not found!')

print()
command = [bitcoin_cli, '-conf=/etc/bitcoin.conf', 'getblockchaininfo']
try:
    res = subprocess.run(args=command, capture_output=True)
    output = res.stdout.decode('UTF-8')
    ret_value = res.returncode

    if ret_value == 0:
        getblockchaininfo = json.loads(output)
        print(5*'*' + ' getblockchaininfo:')
        for i in getblockchaininfo.keys():
            print(i + ': ' + str(getblockchaininfo[i]))
    else:
        print('Error!')
except FileNotFoundError:
    print(bitcoin_cli + ': command not found!')