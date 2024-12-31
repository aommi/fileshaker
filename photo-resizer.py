import os
from PIL import Image

def resize_swatch_images(input_dir, output_dir, target_size=(200, 200)):
    """

    Args:
        input_dir (str): Directory containing the images.
        output_dir (str): Directory to save the resized images.
        target_size (tuple): The desired size as (width, height).
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if '_sw_' in filename and filename.lower().endswith(('png', 'jpg', 'jpeg')):
            file_path = os.path.join(input_dir, filename)
            try:
                with Image.open(file_path) as img:
                    resized_img = img.resize(target_size)
                    output_path = os.path.join(output_dir, filename)
                    resized_img.save(output_path)
                    print(f"Resized and saved: {output_path}")
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

# Directory paths
input_directory = 'C:/Python Projects/Assets Processed/files-to-swatch'
output_directory = 'C:/Python Projects/Assets Processed/files-to-swatch/swatch'

# Resize images
resize_swatch_images(input_directory, output_directory)
