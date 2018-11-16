#!/usr/bin/env python3

from os import mkdir
from os import environ
def git_init():
    mkdir('.git')
    mkdir('.git/objects')
    mkdir('.git/commits')
    mkdir('.git/snapshots')
    with open('.git/index','w') as f:
        pass
    with open('.git/config','w') as f:
        f.write(environ['LOGNAME'])
    with open('.git/config', 'w') as f:
        f.write('master')
git_init()