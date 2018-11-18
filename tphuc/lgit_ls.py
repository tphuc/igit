from lgit_lib import *

def ls_files():
    # ls-files in current folder
    lines = read_index_file()
    # Get current folder path by subtract its realpath with lgit_parent path
    current_folder = os.path.realpath('.')\
        .replace(LGIT_PARENT_PATH, '')\
        .strip('/')

    # Remove current folder name to get only filenames
    file_names = [x.split()[-1].replace(current_folder, '').strip('/')
                  for x in lines if current_folder in x]

    # Sort output
    file_names.sort()
    return file_names
