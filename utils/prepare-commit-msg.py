#!/usr/bin/env python

# This script is intended to be used a a git hook and will prepend the ticket
# number to a commit message in the correct format for Github/Gitlab to parse.
#
# To use, create a shortcut to this file in .git/hooks called
# 'prepare-commit-msg' e.g. from top folder of your project:
#     cd .git/hooks
#     ln -s ./utils/prepare-commit-msg.py prepare-commit-msg
#
# TODO - the above doesn't work on Windows

import sys
import re
from subprocess import check_output

# By default, the hook will check to see if the branch name starts with
# 'issue-' and will then prepend whatever follows in the commit message.
# e.g. for a branch named 'issue-123', the commit message will start with
# '[#123]'
# If you wish to use a diferent prefix on branch names, change it here.
issue_prefix = 'issue-'

commit_msg_filepath = sys.argv[1]
branch = check_output(
    ['git', 'symbolic-ref', '--short', 'HEAD']
).strip().decode(encoding='UTF-8')

if branch.startswith(issue_prefix):
    issue_number = re.match('%s(.*)' % issue_prefix, branch).group(1)
    print("prepare-commit-msg: Prepending [#%s] to commit message" % issue_number)

    with open(commit_msg_filepath, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write("[#%s] %s" % (issue_number, content))
else:
    print("prepare-commit-msg: No changes made to commit message")
