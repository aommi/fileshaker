import os
import shutil
import fnmatch

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
            # Convert filename to lowercase and remove spaces for comparison
            file_name_lower = file_name.lower().replace(' ', '')
            
            # Check if the file has an excluded extension
            if any(file_name_lower.endswith(ext.lower()) for ext in excluded_extensions):
                continue  # Skip this file

            # Check if the file matches any of the search keys
            for key in search_keys:
                matches = False
                if use_wildcards:
                    matches = fnmatch.fnmatch(file_name_lower, key) or (key in file_name_lower)
                else:
                    matches = key in file_name_lower

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
    search_keys_file = "C:\\Python-Projects\\fileshaker\\assets\\files-found\\search-keys.txt"
    source_folder = input("Enter the path to the source folder: ").strip()
    destination_folder = "C:\\Python-Projects\\fileshaker\\assets\\files-found"

    # Specify file extensions to exclude
    #excluded_extensions = ['.txt', '.log', '.tmp']  # Add extensions to exclude #--example
    excluded_extensions = ['.tif']
    operation=input("Enter the operation (copy/move): ").strip().lower()
    use_wildcards=True
    search_and_copy_files(search_keys_file, source_folder, destination_folder, excluded_extensions, operation, use_wildcards)