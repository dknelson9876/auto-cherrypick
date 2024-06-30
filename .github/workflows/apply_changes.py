import sys
import subprocess
import re

def get_trailer_value(message_file):
    with open(message_file, 'r') as file:
        message = file.read()
    match = re.search(r'applies-to:\s*(\w+)', message)
    if match:
        return match.group(1)
    return None

def get_current_branch():
    result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
    return result.stdout.strip()

def cherry_pick_commit(branch, commit):
    subprocess.run(['git', 'checkout', branch])
    subprocess.run(['git', 'cherry-pick', commit])
    subprocess.run(['git', 'commit', '--amend', '--no-edit'])

def main():
    if len(sys.argv) != 2:
        print("Usage: python apply_changes.py <commit_message_file>")
        sys.exit(1)

    commit_message_file = sys.argv[1]
    trailer_value = get_trailer_value(commit_message_file)

    if not trailer_value:
        print("No 'applies-to' trailer found in the commit message.")
        sys.exit(0)

    current_branch = get_current_branch()
    commit_hash = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()

    branches = []
    if trailer_value == 'personal':
        branches = ['frost']
    elif trailer_value == 'all':
        branches = ['frost', 'main']

    for branch in branches:
        cherry_pick_commit(branch, commit_hash)

    subprocess.run(['git', 'checkout', current_branch])

if __name__ == '__main__':
    main()
