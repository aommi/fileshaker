import os
from PIL import Image

def convert_webp_to_format(image_path, target_format="jpg"):
    """
    Converts a single .webp image to the specified format.
    For JPG conversion, a white background (#ffffff) is applied.
    """
    target_format = target_format.lower()
    if target_format == "jpg":
        output_path = os.path.splitext(image_path)[0] + '.jpg'
    elif target_format == "png":
        output_path = os.path.splitext(image_path)[0] + '.png'
    else:
        print(f"Unsupported target format: {target_format}")
        return

    try:
        with Image.open(image_path) as img:
            if target_format == "jpg":
                # Create a white background image and paste the original image on it.
                rgb_img = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode in ("RGBA", "LA") or (img.mode == "P" and 'transparency' in img.info):
                    rgb_img.paste(img, mask=img.split()[-1])
                else:
                    rgb_img.paste(img)
                rgb_img.save(output_path, "JPEG")
            elif target_format == "png":
                # For PNG, simply save; transparency will be preserved.
                img.save(output_path, "PNG")
        print(f"Converted {image_path} to {output_path}")
    except Exception as e:
        print(f"Error converting {image_path}: {e}")

def convert_directory_images(directory, target_format="jpg"):
    """
    Processes all .webp files in the given directory,
    converting each to the specified format.
    """
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    for filename in os.listdir(directory):
        if filename.lower().endswith('.webp'):
            image_path = os.path.join(directory, filename)
            convert_webp_to_format(image_path, target_format)

if __name__ == "__main__":
    dir_path = input("Enter the directory path containing .webp files: ").strip()
    fmt = input("Enter the target format (jpg or png): ").strip().lower()
    if fmt not in ("jpg", "png"):
        print("Invalid format specified. Please use 'jpg' or 'png'.")
    else:
        convert_directory_images(dir_path, fmt)