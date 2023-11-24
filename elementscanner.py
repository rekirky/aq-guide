import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import pyautogui
import cv2
import numpy as np
import pygetwindow as gw


class ImageScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Scanner")

        self.folder_path = tk.StringVar()

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Folder selection
        folder_label = tk.Label(self.root, text="Select Folder:")
        folder_label.pack(pady=10)

        folder_entry = tk.Entry(self.root, textvariable=self.folder_path, state="disabled", width=40)
        folder_entry.pack(pady=5, side=tk.LEFT)

        browse_button = tk.Button(self.root, text="Browse", command=self.browse_folder)
        browse_button.pack(pady=5, side=tk.LEFT)

        # Scan button
        scan_button = tk.Button(self.root, text="Scan Images", command=self.scan_images)
        scan_button.pack(pady=10)

        # Screenshot display
        self.screenshot_label = tk.Label(self.root, text="Screenshot will be displayed here.")
        self.screenshot_label.pack(pady=10)

    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        self.folder_path.set(folder_selected)

    def scan_images(self):
        folder_path = self.folder_path.get()

        if not folder_path:
            tk.messagebox.showerror("Error", "Please select a folder.")
            return

        webp_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.webp')]

        if not webp_files:
            tk.messagebox.showinfo("Result", "No WebP files found in the selected folder.")
            return

        for window in gw.getWindowsWithTitle(""):
            if not window.isMinimized:
                for webp_file in webp_files:
                    image_path = os.path.join(folder_path, webp_file)
                    self.check_and_display_image(image_path) 

    def check_and_display_image(self, image_path):
        try:
            # Specify the format explicitly when opening the image
            image = Image.open(image_path).convert("RGB")
            image_tk = ImageTk.PhotoImage(image)

            # Check if the image is being displayed on the screen
            if self.is_image_displayed(image_path):
                tk.messagebox.showinfo("Image Found", f"The image {os.path.basename(image_path)} is being displayed.")

                # Capture and save the screenshot
                screenshot_path = self.capture_full_screen_screenshot()
                tk.messagebox.showinfo("Screenshot Saved", f"Screenshot saved to {screenshot_path}")

        except Exception as e:
            print(f"Error opening image {image_path}: {e}")

    def is_image_displayed(self, image_path):
        # Open the target image
        target_image = cv2.imread(image_path)

        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        screenshot_cv2 = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # Use OpenCV to find the image within the screenshot
        result = cv2.matchTemplate(screenshot_cv2, target_image, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        # Set a threshold for matching
        threshold = 0.8
        if max_val >= threshold:
            return True
        else:
            return False

    def capture_window_screenshot(self, window, output_folder='screenshots', file_format='jpg'):
        print("capture window screenshot")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Generate a unique filename for each screenshot
        screenshot_filename = f"{window.title.replace(' ', '_')}_{window.left}_{window.top}.{file_format}"

        # Capture the content of the window
        left, top, right, bottom = window.left, window.top, window.right, window.bottom
        screenshot = pyautogui.screenshot(region=(left, top, right - left, bottom - top))

        # Save the screenshot to a file
        screenshot_path = os.path.join(output_folder, screenshot_filename)
        screenshot.save(screenshot_path, format=file_format)
        print('yeah')
        return screenshot_path

    def display_screenshot(self, screenshot):
        # Convert the screenshot to a format that can be displayed with ImageTk
        screenshot = ImageTk.PhotoImage(screenshot)

        # Update the label with the new screenshot
        self.screenshot_label.config(image=screenshot)
        self.screenshot_label.image = screenshot
    
    def capture_full_screen_screenshot(self, output_folder='screenshots', file_format='jpg'):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Capture the entire screen
        screenshot = pyautogui.screenshot()
        screenshot_path = os.path.join(output_folder, f"full_screen.{file_format}")
        screenshot.save(screenshot_path, format=file_format)

        return screenshot_path


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageScannerApp(root)
    root.mainloop()