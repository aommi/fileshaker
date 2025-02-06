import os
import time
import requests
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

###############################
# Configuration & Setup
###############################

# URL of the product page
BASE_URL = "https://www.spyoptic.com/ca/goggles/snow-goggles/marauder-36615.html"  # <-- Replace with the actual URL

# Folder to save images
SAVE_FOLDER = "downloaded_images"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# CSS Selectors and class names based on your inspection:
COLOR_BUTTON_SELECTOR = ".color-attribute.color-vatiations-item"
# The active carousel container that holds the main image:
ACTIVE_CAROUSEL_SELECTOR = "div.carousel-item.slick-slide.slick-current.slick-active span.js-main-image img"
# Alt image button (assumed based on your description)
ALT_BUTTON_SELECTOR = "button.slick-paging-btn"

# Timing (in seconds)
PAGE_LOAD_WAIT = 3
ALT_IMAGE_WAIT = 2

###############################
# Helper Functions
###############################

def download_image(img_url, filename_suffix=""):
    """Downloads the image from img_url and saves it with an appended suffix."""
    if not img_url:
        print("No image URL provided.")
        return

    # Extract a filename from the URL and append suffix to avoid collisions.
    parsed_url = urlparse(img_url)
    base_name = os.path.basename(parsed_url.path)
    name, ext = os.path.splitext(base_name)
    filename = f"{name}{filename_suffix}{ext}"
    file_path = os.path.join(SAVE_FOLDER, filename)

    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
            
            # Optionally, convert WebP to JPG if desired
            if ext.lower() == ".webp":
                try:
                    jpg_filename = f"{name}{filename_suffix}.jpg"
                    jpg_path = os.path.join(SAVE_FOLDER, jpg_filename)
                    img = Image.open(file_path).convert("RGB")
                    img.save(jpg_path, "JPEG")
                    os.remove(file_path)
                    print(f"Converted to: {jpg_filename}")
                except Exception as e:
                    print(f"Conversion error for {filename}: {e}")
        else:
            print(f"Failed to download image: {img_url}")
    except Exception as e:
        print(f"Error downloading {img_url}: {e}")

def get_active_image_url(driver, wait):
    """
    Returns the data-largeimage URL from the active carousel image.
    If not found, returns None.
    """
    try:
        # Wait until the active carousel image is present
        img_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ACTIVE_CAROUSEL_SELECTOR)))
        # Get the high-res image URL from the attribute 'data-largeimage'
        url = img_element.get_attribute("data-largeimage")
        return url
    except Exception as e:
        print("Error getting active image URL:", e)
        return None

###############################
# Main Scraping Logic
###############################

def main():
    # Set up Selenium WebDriver (Chrome)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    wait = WebDriverWait(driver, 10)
    
    # Open the page
    driver.get(BASE_URL)
    time.sleep(PAGE_LOAD_WAIT)  # Allow time for the page to load

    # Find all color buttons
    color_buttons = driver.find_elements(By.CSS_SELECTOR, COLOR_BUTTON_SELECTOR)
    print(f"Found {len(color_buttons)} color variations.")

    # Iterate over each color variation
    for color_index, color_button in enumerate(color_buttons, start=1):
        try:
            # Click the color variation button
            driver.execute_script("arguments[0].click();", color_button)
            print(f"Clicked color variation {color_index}")
            time.sleep(PAGE_LOAD_WAIT)  # Wait for the carousel to update

            # Get and download the main image for this color
            main_img_url = get_active_image_url(driver, wait)
            if main_img_url:
                download_image(main_img_url, filename_suffix=f"_color{color_index}_main")
            else:
                print(f"No main image URL found for color {color_index}")

            # Find all alternative image buttons for this color variation
            alt_buttons = driver.find_elements(By.CSS_SELECTOR, ALT_BUTTON_SELECTOR)
            print(f"Found {len(alt_buttons)} alternative images for color {color_index}.")

            # Iterate through alternative image buttons
            for alt_index, alt_button in enumerate(alt_buttons, start=1):
                try:
                    # Click the alt image button
                    driver.execute_script("arguments[0].click();", alt_button)
                    print(f"Clicked alternative image {alt_index} for color {color_index}")
                    time.sleep(ALT_IMAGE_WAIT)  # Wait for the active image to update

                    # Get and download the alternative image from the active carousel
                    alt_img_url = get_active_image_url(driver, wait)
                    if alt_img_url:
                        download_image(alt_img_url, filename_suffix=f"_color{color_index}_alt{alt_index}")
                    else:
                        print(f"No alternative image URL found for color {color_index}, alt {alt_index}")
                except Exception as e_alt:
                    print(f"Error processing alternative image {alt_index} for color {color_index}: {e_alt}")
        except Exception as e_color:
            print(f"Error processing color variation {color_index}: {e_color}")
    
    driver.quit()

if __name__ == '__main__':
    main()
