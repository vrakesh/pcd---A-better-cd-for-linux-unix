from __future__ import print_function
import os
from getopt import getopt, GetoptError
import sys
class CmdArgs(object):
    __slots__ = ('_usage', '_sopts', '_dopts')
    def  __init__(self, usage, sopts, dopts):
        try:
            self._usage = str(usage)
            self._sopts = str(sopts)
            self._dopts = list(dopts)
        except Exception as ex:
            raise ValueError("Check the type of the values being initialized expecting str,str, list")
    def parseargs(self, argv):
        "Parse command line options."
        parsed = {}
        try:
            (opts, args) = getopt(argv[1:], self._sopts, self._dopts)
        except GetoptError as ex:
            print("error: %s" % str(ex), file = sys.stderr)
            sys.exit(1)

        for opt, arg in opts:
            if opt == '-h' or opt == '--help':
                parsed['help'] = True
            if opt == '-l' or opt == '--list':
                parsed['list'] = True

        if len(args) >= 1 and len(args) < 2 :
            parsed['pattern'] = args[0]

        return parsed


    def doHelp(self):
        fmtargs = {
            'cmd' : os.path.basename(sys.argv[0]),
        }
        return self._usage % fmtargs



