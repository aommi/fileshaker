import re
from pathlib import Path
import shutil
from collections import defaultdict
import os

def validate_and_organize_images(input_folder):
    folder_path = Path(input_folder)
    if not folder_path.is_dir():
        print(f"Invalid folder: {folder_path}")
        return

    # Define subfolders
    primary_folder = folder_path / "primary"
    alt_folder = folder_path / "alt"
    swatch_folder = folder_path / "swatch"

    # Create them if not exist
    for subfolder in [primary_folder, alt_folder, swatch_folder]:
        subfolder.mkdir(exist_ok=True)

    # Patterns
    primary_pattern = re.compile(r'^(\d{7})_([A-Za-z0-9]{5})$')
    alt_pattern = re.compile(r'^(\d{7}_[A-Za-z0-9]{5})_ALT-[A-Za-z0-9]+$')
    swatch_pattern = re.compile(r'^(\d{7}_[A-Za-z0-9]{5})_SWATCH$')

    # Storage
    found_styles = defaultdict(lambda: {"alts": [], "swatch": False, "noc02": False, "primary_file": None})

    # Define allowed file extensions and excluded extensions
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tif', '.tiff'}
    EXCLUDED_EXTENSIONS = {'.txt', '.log', '.db'}

    # Process files using os.walk
    for root, dirs, files in os.walk(folder_path):
        current_path = Path(root)
        
        # Skip if we're already in an output folder or its subdirectories
        if any(str(current_path).startswith(str(output)) 
               for output in [primary_folder, alt_folder, swatch_folder]):
            dirs.clear()  # Stop recursion into this directory
            continue
            
        print(f"Checking directory: {current_path}")  # Debug print
            
        for filename in files:
            file_path = current_path / filename
            ext = file_path.suffix.lower()
            
            # Skip excluded file types and check for allowed extensions
            if ext in EXCLUDED_EXTENSIONS or ext not in ALLOWED_EXTENSIONS:
                continue
                
            name = file_path.stem
            print(f"Processing: {file_path}")  # Debug print

            # Process the file based on its pattern
            try:
                if primary_pattern.fullmatch(name):
                    found_styles[name]["primary_file"] = file_path
                    if name.endswith("NOC02"):
                        found_styles[name]["noc02"] = True
                    shutil.move(str(file_path), primary_folder / filename)
                    print(f"Moved to primary: {filename}")  # Debug print

                elif alt_pattern.fullmatch(name):
                    base = name.split("_ALT")[0]
                    found_styles[base]["alts"].append(file_path)
                    shutil.move(str(file_path), alt_folder / filename)
                    print(f"Moved to alt: {filename}")  # Debug print

                elif swatch_pattern.fullmatch(name):
                    base = name.replace("_SWATCH", "")
                    found_styles[base]["swatch"] = True
                    shutil.move(str(file_path), swatch_folder / filename)
                    print(f"Moved to swatch: {filename}")  # Debug print
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")

    # Print report
    print("\n📦 Style Summary:")
    for style, info in found_styles.items():
        num_alts = len(info["alts"])
        swatch_status = "✔️" if info["swatch"] else ("(not needed)" if info["noc02"] else "❌ missing")
        print(f"- {style}: {num_alts} ALT(s), Swatch: {swatch_status}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        input_folder = input("Please enter the folder path: ").strip()
        validate_and_organize_images(input_folder)
    else:
        validate_and_organize_images(sys.argv[1])
