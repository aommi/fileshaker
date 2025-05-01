import os
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageCms
from pathlib import Path

# Configuration
MAX_SIZE = 2500  # px
OUTPUT_FORMAT = 'JPEG'
OUTPUT_QUALITY = 95  # Max quality for JPEG
NUM_WORKERS = 8  # You can adjust this depending on your CPU

def process_alt_image(input_path, output_path):
    """Process a single image according to the ALT Images pipeline."""
    with Image.open(input_path) as img:
        # Handle transparency - with better error handling
        try:
            if img.mode == 'RGBA':
                # Handle RGBA images
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, (0, 0), img)
                img = background
            elif img.mode == 'LA':
                # Handle grayscale with alpha
                background = Image.new('RGB', img.size, (255, 255, 255))
                img_rgba = img.convert('RGBA')
                background.paste(img_rgba, (0, 0), img_rgba)
                img = background
            elif img.mode == 'P':
                # Handle palette images (including those with transparency)
                img = img.convert('RGBA')
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, (0, 0), img)
                img = background
            else:
                img = img.convert('RGB')

            # Convert to sRGB if necessary
            if img.info.get('icc_profile', None):
                try:
                    icc_profile = img.info.get('icc_profile')
                    img = ImageCms.profileToProfile(img, icc_profile, ImageCms.createProfile("sRGB"))
                except Exception:
                    img = img.convert('RGB')
            else:
                img = img.convert('RGB')

            # Resize if needed
            width, height = img.size
            longest_side = max(width, height)
            if longest_side > MAX_SIZE:
                if width > height:
                    new_width = MAX_SIZE
                    new_height = int(height * MAX_SIZE / width)
                else:
                    new_height = MAX_SIZE
                    new_width = int(width * MAX_SIZE / height)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Strip metadata
            new_img = Image.new("RGB", img.size, (255, 255, 255))  # Create new white canvas
            new_img.paste(img)

            # Save as JPG, max quality
            output_path = output_path.with_suffix('.jpg')
            output_path.parent.mkdir(parents=True, exist_ok=True)
            new_img.save(output_path, format=OUTPUT_FORMAT, quality=OUTPUT_QUALITY, optimize=True)
        except Exception as e:
            print(f"Error processing {input_path}: {str(e)}")
            raise


def process_folder(input_folder, output_folder, process_name):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    # Determine which processor function to use
    if process_name == "ALT Images":
        processor = process_alt_image
    else:
        raise ValueError(f"Unknown process name: {process_name}")

    # Get all image files (you can refine this to certain extensions if needed)
    image_files = list(input_folder.glob("*"))

    # Process images in parallel
    with ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        futures = []
        for img_file in image_files:
            output_file = output_folder / img_file.name
            futures.append(executor.submit(processor, img_file, output_file))

        # wait for completion
        for future in futures:
            future.result()

if __name__ == "__main__":
    # Example usage
    input_folder = "C:/python-projects/fileshaker/assets/photos-to-process"
    output_folder = "C:/python-projects/fileshaker/assets/photos-processed"
    process_name = "ALT Images"

    process_folder(input_folder, output_folder, process_name)
