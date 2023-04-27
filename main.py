import os
import time
import subprocess
from PIL import Image
import pytesseract
from tkinter import filedialog
import tkinter as tk

# Check if Tesseract is installed
try:
    output = subprocess.check_output(["pip", "show", "pytesseract"]).decode("utf-8")
    if "Version: 0.3.10" not in output:
        raise Exception("pytesseract is not installed")
except Exception as e:
    print("pytesseract is not installed on your device.")
    install_tesseract = input("Do you want to install Tesseract now? (y/n) ")
    if install_tesseract.lower() == "y":
        # Install Tesseract
        subprocess.run(["pip", "install", "pytesseract"])
        # Check if installation was successful
        try:
            output = subprocess.check_output(["pip", "show", "pytesseract"]).decode("utf-8")
            if "Version: 0.3.10" not in output:
                raise Exception("Tesseract installation failed")
            else:
                print("Tesseract installation successful.")
        except Exception as e:
            print("Tesseract installation failed.")
            exit()

# Create a Tkinter root window (required for file dialog)
root = tk.Tk()
root.withdraw()

# Ask user to select the directory containing the images
while True:
    image_folder_path = filedialog.askdirectory(title="Select Directory Containing Images")
    if not os.path.exists(image_folder_path):
        print("Invalid directory path, please try again.")
    else:
        break

# Ask user to enter the path of Tesseract executable
while True:
    tesseract_path = input("Enter the directory of Tesseract executable: (NOTE:IT LOOKS LIKE THIS-- C:\ ur name \gayat\AppData\Local\Programs\Tesseract-OCR ")
    if not os.path.isfile(os.path.join(tesseract_path, 'tesseract.exe')):
        print("Invalid Tesseract directory.")
    else:
        break

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')

# Ask user to enter the word to be searched
deleting_file = input("Enter the word you want to search for: ")
img_paths = []

# Keep track of whether any files were found and deleted
files_deleted = False

# Loop over all image files in the directory
for filename in os.listdir(image_folder_path):
    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
        # Check if the search word is present in the image
        file_path = os.path.join(image_folder_path, filename)
        img = Image.open(file_path)
        # Thresholding to improve text detection
        img = img.convert('L')
        threshold = 200
        img = img.point(lambda p: p > threshold and 255)
        text = pytesseract.image_to_string(img)
        if deleting_file.lower() in text.lower():
            # Display the file name for 3 seconds
            print(f"File '{filename}' containing the word '{deleting_file}' will be deleted in 3 seconds...")
            time.sleep(3)
            # Remove the file
            os.remove(file_path)
            # Mark that at least one file was deleted
            files_deleted = True

# Print a message if no files were found and deleted
if not files_deleted:
    print(f"No files containing the word '{deleting_file}' were found.")
else:
    print("Done.")

