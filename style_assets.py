import os
import re
# This class is used to process assets of a given style based on the VPN and alt-VPN values in the input data.
class StyleAssets:
    def __init__(self, source_folder_path, output_folder_path, today_date, alphabet, custom_sort):
        self.source_folder_path = source_folder_path
        self.output_folder_path = output_folder_path
        self.today_date = today_date
        self.alphabet = alphabet
        self.custom_sort = custom_sort

    def find_assets(self, vpn, alt_vpn):
        def matches_pattern(filename, pattern):
            # Convert glob pattern to regex pattern
            regex_pattern = pattern.replace('*', '.*').lower()
            return bool(re.search(regex_pattern, filename.lower()))
        
        return [
            self.source_folder_path / filename
            for filename in os.listdir(self.source_folder_path)
            if (matches_pattern(filename, vpn) or matches_pattern(filename, alt_vpn)) 
            and not (self.source_folder_path / filename).is_dir()
        ]

    def sort_assets(self, files_to_process):
        print(f"\nDebug: Entering sort_assets function")
        print(f"Debug: custom_sort value is {self.custom_sort}")
        print(f"Debug: Number of files to process: {len(files_to_process)}")
        print(f"Debug: Files before sorting: {[str(f) for f in files_to_process]}")
        
        if self.custom_sort:
            #remember to use lower case if you're adding sort keys
            sorted_files = sorted(files_to_process, key=lambda filepath: (
                0 if '_f' in str(filepath).lower()
                #else 1 if '_side' in str(filepath).lower()
                #else 2 if '_back' in str(filepath).lower()
                else 3, filepath
            ))
            print(f"Debug: Files after custom sorting: {[str(f) for f in sorted_files]}")
            return sorted_files
        else:
            sorted_files = sorted(files_to_process)
            print("Debug: Using default sort")
            print(f"Debug: Files after default sorting: {[str(f) for f in sorted_files]}")
            return sorted_files

    def move_assets(self, files_to_process, vpn, primary_name, primary_folder, alt_folder):
        is_primary_moved = False
        num_alts = 0
        alt_folder_name_logged = ""

        if files_to_process:
            first_file = files_to_process[0]
            file_extension = first_file.suffix
            new_primary_path = primary_folder / (primary_name + file_extension)
            first_file.rename(new_primary_path)
            is_primary_moved = True
            print(f"Primary file '{first_file.name}' moved to '{primary_folder}'")

            for index, file_path in enumerate(files_to_process[1:], start=1):
                file_extension = file_path.suffix
                alt_name = f"{primary_name}_ALT_{self.alphabet[index-1]}{file_extension}"
                new_alt_file_path = alt_folder / alt_name
                file_path.rename(new_alt_file_path)
                num_alts += 1
                alt_folder_name_logged = str(alt_folder)

            print(f"ALT files for VPN '{vpn}' are moved to folder: {alt_folder}")

        return is_primary_moved, num_alts, alt_folder_name_logged