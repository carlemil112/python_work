import cv2 as cv
import numpy as np
import os
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Main function containing the backbone of the program
def main():
    print("+-------------------------------+")
    print("| King Domino points calculator |")
    print("+-------------------------------+")
    image_path = r"C:\Users\carle\Desktop\python_work\p0\King Domino dataset\4.jpg"
    if not os.path.isfile(image_path):
        print("Image not found")
        return
    image = cv.imread(image_path)
    tiles = get_tiles(image)
    print(len(tiles))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            print(f"Tile ({x}, {y}):")
            print(get_terrain(tile))
            print("=====")

# Break a board into tiles
def get_tiles(image):
    tiles = []
    for y in range(5):
        tiles.append([])
        for x in range(5):
            tiles[-1].append(image[y*100:(y+1)*100, x*100:(x+1)*100])
    return tiles

# Determine the type of terrain in a tile
def get_terrain(tile : np.ndarray):
    rows, colums, _ = tile.shape

    pixel_values = []

    for y in range(rows):
        for x in range(colums):
            blue, green, red = tile[x, y]
            pixel_value = categorize_pixel(red, green, blue)
            if (pixel_value != None):
                pixel_values.append(pixel_value)
    
    light_green, dark_green, blue, black, yellow, brown, white, grey = get_pixel_percentage(pixel_values)

    return get_tile_type(light_green, dark_green, blue, black, yellow, brown, white, grey)

def categorize_pixel(r: int, g: int, b: int) -> str:
    light_green = [(103, 161, 15), (82, 149, 17), (59, 123, 11)]
    dark_green = [(23, 59, 11), (55, 89, 38), (41, 95, 20), (31, 48, 29), (21, 35, 12)]
    blue = [(0, 83, 179), (0, 55, 118)]
    black = [(18, 16, 17)]
    yellow = [(194, 175, 11), (196, 156, 7), (180, 157, 1), (186, 162, 4)]
    brown = [(68, 45, 1)]
    white = [(154, 149, 145)]
    grey = [(131, 125, 93), (140, 128, 80), (119, 101, 53), (122, 113, 84), (110, 97, 44)]

    color_list = [light_green, dark_green, blue, black, yellow, brown, white, grey]

    closest_value = 9999
    closest_color = None

    for color_collection in color_list:

        for color in color_collection:
            closeness = calculate_closeness((r, g, b), color)
            if closeness < closest_value:
                closest_value = closeness
                closest_color = color_collection

    if closest_color == light_green:
        return "Lys Grøn"
    elif closest_color == dark_green:
        return "Mørk Grøn"
    elif closest_color == blue:
        return 'Blå'
    elif closest_color == black:
        return 'Sort'
    elif closest_color == yellow:
        return 'Gul'
    elif closest_color == brown:
        return 'Brun'
    elif closest_color == white:
        return 'Hvid'
    elif closest_color == grey:
        return 'Grå'
    else:
        return 'Ukendt'

# Calculate the "closeness" of two colors
def calculate_closeness(check_color : tuple[int, int, int], target_color : tuple[int, int, int]) -> float:
    red_closeness = exp_function(abs(check_color[0] - target_color[0]))
    blue_closeness = exp_function(abs(check_color[1] - target_color[1]))
    green_closeness = exp_function(abs(check_color[2] - target_color[2])) 

    return red_closeness + blue_closeness + green_closeness

def exp_function(val : np.float64):
    return val *((val ** 2) * 0.05 + 1)

#light_green, dark_green, blue, black, yellow, brown, white, grey
def get_pixel_percentage(pixel_values : list[str]):
    count = len(pixel_values)
    light_green, dark_green, blue, black, yellow, brown, white, grey = 0, 0, 0, 0, 0, 0, 0, 0
    
    for pixel in pixel_values:
        if pixel == "Sort":
            black += 1
        elif pixel == "Hvid":
            white += 1
        elif pixel == "Grå":
            grey += 1
        elif pixel == "Gul":
            yellow += 1
        elif pixel == "Brun":
            brown += 1
        elif pixel == "Lys Grøn":
            light_green += 1
        elif pixel == "Mørk Grøn":
            dark_green += 1
        elif pixel == "Blå":
            blue += 1
            
    return light_green / count * 100, dark_green / count * 100, blue / count * 100, black / count * 100, yellow / count * 100, brown / count * 100, white / count * 100, grey / count * 100

