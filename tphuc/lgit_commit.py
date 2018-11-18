from lgit_lib import *

def commit(_message):
    # Save commit information and snapshots
    author = get_author_name()
    if author:
        c_time = format_time(time.time(), floating=True)
        save_commit_information(author, c_time, _message)
        save_snapshots(c_time)

    # get the branch which HEAD pointing to
    current_head = read_file('.lgit/HEAD')
    """
    update the last commit/snapshot of branch,
    so we can use that to switch between branch
    """
    with open('.lgit/refs/heads/' + current_head,'w') as f:
        f.write(c_time)
