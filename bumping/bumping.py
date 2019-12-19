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
import click

from git import Repo

from bumping import __version__, logger, set_debug


_COMMIT_TYPE = r'^([^\(\)]+?)(\([^\(\)]+\))?: [\s\S]+$'


_TYPE_INCREMENT = {
    'BREAKING CHANGE': (1, 0, 0),
    'feat': (0, 1, 0),
    'fix': (0, 0, 1),
}


def get_commit_type(message: str) -> str:
    m = re.match(_COMMIT_TYPE, message)
    if m:
        return m.group(1)


def get_increment(type: str) -> tuple:
    return _TYPE_INCREMENT.get(type, None)


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


def _get_iter_rev(repo, starting_commit: str, stopping_commit: str):
    if starting_commit:
        c = repo.commit(starting_commit)
        if not c.parents:
            # starting_commit is initial commit,
            # treat as default
            starting_commit = ''

    iter_rev = f'{starting_commit}..{stopping_commit}' if starting_commit else stopping_commit
    return iter_rev


def get_commit_increments(repo, base='', base_version=None, end='HEAD'):
    t = parse_version(base_version or '0.0.0')
    iter_rev = _get_iter_rev(repo, starting_commit=base, stopping_commit=end)
    for commit in reversed(list(repo.iter_commits(iter_rev))):
        inc = get_commit_increment(commit.message)
        if inc:
            logger.debug(commit.message)
            t = increase_version(t, inc)
    return t


def parse_version(v):
    '''Parse version string to version tuple.

    :param v: version string like '0.0.1'
    :returns a tuple contains three parts of the version like (0, 0, 1)
    '''
    try:
        if v:
            return tuple(map(int, v.split('.')))
    except Exception:
        pass

    raise Exception(f'Invalid version string: {v}')


def format_version(t: tuple) -> str:
    return '%d.%d.%d' % t


@click.command()
@click.version_option(__version__)
@click.option('-d', '--debug', is_flag=True)
@click.option('-r', '--repo', default='./',
              help="Path to the repository's root directory")
@click.option('--base',
              help='increase the version from base revision')
@click.option('--base-version',
              help='version number of base revision')
@click.option('--end', default='HEAD',
              help='increase the version to end revision')
def main(debug, repo, base, base_version, end):
    '''Python tool to calculate SemVer based on conventional git commit messages.'''
    set_debug(debug)
    repo = Repo(os.path.abspath(repo))
    incs = get_commit_increments(
        repo, base=base, base_version=base_version or base, end=end)
    print(format_version(incs))


if __name__ == '__main__':
    main()
