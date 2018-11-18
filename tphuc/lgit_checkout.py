from lgit_lib import *

def checkout(branch):
    """ git checkout with BRANCH only """


    # checkout if branch not exists
    if not os.path.isfile('.lgit/refs/heads/'+branch):
        print("error: pathspec '"+ branch + "' did not match any file(s) known to git.")
        return
    # check if we already on target branch
    if branch == read_file('.lgit/HEAD'):
        print("Already on '" + branch + "'")
        return


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
    files_modified = files_not_staged()
    for file in files_modified:
        if file_exist_on_branch(branch, file):
            print("error: Your local changes to the following files would be overwritten by checkout:\n\t",file)
            print("Please, commit your changes or stash them before you can switch branches.")
            print("Aborting")
            return
    for file in last_staged_files:
        if os.path.exists(file) and file not in files_modified:
            os.remove(file)

    print("Switched to branch '" + branch + "'")

    # we find the last snapshot of target branch and retrive contents from it
    # find the last commit/snapshots of branch
    commit = None
    with open('.lgit/refs/heads/'+branch, 'r') as f:
        commit = f.read()

    # retrive the contents thourgh all files of last previous snapshot
    data_index = []
    with open('.lgit/snapshots/'+commit,'r') as f:
        for line in f:
            data = line
            hash = data[:40] #  get sha1 hash
            filepath = data[41:-1] # get filename

            # rewrite the file :
            if len(filepath):
                with open(filepath, 'w') as f:
                    with open('.lgit/objects/'+hash[:2]+'/'+hash[2:], 'r') as f2:
                        f.write(f2.read()[:-1])
                arr = [format_time(time.time()),hash,hash,hash,filepath]
                data_index.append(" ".join(arr) + '\n')



    # rewrite index file
    with open('.lgit/index','w') as f:
        f.write("".join(data_index))

    # reset HEAD pointing to new branch
    with open('.lgit/HEAD','w') as f:
        f.write(branch)



def files_not_staged():
    lines = update_index()
    not_staged_changes = []
    committed = False

    for line in lines:
        arr = parse_index_line(line)
        if arr[1] != arr[3]:
            # added hash != current hash
            not_staged_changes.append(arr[-1])
    return not_staged_changes

def file_exist_on_branch(branch, file_check):
    commit = None
    with open('.lgit/refs/heads/'+branch,'r') as f:
        commit = f.read()

    with open('.lgit/snapshots/'+commit, 'r') as f:
        for line in f:
            filename = line.strip().split(' ')[-1]
            if filename == file_check:
                return True
    return False
