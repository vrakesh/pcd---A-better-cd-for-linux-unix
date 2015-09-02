#!/usr/bin/env python

"""
Usage:
     <Script-alias> <directory-pattern>
"""
from __future__ import print_function, absolute_import
import os
import sys
from cmdargs import CmdArgs
from builtins import input
import signal
import colorama
from colorama import Fore, Back, Style
env_homedir = os.environ['HOME']
#ctrl-c and ctrl-z handler
def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT,signal_handler)
signal.signal(signal.SIGTSTP, signal_handler)

class Actions(object):
    """Actions to be performed by the command"""
    def __init__(self):
        """initialize database path and history size"""
        self.db_file = os.path.join(env_homedir, '.cdhist.db')
        self.HIST_SIZE = 1000
        self.hist_dict = {}
        self.history = None
    def absolute_path(self, partial):
        return os.path.abspath(
            os.path.join(os.getcwd(), os.path.expanduser(partial))
        )

    def search_pattern(self, pattern):
        plen = len(pattern)
        min_extra = float('Inf')
        match = None
        for directory in self.history:
            pos = directory.rfind(pattern)
            if pos >= 0:
                # how many extra characters?
                extra = len(directory) - pos - plen
                if extra <= min_extra:
                    min_extra = extra
                    match = directory
        return match or self.absolute_path(pattern)

    def read_history(self):
        if os.path.exists(self.db_file):
            with open(self.db_file) as fh:
                self.history = fh.read().split('\n')
                for i, item in enumerate(self.history):
                    self.hist_dict[item] = i
        else:
            self.history = []

    def list_history(self, pattern = ''):
        top_10 = self.history[:9]
        top_10 = top_10[::-1]
        return_list = list(top_10)
        #print(top_10)
        if (pattern != ''):
            top_10 = [s for s in top_10 if pattern in s]
            return_list = list(top_10)
            for i,s in enumerate(top_10):
                pos = s.rfind(pattern)
                top_10[i] = s[0:pos] + Fore.RED + Back.GREEN + s[pos:pos+len(pattern)] + Style.RESET_ALL + s[pos+len(pattern):]
        for i, item in enumerate(top_10):
            print(str(i+1), item, file = sys.stderr)
        print("Enter your choice:", file=sys.stderr)
        choice = int(input()) - 1
        return str(return_list[choice])


    def write_history(self):
        with open(self.db_file, 'w') as fh:
            if len(self.history) > (self.HIST_SIZE * 1.4):
                self.history = self.history[-self.HIST_SIZE:]
            fh.write('\n'.join(self.history))

    def save_match(self, match):
        idx = self.hist_dict.get(match)
        if idx is not None:
            self.history.pop(idx)
        self.history.append(match)
        self.write_history()

if __name__ == '__main__':
    usage = """\
    usage:
        %(cmd)s -h (or --help)
        %(cmd)s -l (or --list)
        %(cmd)s <pattern/absolute-path>

    -h              show help text
    -l              list history of last 10 directories
    pattern         after first search short version
    absolute path   absolute path of the directory to work like cd
    """
    sopts = 'hl'
    dopts = ['help','list']
    act = Actions()
    if not len(sys.argv) > 1:
        # on typing just the script-name go to user home
        print('cd %s' % env_homedir)
        sys.exit(0)
    args_handler = CmdArgs(usage, sopts, dopts)
    #Handle help for the script
    params = args_handler.parseargs(sys.argv)
    if 'help' in params:
        print(args_handler.doHelp(), file=sys.stderr)
        sys.exit(0)

    act.read_history()
    #Handle listing of top 10 history
    if 'list' in params:
       if 'pattern' in params:
            directory = act.list_history(params['pattern'])
       else:
            directory = act.list_history()
       if os.path.isdir(act.absolute_path(directory)):
            act.save_match(act.absolute_path(directory))
            print('cd %s' % (act.absolute_path(directory)))
            sys.exit(0)
       else:
           print("Unexpected error", file =sys.stderr)
           sys.exit(1)
    #handle pattern match
    required_ok = 'pattern' in params
    if not required_ok:
        print(args_handler.doHelp(), file=sys.stderr)
        sys.exit(1)

    pattern = params['pattern']
    match = act.absolute_path(pattern)

    if os.path.isdir(match):
        # Handle the case with absolute path
        act.save_match(match)
    else:
        # Perform a search for a pattern
        match = act.search_pattern(pattern)
        if os.path.isdir(match):
            act.save_match(match)
        else:
            match = pattern
    print('cd %s' % (match))
