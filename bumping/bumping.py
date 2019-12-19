'''
Python tool to calculate SemVer based on conventional git commit messages.

Usage: bumping [options]

Options:
    -r=REPO --repo=REPO     Path to the repository's root directory
                            [Default: .]
    -h --help               Print this help text
    -v --version            Print the version number
'''

import os
import re
import docopt

from git import Repo

from bumping import __version__


_prog = re.compile(r'^([^\(\)]+?)(\([^\(\)]+\))?: [\s\S]+$')


_increment_map = {
    'BREAKING CHANGE': (1, 0, 0),
    'feat': (0, 1, 0),
    'fix': (0, 0, 1),
}


def get_commit_type(message: str) -> str:
    m = _prog.match(message)
    if m:
        return m.group(1)


def get_increment(type: str) -> tuple:
    return _increment_map.get(type, None)


def get_commit_increment(message: str) -> tuple:
    type = get_commit_type(message)
    return get_increment(type)


def increase_version(v, inc):
    if inc[0]:
        return (v[0] + inc[0], 0, 0)
    elif inc[1]:
        return (v[0], v[1] + inc[1], 0)
    else:
        return (v[0], v[1], v[2] + inc[2])


def get_commit_increments(repo, latest_rev='HEAD'):
    t = (0, 0, 0)
    for commit in repo.iter_commits(latest_rev):
        inc = get_commit_increment(commit.message)
        if inc:
            t = increase_version(t, inc)
    return t


def parse_version(t: tuple) -> str:
    return '%d.%d.%d' % t


def main():
    args = docopt.docopt(__doc__, version=__version__)
    repo = Repo(os.path.abspath(args['--repo']))

    incs = get_commit_increments(repo)
    print(parse_version(incs))


if __name__ == '__main__':
    main()
