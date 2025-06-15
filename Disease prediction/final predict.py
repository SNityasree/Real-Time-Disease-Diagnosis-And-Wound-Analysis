import pandas as pd
import random

# Define the number of samples per category
num_per_category = 200
categories = [
    "Hyperhidrosis", "Arthritis", "Osteoporosis", "Infection-Related Disorder", "Joint Disorder",
    "Parkinson's Disease", "Gout", "Fibromyalgia", "Rheumatoid Arthritis", "Metabolic Bone Disorder", "Normal"
]

# Initialize an empty list to store data
dataset = []

# Function to generate random values within specified ranges
def generate_values(label):
    bpm = random.randint(50, 130)
    spo2 = random.randint(85, 100)
    temp = random.uniform(35.0, 41.0)
    ppg = random.uniform(0.5, 3.0)
    movement = random.randint(0, 100)
    piezo = random.randint(0, 1024)
    flex = random.randint(0, 1024)
    gas = random.randint(0, 1024)

    # Define conditions based on label
    if label == "Hyperhidrosis":
        bpm = random.randint(100, 130)
        temp = random.uniform(38.5, 41.0)
        spo2 = random.randint(85, 89)
    elif label == "Arthritis":
        flex = random.randint(800, 1024)
        piezo = random.randint(700, 1024)
        movement = random.randint(0, 20)
    elif label == "Osteoporosis":
        movement = random.randint(0, 10)
        spo2 = random.randint(85, 87)
    elif label == "Infection-Related Disorder":
        temp = random.uniform(39.0, 41.0)
        gas = random.randint(800, 1024)
    elif label == "Joint Disorder":
        ppg = random.uniform(0.5, 0.8)
        flex = random.randint(900, 1024)
    elif label == "Parkinson's Disease":
        movement = random.randint(80, 100)
        piezo = random.randint(800, 1024)
    elif label == "Gout":
        flex = random.randint(0, 300)
        temp = random.uniform(35.0, 36.0)
        gas = random.randint(500, 1024)
    elif label == "Fibromyalgia":
        bpm = random.randint(110, 130)
        movement = random.randint(0, 30)
        flex = random.randint(600, 1024)
    elif label == "Rheumatoid Arthritis":
        flex = random.randint(700, 1024)
        piezo = random.randint(900, 1024)
        movement = random.randint(0, 15)
    elif label == "Metabolic Bone Disorder":
        spo2 = random.randint(80, 85)
        ppg = random.uniform(0.5, 0.7)
        movement = random.randint(0, 10)

    return [bpm, spo2, temp, ppg, movement, piezo, flex, gas, label]

# Generate data for each category
for category in categories:
    for _ in range(num_per_category):
        dataset.append(generate_values(category))

# Convert dataset to DataFrame and shuffle it
df = pd.DataFrame(dataset, columns=["bpm", "spo2", "temperature", "ppg", "movement", "piezo", "flex", "gas", "label"])
df = df.sample(frac=1).reset_index(drop=True)  # Shuffle dataset

# Save dataset to CSV
df.to_csv("disease_prediction_dataset.csv", index=False)

print("Dataset created with at least 200 samples per category and saved as 'disease_prediction_dataset.csv'.")

