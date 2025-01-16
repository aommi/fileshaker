# sort_files.py

def sort_files(files_to_process):
    return sorted(files_to_process, key=lambda filepath: (
        0 if 'model_1' in str(filepath).lower()
        else 1 if 'product_1' in str(filepath).lower()
        else 2, filepath
    ))