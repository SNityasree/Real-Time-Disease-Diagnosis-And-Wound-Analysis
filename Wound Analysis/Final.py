import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import cv2
import tensorflow as tf
import requests
import imutils


# Load the trained model
model = tf.keras.models.load_model('2unet_model.h5')

# Parameters
img_size = (128, 128)

# Healing rate assumption (pixels per day, arbitrary example)
PIXELS_PER_DAY = 5000

ESP32_CAM_URL = "http://192.168.137.136/capture"

def predict_image(image):
    original_size = image.shape
    resized_image = cv2.resize(image, img_size)
    resized_image = resized_image.astype(np.float32) / 255.0
    resized_image = np.expand_dims(resized_image, axis=-1)
    resized_image = np.expand_dims(resized_image, axis=0)

    # Predict the segmentation mask
    prediction = model.predict(resized_image)
    prediction = (prediction[0, :, :, 0] > 0.5).astype(np.uint8) * 255

    # Resize prediction to the original image size
    prediction = cv2.resize(prediction, (original_size[1], original_size[0]), interpolation=cv2.INTER_NEAREST)

    return prediction

def calculate_healing_time(mask, original_size):
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    total_area = sum(cv2.contourArea(contour) for contour in contours)
    healing_days = total_area / PIXELS_PER_DAY
    
    # Calculate affected area percentage
    total_pixels = original_size[0] * original_size[1]
    affected_percentage = (total_area / total_pixels) * 100
    
    return round(healing_days, 2), round(affected_percentage, 2)

def draw_bounding_box(image, mask):
    image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(image)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        draw.rectangle([x, y, x + w, y + h], outline="red", width=2)
    
    return image

def capture_and_analyze():
    response = requests.get(ESP32_CAM_URL)
    if response.status_code == 200:
        image_arr = np.frombuffer(response.content, np.uint8)
        image = cv2.imdecode(image_arr, cv2.IMREAD_COLOR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        segmented_image = predict_image(gray_image)
        healing_days, affected_percentage = calculate_healing_time(segmented_image, image.shape)
        
        segmented_image_pil = Image.fromarray(segmented_image)
        segmented_image_pil.thumbnail((256, 256))
        segmented_photo = ImageTk.PhotoImage(segmented_image_pil)
        segmented_label.config(image=segmented_photo)
        segmented_label.image = segmented_photo

        bounded_image = draw_bounding_box(image, segmented_image)
        bounded_image.thumbnail((256, 256))
        bounded_photo = ImageTk.PhotoImage(bounded_image)
        bounded_label.config(image=bounded_photo)
        bounded_label.image = bounded_photo
        
        healing_label.config(text=f"Estimated Healing Time: {healing_days} days")
        affected_label.config(text=f"Affected Area: {affected_percentage}%")
        


# Create the main window
root = tk.Tk()
root.title("Real-Time Image Segmentation with ESP32-CAM")

# Create frames for layout
frame = tk.Frame(root)
frame.pack(pady=10)

# Create and place the segmented image label
segmented_label = tk.Label(frame, text="Segmented Image")
segmented_label.grid(row=0, column=0, padx=10, pady=10)

# Create and place the bounded image label
bounded_label = tk.Label(frame, text="Bounded Image")
bounded_label.grid(row=0, column=1, padx=10, pady=10)

# Create and place the healing time label
healing_label = tk.Label(root, text="Estimated Healing Time: ")
healing_label.pack(pady=5)

# Create and place the affected area label
affected_label = tk.Label(root, text="Affected Area: ")
affected_label.pack(pady=5)

# Create and place the capture button
capture_button = tk.Button(root, text="Capture & Analyze", command=capture_and_analyze)
capture_button.pack(pady=20)

# Start the Tkinter event loop
root.mainloop()
