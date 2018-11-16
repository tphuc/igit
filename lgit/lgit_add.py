#!/usr/bin/env python3
import pathlib
import os.path
import time,datetime
from os import mkdir
from timestamp import *
from sha1 import *
import argparse

def content(filepath):
    with open(filepath,'r') as f:
        return f.read()

def git_add(args):
    """ git add with list of file path as argument """
    
    # Check if initialized git
    if not os.path.exists('.git/objects'):
        print('fatal: not a git repository (or any of the parent directories): .git')
        return

    # check if args is empty directory
    if not len(args):
        return
    
    ##############################
    for file in args:
        update_git_object(file)
        update_git_index(file)
        

def update_git_object(file):
    Git_Obj_Dir = '.git/objects'
    sha1_str = sha1(file)

    # check if encountered the same directory 
    if not os.path.isdir(Git_Obj_Dir + '/' + sha1_str[:2]):
        os.mkdir(Git_Obj_Dir + '/' + sha1_str[:2])
    
    # check if encountered the same file
    if not os.path.isfile(Git_Obj_Dir + '/' + sha1_str[:2] + '/' + sha1_str[2:]):
        f = open(Git_Obj_Dir + '/' + sha1_str[:2] + '/' + sha1_str[2:], 'w+')
        f.write(content(file))
        f.close()


def update_git_index(file):
    Git_Index = '.git/index'
    seek_pos = 0
    file_exist = False

    with open(Git_Index, 'r') as f:
        for line in f:
            if line.find(file) < 0:
                seek_pos += len(line)
            else:
                file_exist = True
                break


    with open(Git_Index, 'r+b') as f:
        f.seek(seek_pos)
        if not file_exist:
            f.write(make_string(str(timestamp()), sha1(file), sha1(file), ' '*40, file))
        else:
            f.write(make_string(str(timestamp()), sha1(file), sha1(file)))


def make_string(*args, sep=' ', b=True):
    s = ''
    for arg in args:
        s += arg
        s += sep
    s = s[:-1] + '\n'
    return s.encode()

parser = argparse.ArgumentParser()
parser.add_argument('files',nargs='+')
args = vars(parser.parse_args())
git_add(args['files'])
