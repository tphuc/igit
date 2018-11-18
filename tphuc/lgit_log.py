from lgit_lib import *
def log_commit():
    # Get commits from /commits
    commits = os.listdir(COMMITS_PATH)
    commits.sort(key=lambda x: float(x), reverse=True)
    content = []
    for commit_name in commits:
        with open('%s/%s' % (COMMITS_PATH, commit_name)) as f:
            # Make a line as provided format
            arr = ['commit ' + commit_name + '\n', 'Author: ' + f.readline(),
                   'Date: ' + format_time_from_string(
                       f.readline().strip('\n')), f.readline(),
                   '\t' + f.readline()]
            content.append(''.join(arr))

    if content:
        print('\n\n'.join(content))
