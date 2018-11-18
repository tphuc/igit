from lgit_lib import *

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
