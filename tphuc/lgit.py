#!/usr/bin/env python3
import sys

from lgit_add import *
from lgit_commit import *
from lgit_init import *
from lgit_log import *
from lgit_rm import *
from lgit_status import *
from lgit_branch import *
from lgit_checkout import *


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit()

    command = sys.argv[1]
    arg_1 = sys.argv[2] if len(sys.argv) > 2 else None
    arg_2 = sys.argv[3] if len(sys.argv) > 3 else None

    if command == 'init':
        if LGIT_PATH is None:
            init()
        else:
            print("Git repository already initialized.")
    else:
        if LGIT_PATH is None:
            print("fatal: not a git repository "
                  "(or any of the parent directories)")
        else:
            if command == 'branch':
                branch(sys.argv[2])
            elif command == 'checkout':
                checkout(sys.argv[2])
            elif command == 'add':
                for path in sys.argv[2:]:
                    add(path)
            elif command == 'commit':
                if arg_2 and arg_1 == '-m':
                    message = arg_2
                    commit(message)
                else:
                    status()
            elif command == 'status':
                status()
            elif command == 'config' and arg_1 == '--author':
                set_author_name(arg_2)
            elif command == 'ls-files':
                files = ls_files()
                if files:
                    print('\n'.join(files))
            elif command == 'rm':
                for path in sys.argv[2:]:
                    rm_file(path)
            elif command == 'log':
                log_commit()
            else:
                print("git: '%s' is not a git command. See 'git --help'."
                      % command)
