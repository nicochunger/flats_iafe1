#!/usr/bin/env python

import shlex, subprocess
import platform
import sys
import os
from os.path import expanduser

base = os.environ.get('ASTROCLI', expanduser("~/astrocli"))
lib_path = os.path.abspath(os.path.join(base, 'other'))
sys.path.append(lib_path)
import activityLog

def help():
    print
    print "Usage:\n"
    print "\tsetFilter <clear|u|b|v|r|i>\n"

def main(argv):

    if len(argv) == 1:
        filter = argv[0].lower()
        filtern = -1

        pc = platform.node().lower()
        print pc

        if pc == 'iafe1':
            if filter == 'clear':
                filtern = 1
            elif filter == 'u':
                filtern = 2
            elif filter == 'b':
                filtern = 3
            elif filter == 'v':
                filtern = 4
            elif filter == 'r':
                filtern = 5
            elif filter == 'i':
                filtern = 6
        elif pc == 'iafe2':
            if filter == 'clear':
                filtern = 4
            elif filter == 'b':
                filtern = 3
            elif filter == 'v':
                filtern = 2
            elif filter == 'r':
                filtern = 1
            elif filter == 'i':
                filtern = 5
        elif pc == 'mate':
            if filter == 'clear':
                filtern = 4
            elif filter == 'b':
                filtern = 3
            elif filter == 'v':
                filtern = 2
            elif filter == 'r':
                filtern = 1
            elif filter == 'i':
                filtern = 5

        if filtern == -1:
            help()
        else:
            activityLog.log('(II) Setting filter to ' + argv[0])
            if pc == 'iafe1':
                subprocess.call(shlex.split('/opt/apogee/bin/selectfilter -t 2 -p ' + str(filtern)))
            elif pc == 'mate':
                subprocess.call(shlex.split('setfilter ' + str(filtern)))

            f = open('/tmp/lastFilter', 'w')
            f.write(filter)
            f.close()

    else:
        help()

if __name__ == "__main__":
    main(sys.argv[1:])
