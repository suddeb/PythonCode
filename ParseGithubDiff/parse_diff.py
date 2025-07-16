import re

def parse_git_diff(diff_file_path):
    """
    Reads a git diff file and returns lists of newly added, modified, and deleted files.

    Args:
        diff_file_path (str): The path to the diff.txt file.

    Returns:
        tuple: A tuple containing three lists: (newly_added_files, modified_files, deleted_files).
    """
    newly_added_files = []
    modified_files = []
    deleted_files = []

    # Regex for newly added files:
    # Looks for 'new file mode', optionally followed by an 'index' line,
    # then '--- /dev/null', and finally '+++ b/path/to/new/file'.
    # Captures the 'path/to/new/file' part.
    new_file_pattern = re.compile(
        r'^\s*new file mode \d+\n'
        r'(?:index [0-9a-f]+\.\.[0-9a-f]+(?: \d+)?\n)?' # Optional index line
        r'--- /dev/null\n'
        r'\+\+\+ b/(.*)$',
        re.MULTILINE
    )

    # Regex for modified files:
    # Looks for 'diff --git a/path b/path', optionally followed by an 'index' line,
    # then '--- a/path', and finally '+++ b/path'.
    # It uses backreferences (\1 and \2) to ensure the paths match across lines,
    # and implicitly excludes /dev/null because real paths are expected.
    modified_file_pattern = re.compile(
        r'^diff --git a/(.+?) b/(.+?)\n'
        r'(?:index [0-9a-f]+\.\.[0-9a-f]+(?: \d+)?\n)?' # Optional index line
        r'--- a/\1\n'
        r'\+\+\+ b/\2$',
        re.MULTILINE
    )

    # Regex for deleted files:
    # Looks for 'deleted file mode', optionally followed by an 'index' line,
    # then '--- a/path/to/deleted/file', and finally '+++ /dev/null'.
    # Captures the 'path/to/deleted/file' part.
    deleted_file_pattern = re.compile(
        r'^\s*deleted file mode \d+\n'
        r'(?:index [0-9a-f]+\.\.[0-9a-f]+(?: \d+)?\n)?' # Optional index line
        r'--- a/(.*)\n'
        r'\+\+\+ /dev/null$',
        re.MULTILINE
    )

    try:
        # Explicitly specify 'latin-1' encoding to handle potential non-UTF-8 characters.
        with open(diff_file_path, 'r', encoding='latin-1') as f:
            diff_content = f.read()

        # Find newly added files
        new_matches = new_file_pattern.finditer(diff_content)
        for match in new_matches:
            newly_added_files.append(match.group(1))

        # Find modified files
        # It's important to note that a single file can be listed multiple times in a diff
        # if it has multiple hunks. We use a set to ensure unique file paths.
        modified_matches = modified_file_pattern.finditer(diff_content)
        for match in modified_matches:
            # Group 1 and Group 2 should be the same path for modified files
            modified_files.append(match.group(1))
        
        # Convert to set to remove duplicates, then back to list for consistent output type
        modified_files = list(set(modified_files))

        # Find deleted files
        deleted_matches = deleted_file_pattern.finditer(diff_content)
        for match in deleted_matches:
            deleted_files.append(match.group(1))

    except FileNotFoundError:
        print(f"Error: The file '{diff_file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return newly_added_files, modified_files, deleted_files

if __name__ == "__main__":
    diff_file = "diff.txt"  # Make sure this matches the name of your diff file
    added_files, modified_files, deleted_files = parse_git_diff(diff_file)

    if added_files:
        print("Newly Added Files:")
        with open("newlyAddedFile.csv", "w") as f:
            for file in added_files:
                print(f"- {file}", file=f)
    else:
        print("No newly added files found in the diff.")

    print("\n" + "="*30 + "\n") # Separator for clarity

    if modified_files:
        print("Modified Files:")
        with open("modifiedFile.csv", "w") as f:
            for file in modified_files:
                print(f"- {file}", file=f)
    else:
        print("No modified files found in the diff.")

    print("\n" + "="*30 + "\n") # Separator for clarity

    if deleted_files:
        print("Deleted Files:")
        with open("deletedFile.csv", "w") as f:
            for file in deleted_files:
                print(f"- {file}", file=f)
    else:
        print("No deleted files found in the diff.")
