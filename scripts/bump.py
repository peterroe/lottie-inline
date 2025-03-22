# update the version in `src/lottie_inline/version.py`
# usage: python bump.py patch|minor|major

import sys

def bump_version(version, level):
    major, minor, patch = map(int, version.split('.'))
    
    if level == 'patch':
        patch += 1
    elif level == 'minor':
        minor += 1
        patch = 0  # Reset patch to 0 when minor is incremented
    elif level == 'major':
        major += 1
        minor = 0  # Reset minor and patch to 0 when major is incremented
        patch = 0

    return f"{major}.{minor}.{patch}"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python bump.py patch|minor|major")
        sys.exit(1)

    level = sys.argv[1]

    # Read the current version from the version file
    with open('src/lottie_inline/version.py', 'r') as file:
        version_line = file.readline().strip()
        current_version = version_line.split('=')[1].strip().strip('"')

    # Call bump_version to get the new version
    new_version = bump_version(current_version, level)

    # Write the new version back to the version file
    with open('src/lottie_inline/version.py', 'w') as file:
        file.write(f'__version__ = "{new_version}"\n')

    print(f"Version bumped to {new_version}")

    
