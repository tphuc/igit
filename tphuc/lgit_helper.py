import hashlib
import os
from glob import glob
import time
import datetime


def read_file(_path):
    with open(_path,'r') as f:
        return f.read()


def write_file(_path, content, mode='w'):
    # Write content to _path
    if content == '':
        with open(_path, mode) as f:
            pass
    else:
        with open(_path, mode) as f:
                f.write('\n'.join(content) + '\n')


def read_index_file(read_name=False):
    """
    Read index file content
    If read_name=True, return only file names
    """
    lines = read_file(INDEX_PATH).split('\n')[:-1]
    if read_name:
        lines = [x.split()[-1] for x in lines]
    return lines


def print_pathspec_error(_path):
    print("fatal: pathspec '%s' did not match any files" % _path)


def get_hash(filepath):
    # Return content and hash code of a file
    content = read_file(LGIT_PARENT_PATH + '/' + filepath)
    return content, hashlib.sha1(content.encode()).hexdigest()


def get_lgit_path():
    # Find lgit path if exist in the current directory or its parents
    _path = os.path.realpath('.')
    while _path:
        if os.path.exists(_path + '/.lgit'):
            return _path, _path + '/.lgit'
        _path = '/'.join(_path.split('/')[:-1])
    return None, None


def format_time(timestamp, floating=False):
    # Return a formatted string from a timestamp
    if floating:
        return datetime.datetime.utcfromtimestamp(timestamp) \
            .strftime("%Y%m%d%H%M%S.%f")
    return datetime.datetime.utcfromtimestamp(timestamp) \
        .strftime("%Y%m%d%H%M%S")


def format_time_from_string(time_string):
    # Return ctime from string
    return datetime.datetime.strptime(time_string, "%Y%m%d%H%M%S").ctime()


def parse_index_line(line):
    # Parse a line in /index to a list
    timestamp = line[:14]
    curr_hash = line[15:55]
    added_hash = line[56:96]
    commit_hash = line[97:137]
    file_name = line[138:]
    return [timestamp, curr_hash, added_hash, commit_hash, file_name]


def init():
    # Make dir structure
    os.mkdir('.lgit')
    os.mkdir('.lgit/objects')
    os.mkdir('.lgit/commits')
    os.mkdir('.lgit/snapshots')
    with open('.lgit/index', 'w'):
        pass
    with open('.lgit/config', 'w') as f:
        f.write(os.environ['LOGNAME'] + '\n')
    os.mkdir('.lgit/refs')
    os.mkdir('.lgit/refs/heads')
    with open('.lgit/HEAD', 'w') as f:
        f.write('master')
    with open('.lgit/refs/heads/master', 'w') as f:
        pass


def add(_path):
    # lgit add: add a file to .lgit folder with name is its hash
    if os.path.isfile(_path):
        # If it's a file, get its content and hash code
        content, hash_code = get_hash(_path)

        # Check whether first 2 hash folder is exist, delete.
        in_path = '.lgit/objects/' + hash_code[0:2]
        if not os.path.exists(in_path):
            os.mkdir(in_path)

        # Make a copy of the file to objects folder
        out_path = '.lgit/objects/%s/%s' % (hash_code[0:2], hash_code[2:])
        write_file(out_path, [content])

        # Update index file
        update_index(_path)
    else:
        # If _path is a folder, for every files in it, add those files.
        if os.path.exists(_path):
            files = list_files(_path)
            for file in files:
                add(file)
        else:
            # Else, print a error
            print_pathspec_error(_path)


def update_index(filename=None):
    """
    Update /index and return /index after update
    If file_name is specify, add or update file_name in /index
    If not, update_index was called by status, only update /index file
    """
    content = []  # holding index content after modify
    lines = read_index_file()  # /index content

    filenames = [x.split()[-1] for x in lines]  # filenames in /index

    if filename and filename not in filenames:
        # File doesn't exist, append
        _, hash_code = get_hash(filename)
        time_stamp = format_time(os.path.getmtime(filename))
        arr = [time_stamp, hash_code, hash_code, ' ' * 40, filename]
        content = lines + [' '.join(arr)]
        write_file(INDEX_PATH, content)
    else:
        # File exist, update
        for line in lines:  # For line in index content
            arr = parse_index_line(line)  # Fields in a line
            _, arr[1] = get_hash(arr[-1])  # re-hash to update current content

            if filename and arr[-1] == filename:
                # Update added hash
                arr[2] = arr[1]

            content.append(' '.join(arr))
        if content != '   ':
            write_file(INDEX_PATH, content)

    return content


