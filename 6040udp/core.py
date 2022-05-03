"""
Python program that connects to Heimann HTPA sensors given their IP addresses (in settings file) and records data captured to TXT files. 
Supports recording mutliple sensors at the same time. This tool is supposed to help developing multi-view thermopile sensor array monitoring system.
"""
import socket
import os
import sys
#import threading  # http://www.g-loaded.eu/2016/11/24/how-to-terminate-running-python-threads-using-signals/
import time
#import datetime
#import signal
from pathlib import Path
import struct

import HTPAinterface
#import IMGinterface

'''
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".

    Credit: https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
'''

def main():
    print('Starting main program')
    HTPAinterface.call_HTPA()
    HTPAinterface.bind_HTPA()
    HTPAinterface.stream_HTPA(0)
    

if __name__ == "__main__":
    main()
