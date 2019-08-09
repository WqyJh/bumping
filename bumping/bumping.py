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


def add_version_tuple(v1, v2):
    return (v1[0] + v2[0],
            v1[1] + v2[1],
            v1[2] + v2[2])


def get_commit_increments(repo, latest_rev='HEAD'):
    t = (0, 0, 0)
    for commit in repo.iter_commits(latest_rev):
        inc = get_commit_increment(commit.message)
        if inc:
            t = add_version_tuple(t, inc)
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