def status():
    """
    Read /index, re-hash current files in it, compare to find which was
    changed from when they was added, which is not changed in staged for commit
    """
    lines = update_index()
    staged_changes = []
    not_staged_changes = []
    committed = False

    for line in lines:
        arr = parse_index_line(line)
        if not arr[3].strip():
            # If added stages not commit, add to staged changes
            staged_changes.append(arr[-1])
        else:
            committed = True

        if arr[1] != arr[2]:
            # added hash != current hash
            not_staged_changes.append(arr[-1])

    # Print output
    print("On branch master")
    if not committed:
        print("\nNo commits yet\n")

    if not staged_changes and not not_staged_changes:
        print(NOTHING_TO_COMMIT_MESSAGE)

    # Print Staged changes
    if staged_changes:
        print(STAGED_MESSAGE)
        for change in staged_changes:
            print("\tmodified: %s" % change)
        print()

    # Print Not staged changes
    if not_staged_changes:
        print(NOT_STAGED_MESSAGE)
        for change in not_staged_changes:
            print("\tmodified: %s" % change)
        print()

        if not staged_changes:
            print(NO_CHANGE_MESSAGE)

    # Print untracked files
    untracked_files = get_untracked_files()
    if untracked_files:
        print(UNTRACKED_MESSAGE)
        for file in untracked_files:
            print('\t' + file)





def save_snapshots(c_time):
    # Save added stages to snapshots/c_time, update commit_field in /index
    lines = read_index_file()
    snaps_content = []
    index_content = []

    for line in lines:
        # Get fields in index line
        arr = parse_index_line(line)

        # Get add hash and file name to save to snapshots
        added_hash = arr[2]
        file_name = arr[-1]

        arr[3] = added_hash  # commit hash = added hash

        snaps_content.append(added_hash + ' ' + file_name)
        index_content.append(' '.join(arr))

    # Save index
    write_file(INDEX_PATH, index_content)
    # Save snapshots
    write_file('%s/%s' % (SNAPSHOTS_PATH, c_time), snaps_content)







def rm_file(_path):
    """
    Remove file _path if it in index
    Update the index file after removed
    """
    # Read file names in index
    lines = read_index_file()
    file_names = [x.split()[-1] for x in lines]

    if _path in file_names:
        if os.path.isfile(_path):
            # Remove file
            os.remove(_path)

            # Remove that file from index
            ind = file_names.index(_path)
            lines.pop(ind)
            write_file(INDEX_PATH, lines)
        else:
            # If _path is a folder, for every files in it, remove those files.
            if os.path.exists(_path):
                files = list_files(_path)
                for file in files:
                    rm_file(file)
            else:
                # Else, print a error
                print_pathspec_error(_path)
    else:
        print_pathspec_error(_path)










def branch(_path):
    """ create new branch """
    # check if new branch is exists
    if os.path.exists('.lgit/refs/heads/'+_path):
        print('fatal: A branch named',_path,'already exists.')
        return  # do nothing

    # get the last branch
    last_branch = None
    with open('.lgit/HEAD','r') as f:
        last_branch = f.read()

    # get the last commmit
    last_commit = None
    with open('.lgit/refs/heads/'  +last_branch,'r') as f:
        last_commit = f.read()


    # copy last commit to new branch
    with open('.lgit/refs/heads/' + _path,'w') as f:
        f.write(last_commit)



def checkout_branch(branch):

    """ git checkout with BRANCH only """

    # checkout if branch not exists
    if not os.path.isfile('.lgit/refs/heads/'+branch):
        print("error: pathspec '"+ branch + "' did not match any file(s) known to git.")
    # check if we already on target branch
    if branch == read_file('.lgit/HEAD'):
        print("Already on '" + branch + "'")

    """ at first we need to delete all staged files from previous branch """
    # get the last branch
    last_branch = None
    with open('.lgit/HEAD','r') as f:
        last_branch = f.read()

    # get all staged files of last branch
    last_staged_files = []
    with open('.lgit/refs/heads/' + last_branch, 'r') as f:
        last_snapshot = f.read()
        with open('.lgit/snapshots/' + last_snapshot, 'r') as f_:
            for line in f_:
                if line[41:-1]:
                    last_staged_files.append(line[41:-1])

    # remove all the staged files
    # " we could do 'rsync' for later but i'm lazy
    # so later we have to rewrite all the files :p "
    for file in last_staged_files:
        if os.path.exists(file):
            os.remove(file)



    # we find the last snapshot of target branch and retrive contents from it
    # find the last commit/snapshots of branch
    commit = None
    with open('.lgit/refs/heads/'+branch, 'r') as f:
        commit = f.read()

    # retrive the contents thourgh all files of last previous snapshot
    with open('.lgit/snapshots/'+commit,'r') as f:
        for line in f:
            data = line
            hash = data[:40] #  get sha1 hash
            filepath = data[41:-1] # get filename

            # rewrite the file :
            if len(filepath):
                with open(filepath, 'w') as f:
                    with open('.lgit/objects/'+hash[:2]+'/'+hash[2:], 'r') as f2:
                        f.write(f2.read())

    # reset HEAD pointing to new branch
    with open('.lgit/HEAD','w') as f:
        f.write(branch)
