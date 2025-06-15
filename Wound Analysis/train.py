import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras import layers, Model
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, jaccard_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from tensorflow.keras.optimizers import Adam

# Remove weight_decay and recompile the model


# Set paths to the directories
train_dir = 'train_images'
truth_dir = 'train_masks'

# Parameters
img_size = (128, 128)  # Adjust as needed
num_images = 1000  # Number of images to use from the dataset

# Load and preprocess images
def load_images(train_dir, truth_dir, img_size, num_images):
    train_images = []
    truth_images = []
    
    train_files = os.listdir(train_dir)[:num_images]  # Limit to the first 500 images
    
    for filename in train_files:
        train_path = os.path.join(train_dir, filename)
        
        # Modify the filename to match the ground truth file
       # truth_filename = filename.replace('.jpg')
        truth_path = os.path.join(truth_dir, filename)
        
        if not os.path.isfile(truth_path):
            print(f"Warning: Ground truth image {truth_path} not found")
            continue
        
        train_image = cv2.imread(train_path, cv2.IMREAD_GRAYSCALE)
        truth_image = cv2.imread(truth_path, cv2.IMREAD_GRAYSCALE)
        
        if train_image is None:
            print(f"Warning: Could not read train image {train_path}")
            continue
        
        if truth_image is None:
            print(f"Warning: Could not read truth image {truth_path}")
            continue
        
        train_image = cv2.resize(train_image, img_size)
        truth_image = cv2.resize(truth_image, img_size)
        
        train_images.append(train_image)
        truth_images.append(truth_image)
    
    train_images = np.array(train_images, dtype=np.float32) / 255.0
    truth_images = np.array(truth_images, dtype=np.float32) / 255.0
    
    train_images = np.expand_dims(train_images, axis=-1)
    truth_images = np.expand_dims(truth_images, axis=-1)
    
    return train_images, truth_images

# Load the images
train_images, truth_images = load_images(train_dir, truth_dir, img_size, num_images)

# Split the data into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(train_images, truth_images, test_size=0.1, random_state=42)

def unet_model(input_shape):
    inputs = tf.keras.Input(input_shape)

    # Encoder
    c1 = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(inputs)
    p1 = layers.MaxPooling2D((2, 2))(c1)

    c2 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(p1)
    p2 = layers.MaxPooling2D((2, 2))(c2)

    # Bottleneck
    c3 = layers.Conv2D(64, (3, 3), activation='relu', padding='same')(p2)

    # Decoder
    u4 = layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c3)
    u4 = layers.concatenate([u4, c2])
    c4 = layers.Conv2D(32, (3, 3), activation='relu', padding='same')(u4)

    u5 = layers.Conv2DTranspose(16, (2, 2), strides=(2, 2), padding='same')(c4)
    u5 = layers.concatenate([u5, c1])
    c5 = layers.Conv2D(16, (3, 3), activation='relu', padding='same')(u5)

    outputs = layers.Conv2D(1, (1, 1), activation='sigmoid')(c5)

    model = Model(inputs=[inputs], outputs=[outputs])
    return model

# Define the model
input_shape = (img_size[0], img_size[1], 1)  # Adjust as needed
model = unet_model(input_shape)

# Compile the model
model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])


# Print the model summary
model.summary()

# Training the model
history = model.fit(
    x_train, y_train,
    epochs=5,
    batch_size=32,
    validation_data=(x_val, y_val)
)

# Save the model
model.save('unet_model.h5')


