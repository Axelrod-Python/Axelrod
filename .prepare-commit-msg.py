#!/usr/bin/env python

# This script is an optional git hook and will prepend the issue
# number to a commit message in the correct format for Github to parse.
#
# If you wish to use it, create a shortcut to this file in .git/hooks called
# 'prepare-commit-msg' e.g. from top folder of your project:
#   ln -s ./.prepare-commit-msg.py .git/hooks/prepare-commit-msg
#
# or, for Windows users:
#   mklink .git\hooks\prepare-commit-msg .prepare-commit-msg.py
#
# If you use a graphical git client, you can configure it so that the issue
# numbers become clickable in the log view. e.g. for Atlassian SourceTree:
#   From the 'Repository Settings' menu, click the 'Advanced' tab
#   In the 'Commit Text Replacements', click the 'Add' button
#   Select 'Other' as the 'Replacement Type'
#   Enter '#(\d{1,})' as the 'Regex Pattern'
#   Enter '<a href="https://github.com/Axelrod-Python/Axelrod/issues/$1">#$1</a>' as the 'Replace With'
#
# Any issue numbers created by this hook (or entered manually in the correct)
# format will now be clickable links in the log view.

import re
import sys
from subprocess import check_output

# By default, the hook will check to see if the branch name starts with
# 'issue-' and will then prepend whatever follows in the commit message.
# e.g. for a branch named 'issue-123', the commit message will start with
# '[#123]'
# If you wish to use a diferent prefix on branch names, change it here.
issue_prefix = "issue-"

commit_msg_filepath = sys.argv[1]
branch = (
    check_output(["git", "symbolic-ref", "--short", "HEAD"])
    .strip()
    .decode(encoding="UTF-8")
)

if branch.startswith(issue_prefix):
    issue_number = re.match("%s(.*)" % issue_prefix, branch).group(1)
    print(
        "prepare-commit-msg: Prepending [#%s] to commit message" % issue_number
    )

    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        f.seek(0, 0)
        f.write("[#%s] %s" % (issue_number, content))
else:
    print("prepare-commit-msg: No changes made to commit message")
