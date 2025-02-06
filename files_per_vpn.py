import os
class FilesPerVpn:
    def __init__(self, source_folder_path, output_folder_path, today_date, alphabet, custom_sort):
        self.source_folder_path = source_folder_path
        self.output_folder_path = output_folder_path
        self.today_date = today_date
        self.alphabet = alphabet
        self.custom_sort = custom_sort

    def find_files(self, vpn, alt_vpn):
        return [
            self.source_folder_path / filename
            for filename in os.listdir(self.source_folder_path)
            if (vpn in filename.lower() or alt_vpn in filename.lower()) and not (self.source_folder_path / filename).is_dir()
        ]

    def sort_files(self, files_to_process):
        if self.custom_sort:
            return sorted(files_to_process, key=lambda filepath: (
                5 if 'left' in str(filepath).lower()
                else 0 if 'hero' in str(filepath).lower()
                else 1 if 'alt1' in str(filepath).lower()
                else 4, filepath
            ))
        else:
            return sorted(files_to_process)

    def move_files(self, files_to_process, vpn, primary_name, primary_folder, alt_folder):
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