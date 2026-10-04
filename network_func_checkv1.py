#!/bin/ !python

import sys, socket
import time

def Netfunc(timeout=5):
    """
    Reliable network check for systemd/cloud:
    - No ping
    - No ICMP
    - Uses TCP DNS connectivity
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.create_connection(("8.8.8.8", 53))
        print("Networks all good :)")
        return True
    except OSError:
        print("Waiting for network...")
        return False
    except Exception as e:
        print('{}'.format(e))
        sys.exit()

def ostronic():
    while not Netfunc():
        time.sleep(5)
    '''try:
        ostronics = 60*1
        _ostronics = [Netfunc() for ostronics in _ostronics if not time.thread_time() == ostronics]
        return _ostronics
        while not Netfunc():
            time.sleep(5)
    except Exception as e:
        print(f'{e}')'''


def Netfunc_():
    ''' We are only checking for the return code, in which case if it is not 0(successful ping of count 10), we print a prompt status to the screen.'''
    ostronics = subprocess.call(['ping', 'google.com', '-c', '10'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if ostronics != 0:
        print('\nCHECK YOUR NETWORK CONNECTION, VPN, OR CONNECT TO A WIFI NETWORK!!!')
        sys.exit(1)
    elif ostronics == 0:
        print('Networks all good :)')

if __name__ == '__main__':
    ostronic()
    Netfunc()
