import unittest

from bumping import bumping


class TestBumping(unittest.TestCase):
    def test_get_commit_type(self):
        asserts = (
            ('feat: xxx', 'feat'),
            ('feat(xxx): xxx', 'feat'),
            ('feat(xxx): ', None),
            ('feat xxx', None),
            ('fix: xxx', 'fix'),
            ('BREAKING CHANGE: xxx', 'BREAKING CHANGE'),
            ('BREAKING CHANGE(xxx): xxx', 'BREAKING CHANGE'),
            ('chore: xxx', 'chore'),
            ('docs: xxx', 'docs'),
        )

        for message, expected in asserts:
            self.assertEqual(expected, bumping.get_commit_type(message))

    def test_get_commit_increment(self):
        asserts = (
            ('feat: xxx', (0, 1, 0)),
            ('feat(xxx): xxx', (0, 1, 0)),
            ('fix: xxx', (0, 0, 1)),
            ('BREAKING CHANGE: XXX', (1, 0, 0)),
            ('feat xxx', None),
        )

        for message, expected in asserts:
            self.assertEqual(expected, bumping.get_commit_increment(message))

    def test_increase_version(self):
        asserts = (
            (((0, 0, 1), (1, 0, 0)), (1, 0, 0)),  # BREAKING CHANGES
            (((0, 0, 1), (0, 1, 0)), (0, 1, 0)),  # features
            (((0, 0, 1), (0, 0, 1)), (0, 0, 2)),  # patches
        )

        for (v, inc), expected in asserts:
            self.assertTupleEqual(expected, bumping.increase_version(v, inc))


if __name__ == '__main__':
    unittest.main()
