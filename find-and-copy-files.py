import os
import shutil

# Function to search and copy files
def search_and_copy_files(search_keys_file, source_folder, destination_folder):
    # Read search keys from the text file
    with open(search_keys_file, 'r') as file:
        search_keys = [line.strip() for line in file]

    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(source_folder):
        for file_name in files:
            # Check if the file starts with any of the search keys
            for key in search_keys:
                if key in file_name:
                    source_path = os.path.join(root, file_name)
                    destination_path = os.path.join(destination_folder, file_name)

                    # Copy the file to the destination folder
                    shutil.copy2(source_path, destination_path)
                    print(f"Copied: {source_path} to {destination_path}")

if __name__ == "__main__":
    search_keys_file = "C:\\Python Projects\\fileshaker\\Assets Processed\\files-found\\search keys.txt"
    source_folder = input("Enter the path to the source folder: ").strip()
    destination_folder = "C:\\Python Projects\\fileshaker\\Assets Processed\\files-found\\files-copied"

    search_and_copy_files(search_keys_file, source_folder, destination_folder)