def get_tile_type(light_green : float, dark_green : float, blue : float, black : float, yellow : float, brown : float, white : float, grey : float) -> str:

    if light_green >= 40.0 or light_green >= 20.0 and brown >= 10.0:
        return "Eng"
    if blue >= 18.0:
        return "Hav"
    if yellow >= 35.0 or yellow >= 25.0 and brown >= 5.0:
        return "Mark"
    if grey >= 30.0 or grey >= 20.0 and brown >= 10.0:
        return "Sump"
    if dark_green >= 30.0:
        return "Skov"
    if black >= 20.0 or black >= 10.0 and grey >= 10.0 and brown >= 10.0:
        return "Mine"

    return "Unknown"

#CONFUSION MATRIX
import os
import cv2 as cv
import numpy as np
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# Folder where the images are stored
image_folder = r'C:\Users\carle\Desktop\python_work\p0\King Domino dataset'


def get_actual_labels(filename): #Definationen af de faktiske labels
    print(f"Processing filename: {filename}") #Viser hvilken fil der er under processing
    
    corrected_filename = 'image_' + filename  # Adjust this to match your actual labels dictionary keys
    
    # De faktiske labels
    actual_labels = {
        'image_1.jpg': [['Eng', 'Hav', 'Skov', 'Skov', 'Skov'],
                        ['Eng', 'Skov', 'Skov', 'Skov', 'Eng'],
                        ['Eng', 'Sump', 'Unknown', 'Skov', 'Eng'],
                        ['Eng', 'Sump', 'Hav', 'Eng', 'Eng'],
                        ['Skov', 'Hav', 'Hav', 'Eng', 'Mark']],
       
        'image_2.jpg': [['Eng', 'Sump', 'Mark', 'Mine', 'Sump'],
                        ['Mine', 'Sumo', 'Mark', 'Mark' ]]
        
        # Flere skal tilføjes
    }
    
    if corrected_filename not in actual_labels: #Check om filnavnet er skrevet rigtigt i actual_labels
        print(f"Warning: Filename {corrected_filename} not found in actual labels dictionary. Skipping this image.")
        return None  
    
    return actual_labels[corrected_filename]

def predict_label(tile): #Funktion der forudsiger label
    return get_terrain(tile)

actual_labels_all = []
predicted_labels_all = []


for filename in os.listdir(image_folder): #Looper alle billeder i mappen
    if filename.endswith(".jpg"):  # Sikre det er en jpg.fil
        image_path = os.path.join(image_folder, filename)
        image = cv.imread(image_path)

        # Få det faktiske label (5x5 grid of labels)
        actual_labels = get_actual_labels(filename)
        
        # Hvis der ikke er labels defineret, springes billede over
        if actual_labels is None:
            continue
        
        tiles = get_tiles(image)  
        
        # Looper hver tile (5x5 grid)
        for y in range(5):
            for x in range(5):
                # Get the actual label for this tile
                actual_label = actual_labels[y][x]
                actual_labels_all.append(actual_label)

                # Predict the label for the current tile
                tile = tiles[y][x]
                predicted_label = predict_label(tile)
                predicted_labels_all.append(predicted_label)

# Konverter til numpy:
actual_labels_all = np.array(actual_labels_all)
predicted_labels_all = np.array(predicted_labels_all)

# Udregning af confusion matrix
cm = confusion_matrix(actual_labels_all, predicted_labels_all)
accuracy = accuracy_score(actual_labels_all, predicted_labels_all)
precision = precision_score(actual_labels_all, predicted_labels_all, average='weighted')
recall = recall_score(actual_labels_all, predicted_labels_all, average='weighted')
f1 = f1_score(actual_labels_all, predicted_labels_all, average='weighted')

# Print alle resultater
print("Confusion Matrix:\n", cm)
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
