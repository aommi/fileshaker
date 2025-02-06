from google.cloud import vision
from PIL import Image
from pathlib import Path
from collections import defaultdict
import os

# Set up Google Cloud Vision client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/amirali/Library/Mobile Documents/com~apple~CloudDocs/Python Projects/secret/photo-editor.json"
client = vision.ImageAnnotatorClient()

def detect_objects(image_path):
    """Detect objects in the image using Google Vision API."""
    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations
    
    return objects

def filter_irrelevant_objects(objects):
    """Filter out irrelevant objects like 'person' or 'skin'."""
    irrelevant_labels = ["person", "skin", "face", "hair", "hand"]
    return [obj for obj in objects if obj.name.lower() not in irrelevant_labels]

def get_largest_object(objects):
    """Get the largest object by bounding box area."""
    if not objects:
        return None
    
    largest_object = max(objects, key=lambda obj: (
        (obj.bounding_poly.normalized_vertices[2].x - obj.bounding_poly.normalized_vertices[0].x) *
        (obj.bounding_poly.normalized_vertices[2].y - obj.bounding_poly.normalized_vertices[0].y)
    ))
    return largest_object

def crop_image_to_object(image, vertices):
    """Crop the image to the region defined by the object's bounding polygon."""
    width, height = image.size
    x_coords = [int(v.x * width) for v in vertices]
    y_coords = [int(v.y * height) for v in vertices]
    
    x1, x2 = min(x_coords), max(x_coords)
    y1, y2 = min(y_coords), max(y_coords)
    
    return image.crop((x1, y1, x2, y2))

def get_prominent_colors(image, num_colors=2):
    """Get the most prominent colors from the image."""
    pixels = image.getdata()
    color_count = defaultdict(int)
    
    for pixel in pixels:
        color_count[pixel[:3]] += 1  # Ignore alpha channel if present
    
    sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)
    return [color[0] for color in sorted_colors[:num_colors]]

def create_swatch(image, size=(200, 200)):
    """Create a swatch from the image."""
    return image.resize(size)

def save_swatch(image, output_path):
    """Save the swatch as a JPG file."""
    # Convert RGBA to RGB if necessary
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    
    # Create the directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path, 'JPEG')

def process_image(image_path, output_path):
    """Process an image to detect objects, find the prominent color, and create a swatch."""
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Detect objects in the image
        objects = detect_objects(image_path)
        print(f"Detected objects in {image_path.name}: {[obj.name for obj in objects]}")
        
        # Filter out irrelevant objects
        filtered_objects = filter_irrelevant_objects(objects)
        if not filtered_objects:
            print(f"No relevant objects found in {image_path.name}")
            return
        
        # Get the largest object (assumed to be the main product)
        largest_object = get_largest_object(filtered_objects)
        print(f"Processing object: {largest_object.name}")
        
        # Crop the image to the largest object's bounding box
        cropped_image = crop_image_to_object(image, largest_object.bounding_poly.normalized_vertices)
        
        # Create a swatch from the cropped image
        swatch = create_swatch(cropped_image)
        
        # Save the swatch
        save_swatch(swatch, output_path)
        print(f"Swatch saved successfully to {output_path}")
    except Exception as e:
        print(f"Error processing {image_path.name}: {e}")

def process_directory(input_dir, output_dir):
    """Process all files in the input directory and save swatches to the output directory."""
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each file in the input directory
    for file_path in input_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg']:
            # Define the output file name
            output_file_name = f"{file_path.stem}_SWATCH.jpg"
            output_path = output_dir / output_file_name
            
            # Process the image
            process_image(file_path, output_path)

if __name__ == "__main__":
    # Define input and output directories
    input_directory = Path('/Users/amirali/Desktop/files-to-swatch')
    output_directory = Path('/Users/amirali/Desktop/files-to-swatch/swatches')
    
    # Process all files in the input directory
    process_directory(input_directory, output_directory)