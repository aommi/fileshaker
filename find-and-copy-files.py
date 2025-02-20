import os
import shutil
import re
from pathlib import Path  # Add this import

# Function to convert file pattern to regex pattern
def convert_pattern_to_regex(pattern):
    """Convert a Windows-style wildcard pattern to regex pattern."""
    # Escape special regex characters in each part except *
    pattern = re.escape(pattern).replace('\\*', '.*')
    return f"^{pattern}$"

# Function to search and copy files
def search_and_copy_files(search_keys_file, source_folder, destination_folder, excluded_extensions, operation="copy", use_wildcards=False):
    # Read search keys from the text file and convert to lowercase, remove spaces
    with open(search_keys_file, 'r') as file:
        search_keys = [line.strip().lower().replace(' ', '') for line in file]
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # Get filename without extension for matching
            file_name_no_ext = os.path.splitext(file_name)[0]
            file_name_lower = file_name_no_ext.lower().replace(' ', '')
            
            # Check if the file has an excluded extension
            if any(file_name.lower().endswith(ext.lower()) for ext in excluded_extensions):
                continue  # Skip this file

            # Check if the file matches any of the search keys
            for key in search_keys:
                matches = False
                if use_wildcards and '*' in key:
                    pattern = convert_pattern_to_regex(key.lower())
                    # Debug print to see the pattern
                    #print(f"Pattern: {pattern}")
                    #print(f"Testing against: {file_name_lower}")
                    matches = bool(re.search(pattern, file_name_lower))
                else:
                    matches = key.lower() in file_name_lower

                if matches:
                    source_path = os.path.join(root, file_name)
                    destination_path = os.path.join(destination_folder, file_name)
                    
                    print(f"Match found: '{key}' in '{file_name}'")  # Debug print

                    # Perform the specified operation
                    if operation == "move":
                        shutil.move(source_path, destination_path)
                        print(f"Moved: {source_path} to {destination_path}")
                    else:  # Default to copy
                        shutil.copy2(source_path, destination_path)
                        print(f"Copied: {source_path} to {destination_path}")

if __name__ == "__main__":
    # Use Path for cross-platform path handling
    search_keys_file = Path("Python-Projects/fileshaker/assets/files-found/search-keys.txt")
    source_folder = Path(input("Enter the path to the source folder: ").strip())
    destination_folder = Path("Python-Projects/fileshaker/assets/files-found")

    # Convert to absolute paths
    search_keys_file = search_keys_file.resolve()
    destination_folder = destination_folder.resolve()

    # Specify file extensions to exclude
    #excluded_extensions = ['.txt', '.log', '.tmp']  # Add extensions to exclude #--example
    excluded_extensions = ['.tif']
    operation=input("Enter the operation (copy/move): ").strip().lower()
    use_wildcards=True
    search_and_copy_files(search_keys_file, source_folder, destination_folder, excluded_extensions, operation, use_wildcards)