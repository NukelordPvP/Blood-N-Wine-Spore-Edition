import os

def find_large_files(directory='.', size_limit_mb=100, exclude_dirs=None):
    size_limit_bytes = size_limit_mb * 1024 * 1024
    large_files = []

    if exclude_dirs is None:
        exclude_dirs = {'.git'}

    for root, dirs, files in os.walk(directory, topdown=True):
        # Modify dirs in-place to exclude specified directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            file_path = os.path.join(root, file)
            try:
                if os.path.getsize(file_path) > size_limit_bytes:
                    large_files.append(file_path)
            except (FileNotFoundError, PermissionError):
                # Skip files that cannot be accessed
                continue

    return large_files

def update_gitignore(large_files, gitignore_path='.gitignore'):
    if not large_files:
        print("No files over 100MB found.")
        return

    existing_entries = set()
    need_newline = False

    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as gitignore_file:
            content = gitignore_file.read()
            # Check if file is not empty and doesn't end with a newline
            if content and not content.endswith('\n'):
                need_newline = True

        # Re-read to get existing entries
        with open(gitignore_path, 'r') as gitignore_file:
            existing_entries = set(line.strip() for line in gitignore_file if line.strip())

    with open(gitignore_path, 'a') as gitignore_file:
        if need_newline:
            gitignore_file.write('\n')
        for file in large_files:
            relative_path = os.path.relpath(file)
            # Convert backslashes to forward slashes
            relative_path = relative_path.replace(os.sep, '/')
            if relative_path not in existing_entries:
                gitignore_file.write(relative_path + '\n')
                print(f"Added {relative_path} to {gitignore_path}")

def main():
    large_files = find_large_files()
    update_gitignore(large_files)

if __name__ == "__main__":
    main()
