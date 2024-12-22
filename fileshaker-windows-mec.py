from pathlib import Path
import os
import shutil
from datetime import datetime

# Step 1: Get today's date in the desired format
today_date = datetime.now().strftime("%Y-%m-%d")

# Step 2: Define the folder paths
source_folder_path = Path('Fileshaker') / 'files-to-rename'
output_base_path = Path('Fileshaker') / 'files-shaked'
primary_folder = output_base_path / f"Primary_{today_date}"
alt_folder = output_base_path / f"Alt_{today_date}"

# Step 3: Create output folders
primary_folder.mkdir(parents=True, exist_ok=True)
alt_folder.mkdir(parents=True, exist_ok=True)

# Step 4: Process the files in the source folder
for filename in os.listdir(source_folder_path):
    current_file_path = source_folder_path / filename

    # Skip directories
    if current_file_path.is_dir():
        continue

    # Check if the filename contains '_ALT'
    if "_ALT" in filename:
        # Move to Alt folder
        new_path = alt_folder / filename
        shutil.move(str(current_file_path), str(new_path))
        print(f"Moved '{current_file_path.name}' to '{new_path}'")
    else:
        # Move to Primary folder
        new_path = primary_folder / filename
        shutil.move(str(current_file_path), str(new_path))
        print(f"Moved '{current_file_path.name}' to '{new_path}'")

print("File processing complete.")
