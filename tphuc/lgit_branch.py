from lgit_lib import *

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
