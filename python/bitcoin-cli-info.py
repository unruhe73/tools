#!/usr/bin/env python3

import subprocess
import json

command = ['/usr/local/bin/bitcoin-cli', '-conf=/etc/bitcoin.conf', '-getinfo']
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

print()
command = ['bitcoin-cli', '-conf=/etc/bitcoin.conf', 'getblockchaininfo']
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
