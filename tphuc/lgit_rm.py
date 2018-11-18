from lgit_lib import *

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
