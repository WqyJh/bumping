# Bumping

Python tool to calculate SemVer based on conventional git commit messages.

## Prerequisite

- Python >= 3

## Installation

```bash
pip install bumping
```

## Usage

Execute `bumping` and the calculated version would be printed.

```bash
$ bumping
0.1.1
```

Assume the latest version is `0.5.1` and the version tag is `v0.5.1` or `0.5.1`, calculate the incremental version starting from the base revision with the following command, which is really useful for the situation where you didn't use SemVer in the previous versions and want to use it afterwards.

```bash
# Treat tag v0.5.1 as the base version, 
# calculate the incremental version number 
# and plus with 0.5.1.
bumping --base v0.5.1

# Treat master as the base version, version 
# number is 0.5.1, calculate the incremental version
# number and plus with 0.5.1.
bumping --base master --base-version 0.5.1
```
