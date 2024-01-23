import math
import sys
import os
import requests
import win32api
import time
import cv2
from docx import Document
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

AUCTION_NUM =("1")
PHOTO_FOLDER = "C:/Users/wangk/Documents/Auction1"


def get_image_urls(url):
    # Set the path to the Edge WebDriver executable
    edge_driver_path = "C:/Users/wangk/PycharmProjects/ExtractImage/msedgedriver.exe"

    # Set Edge WebDriver options
    edge_options = webdriver.EdgeOptions()
    edge_options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    # Replace with your actual path to Edge binary
    # edge_options.headless = True
    # Initialize Edge WebDriver with options
    driver = webdriver.Edge(options=edge_options)

    # Navigate to the webpage
    driver.get(url)

    if url[25:-1].isnumeric():
        image_element = driver.find_element(By.ID, 'landingImage')
        return [image_element.get_attribute('src')]
    else:

        try:
            # Find the thumbnail elements with class name "a-spacing-small item imageThumbnail a-declarative"
            thumbnail_elements = driver.find_elements(By.CSS_SELECTOR,
                                                    'li.a-spacing-small.item.imageThumbnail.a-declarative')

            # Interact with each thumbnail element and click the nested <span> with class name
            # "a-button a-button-thumbnail a-button-toggle"
            for i, thumbnail in enumerate(thumbnail_elements[:3], start=1):
                span_element = thumbnail.find_element(By.CSS_SELECTOR, 'span.a-button.a-button-thumbnail.a-button-toggle')
                ActionChains(driver).move_to_element(span_element).click().perform()

            # Use explicit wait to wait for the <li> elements with class prefix "image item item" to be present
            wait = WebDriverWait(driver, 4)
            li_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[class^="image item item"]')))

            image_urls = []

            # Loop through the <li> elements and extract the image URLs
            for i, li_element in enumerate(li_elements[:3], start=1):
                image_element = li_element.find_element(By.TAG_NAME, 'img')
                image_url = image_element.get_attribute('src')
                image_urls.append(image_url)

            # Output the image URLs
            for idx, iURL in enumerate(image_urls, start=1):
                print(f"Image {idx}: {iURL}")

            return image_urls

        finally:
            # Close the browser when done
            driver.quit()


def change_and_print_number(new_number):
    # Load the Word document
    template_path = "C:/Users/wangk/PycharmProjects/ExtractImage/Label.docx"
    doc = Document(template_path)

    # Find the bolded number and replace it with the new number
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            if run.bold:
                run.text = new_number

    # Save the modified document as a temporary file
    modified_doc_path = "modified_template.docx"
    doc.save(modified_doc_path)

    # Send the document to the printer
    win32api.ShellExecute(0, "print", f"{modified_doc_path}", None, ".", 0)

    # Remove the temporary file
    time.sleep(5)
    os.remove(modified_doc_path)


def download_images(image_urls, lot):
    # Folder where you want to save the images
    save_folder = PHOTO_FOLDER
    auction_num = AUCTION_NUM
    prefix = ''

    digits = int(math.log10(int(lot))) + 1
    if digits == 1:
        prefix = '000'
    elif digits == 2:
        prefix = '00'
    elif digits == 3:
        prefix = '0'

    # change_and_print_number(f"{auction_num}{prefix}{lot}")

    # Check if the folder exists, if not, create it
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Loop through the image URLs and download the images
    for i, image_url in enumerate(image_urls):
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # Get the file extension from the URL
            file_extension = image_url.split(".")[-1]
            # Save the image to the specified folder
            image_name = os.path.join(save_folder, f"{auction_num}{prefix}{lot}_{str(i+1)}.{file_extension}")
            with open(image_name, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print("Image {} downloaded and saved as {}".format(i + 1, image_name))

    return True

'''
def take_photos(take=False):
    # Open the webcam
    cap = cv2.VideoCapture(0)  # 0 represents the default camera (usually the built-in webcam)

    if not cap.isOpened():
        print("Error: Could not open the webcam.")
        exit()

    while take:
        # Capture a frame from the webcam
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read a frame from the webcam.")
            cap.release()
            exit()

        # Specify the folder to save the captured image
        save_folder = "C:/Users/wangk/Documents/TestPhotos/"  # Replace with your desired folder path

        # Save the captured frame as an image file in the specified folder
        image_filename = os.path.join(save_folder, "captured_image.jpg")
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")

        response = input("Keep taking photo? (y/n)  ")

        if response != 'y':
            take = False

    # Release the webcam
    cap.release()
'''

if __name__ == "__main__":
    # Read the URL from the command-line argument
    if len(sys.argv) > 2:
        url = sys.argv[1]
        lot = sys.argv[2]
        # Call the function with the URL as an argument
        print(download_images(get_image_urls(url), lot))
    else:
        print("Please provide a URL and lot number.")
