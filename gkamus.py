import os
import sys
import time
from termcolor import colored, cprint

print colored('\ngkamus says Hello!', 'green', attrs=['reverse', 'blink'])
print '\n\n'
# A very simple way to access the gkamus-id,gkamus-en files
# we just open the file and read until we find what we need.
# First we check if any entries start with the search word,
# if not we check if there are any entries containing the search word.
# Both indonesian and english files will be checked
# Since python is fast this works...
# Usage :  python gkamus.py  seteleah
#          python gkamus.py

global tc
tc = 0
global sl
sl = 0
theWord = ''


# terminal size code is from here:
# http://blog.taz.net.au/2012/04/09/getting-the-terminal-size-in-python/
def get_terminal_size(fd=1):
    """
    Returns height and width of current terminal. First tries to get
    size via termios.TIOCGWINSZ, then from environment. Defaults to 25
    lines x 80 columns if both methods fail.

    :param fd: file descriptor (default: 1=stdout)
    """
    try:
        import fcntl
        import termios
        import struct
        hw = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, '1234'))
    except:
        try:
            hw = (os.environ['LINES'], os.environ['COLUMNS'])
        except:
            hw = (25, 80)

    return hw


def get_terminal_height(fd=1):
    """
    Returns height of terminal if it is a tty, 999 otherwise

    :param fd: file descriptor (default: 1=stdout)
    """
    if os.isatty(fd):
        height = get_terminal_size(fd)[0]
    else:
        height = 999

    return height


def get_terminal_width(fd=1):
    """
    Returns width of terminal if it is a tty, 999 otherwise

    :param fd: file descriptor (default: 1=stdout)
    """
    if os.isatty(fd):
        width = get_terminal_size(fd)[1]
    else:
        width = 999

    return width


def gkamid(sw, switch):
    global tc
    global sl
    s = 1
    c = 0
    with open('gkamus-id.dict', 'r+') as f:
        while s <> '':
            s = f.readline()
            c += 1
            sl += 1
            if switch == 1:
                if s.startswith(sw):
                    lsx = colored(
                        str(c) + '-id  : \n', 'white') + colored(s, 'green')
                    print lsx
                    tc += 1
            else:
                if sw in s:
                    lsx = colored(
                        str(c) + '-id  : \n', 'white') + colored(s, 'green')
                    print lsx
                    tc += 1


def gkamen(sw, switch):
    global tc
    global sl
    s = 1
    c = 0
    with open('gkamus-en.dict', 'r+') as f:
        while s <> '':
            s = f.readline()
            c += 1
            sl += 1
            if switch == 1:
                if s.startswith(sw):
                    print colored(str(c) + '-en  : \n', 'white') + colored(s, 'cyan')

                    tc += 1
            else:
                if sw in s:
                    print colored(str(c) + '-en  : \n', 'white') + colored(s, 'cyan')
                    tc += 1


# main

if len(sys.argv) > 1:
    theWord = sys.argv[1]
while 1:
    start = time.clock()
    if theWord <> '':
        txWord = theWord
        theWord = ''
    else:
        tc = 0
        sl = 0
        print colored('-' * get_terminal_width(), 'yellow')
        txWord = raw_input(colored('\nWord/kata : ', 'yellow'))
        print '\n'

    gkamid(txWord, 1)
    gkamen(txWord, 1)

    # in case nothing found we do another search with containing
    if tc == 0:
        print colored('No words starts with          : ' + txWord + '\n\nResults for containing search :', 'yellow')
        print '\n'
        gkamid(txWord, 2)
        gkamen(txWord, 2)
        if tc == 0:
            print colored('      Kata ditemukan - Word not found in dictionary', 'red')

    end = time.clock()

    print '\n\nGkamus local lookup:\nSearch returned    : ', tc, ' entries', '\nTotal scanned      : ', sl, ' lines .  Duration  : ', end - start, ' secs.   | Ctrl-C to Quit'
