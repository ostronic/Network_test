#!/bin/ !python

import sys, subprocess

def Netfunc():
    ''' We are only checking for the return code, in which case if it is not 0(successful ping of count 10), we print a prompt status to the screen.'''
    ostronics = subprocess.run(['ping', 'google.com', '-c', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if not ostronics==0:
        print('CHECK YOUR NETWORK CONNECTION, VPN, OR CONNECT TO A WIFI NETWORK!!!')
        sys.exit(1)
    return

if __name__ == '__main__':
    Netfunc()