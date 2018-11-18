import hashlib
import os
from glob import glob
import time
import datetime
import os.path

def read_file(_path):
    with open(_path,'r') as f:
        return f.read()

def write_file(_path, content, mode='w'):
    # Write content to _path
    if content:
        with open(_path, mode) as f:
            f.write('\n'.join(content) + '\n')

def get_hash(filepath):
    # Return content and hash code of a file
    content = read_file(LGIT_PARENT_PATH + '/' + filepath)
    return content, hashlib.sha1(content.encode()).hexdigest()
""" --------------------------time -------------------------"""
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

""" -------------------index file -------------------------"""
def read_index_file(read_name=False):
    """
    Read index file content
    If read_name=True, return only file names
    """
    lines = read_file(INDEX_PATH).split('\n')[:-1]
    if read_name:
        lines = [x.split()[-1] for x in lines]
    return lines

def parse_index_line(line):
    # Parse a line in /index to a list
    timestamp = line[:14]
    curr_hash = line[15:55]
    added_hash = line[56:96]
    commit_hash = line[97:137]
    file_name = line[138:]
    return [timestamp, curr_hash, added_hash, commit_hash, file_name]

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
""" ------------------------------------------------- """

def get_lgit_path():
    # Find lgit path if exist in the current directory or its parents
    _path = os.path.realpath('.')
    while _path:
        if os.path.exists(_path + '/.lgit'):
            return _path, _path + '/.lgit'
        _path = '/'.join(_path.split('/')[:-1])
    return None, None

def save_commit_information(author, c_time, _message):
    # Save author, timestamp, message to /commits/c_time
    content = ['%s\n%s\n\n%s\n' % (author, c_time.split('.')[0], _message)]
    write_file('%s/%s' % (COMMITS_PATH, c_time), content)

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

""" ----------------------config----------------------"""
def set_author_name(author_name):
    # Set author name in config
    content = [author_name + '\n']
    write_file(CONFIG_PATH, content)

#########################################################
def get_author_name():
    # Get author name from config
    author = read_file(CONFIG_PATH).strip('\n')
    return author

def get_untracked_files():
    # Get untracked files in current dir that not in index
    curr_files = os.listdir('.')
    index_names = read_index_file(read_name=True)
    index_names = [x.split('/')[0] for x in index_names]
    return [x for x in curr_files if x not in index_names]

def list_files(_path):
    # List all file in a path recursively
    result = [y for x in os.walk(_path)
              for y in glob(os.path.join(x[0], '*'))] \
             + [y for x in os.walk(_path)
                for y in glob(os.path.join(x[0], '.*'))]
    return [i for i in result if os.path.isfile(i) or os.path.islink(i)]


# Get .lgit path and its parent dir
LGIT_PARENT_PATH, LGIT_PATH = get_lgit_path()
INDEX_PATH = '%s/index' % LGIT_PATH
OBJECT_PATH = '%s/objects' % LGIT_PATH
SNAPSHOTS_PATH = '%s/snapshots' % LGIT_PATH
COMMITS_PATH = '%s/commits' % LGIT_PATH
CONFIG_PATH = '%s/config' % LGIT_PATH
UNTRACKED_MESSAGE = "Untracked files:\n  (use \"./lgit.py add <file>...\" " \
                    "to include in what will be committed)\n"
NO_CHANGE_MESSAGE = "no changes added to commit (use \"./lgit.py " \
                    "add and/or \"./lgit.py commit -a\")"
NOT_STAGED_MESSAGE = "Changes not staged for commit:\n  (use \"./lgit.py add "\
                    "...\" to update what will be committed)\n  (use " \
                    "\"./lgit.py checkout -- ...\" to discard changes in " \
                    "working directory)\n "
STAGED_MESSAGE = "Changes to be committed:\n  (use \"./lgit.py reset HEAD" \
                 " ...\" to unstage)\n"
NOTHING_TO_COMMIT_MESSAGE = "nothing to commit (create/copy files and " \
                            "use \"./lgit.py add\" to track)\n"
