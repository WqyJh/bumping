import re

from git import Repo, Commit

_prog = re.compile(r'^([^\(\)]+?)(\([^\(\)]+\))?: [\s\S]+$')

_increment_map = {
    'BREAKING CHANGE': (1, 0, 0),
    'feat': (0, 1, 0),
    'fix': (0, 0, 1),
}
_increment_map.setdefault(None)


def get_commit_type(message: str) -> str:
    m = _prog.match(message)
    if m:
        return m.group(1)


def get_increment(type: str) -> tuple:
    return _increment_map[type]


def get_commit_increment(message: str) -> tuple:
    type = get_commit_type(message)
    return get_increment(type)


def main():
    repo = Repo('.')
    
    for commit in repo.iter_commits('HEAD'):
        print('%-10s%s' % (get_commit_increment(commit.message), commit.message))


if __name__ == '__main__':
    main()