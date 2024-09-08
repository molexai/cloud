__version__ = "0.0.1"

import os


def upgrade():
    new_version = increment_version(__version__)
    with open(os.path.abspath(__file__), 'r') as f:
        lines = f.readlines()

    # Replace the version line
    for i, line in enumerate(lines):
        if line.startswith('__version__'):
            lines[i] = f'__version__ = "{new_version}"\n'

    # Write the modified lines back to the file
    with open(os.path.abspath(__file__), 'w') as f:
        f.writelines(lines)

def increment_version(version):
    major, minor, patch = map(int, version.split("."))

    # Increment the patch version
    patch += 1

    if patch >= 10:
        # Increment the minor version and reset patch
        minor += 1
        patch = 0

    if minor >= 10:
        # Increment the major version and reset minor
        major += 1
        minor = 0

    new_version = ".".join([str(major), str(minor), str(patch)])
    return new_version

upgrade()