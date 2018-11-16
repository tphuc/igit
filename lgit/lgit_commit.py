#!/usr/bin/env python3
import os.path
from os import environ
from os import mkdir
from timestamp import *
from sha1 import *
import argparse

def content(filepath):
    with open(filepath,'r') as f:
        return f.read()

def git_commit(message):
    """ perfrom git commit -m [message] """


    # check if git index is empty or not
    with open('.git/index', 'r') as f:
        data = f.read()
        if not len(data):
            # Output error message
            return
        f.close()
    
    time = timestamp(mili=True, str_type=False)
    LOGNAME = environ['LOGNAME']

    # update .git/commits directory
    with open('.git/commits' + '/' + str(time), 'w') as f:
        #.write(LOGNAME + '\n' + str(int(time)) + '\n' + '\n' + message + '\n')
        f.write('\n'.join([LOGNAME, str(int(time)), '', message]))
    # update .git/index
    update_git_index()

    # update snapshot
    update_snap_shot(str(time))

    current_head = content('.git/HEAD')
    with open('.git/refs/heads/' + current_head,'w') as f:
        f.write(str(time))
    
    
            

def update_git_index():
    seek_pos = 0
    line_pos = 0
    with open('.git/index', 'r+') as f:
        for line in f:
            seek_pos = line.find(' ', 80) + 1
            f.seek(seek_pos + line_pos,0)
            f.write(line[seek_pos-41:seek_pos-1])
            line_pos += len(line)
            f.seek(line_pos,0)

def update_snap_shot(time):
    with open('.git/snapshots/' + time, 'w') as f:
        with open('.git/index', 'r') as f_index:
            data = f_index.read().split('\n')
            for line in data:
                f.write(line[line.find(' ',80)+1:]+'\n')

parser = argparse.ArgumentParser()
parser.add_argument('messages', nargs = '+')
args = vars(parser.parse_args())

git_commit(args['messages'][0])