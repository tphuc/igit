from lgit_lib import *

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
