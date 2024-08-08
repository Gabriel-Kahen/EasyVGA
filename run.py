import subprocess
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import os
import osmnx as ox
from math import radians, sin, cos, sqrt, atan2
from scipy.spatial.distance import cdist

def prepare(image_path, new_width):
    threshold = 128 #doesn't matter for black and white inputs, for colored inputs mess around with this value to get correct polarization between walls and space
    image = Image.open(image_path)
    original_width, original_height = image.size
    image_array = np.array(image.convert("L"))
    resized_height = int(new_width * image_array.shape[0] / image_array.shape[1])
    image_array = np.array(Image.fromarray(image_array).resize((new_width, resized_height), resample=Image.BOX))
    arr = (image_array < threshold).astype(int)
    arr[arr == 1] = -1
    return arr

def finish(array):
    array = np.array(array)
    color_map = plt.cm.jet
    color_map_colors = color_map(np.arange(256))
    color_map_colors[0] = [0, 0, 0, 1]
    color_map_colors[1] = [0, 0, 0, 1]
    modified_color_map = plt.cm.colors.ListedColormap(color_map_colors)
    rows, cols = array.shape
    min_value = np.inf
    max_value = 0
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != 0 and array[current_row][current_col] < min_value:
                min_value = array[current_row][current_col]
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != 0:
                array[current_row][current_col] -= min_value - 1
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] > max_value:
                max_value = array[current_row][current_col]
    ratio = 255 / max_value
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != 0:
                array[current_row][current_col] = array[current_row][current_col] * ratio + 1
    colored_array = modified_color_map((array + 1) / 256.0)[:, :, :3]
    colored_image = Image.fromarray((colored_array * 255).astype('uint8'), mode='RGB')
    os.remove("data.txt")
    os.remove("input.txt")
    colored_image.save("output.png")

def write_array_to_file(array, filename):
    with open(filename, 'w') as f:
        rows, cols = array.shape
        for row in range(rows):
            for col in range(cols):
                f.write(f"{array[row][col]} ")
            f.write("\n")

def read_array_from_file(filename):
    with open(filename, 'r') as f:
        array = []
        for line in f:
            array.append([int(x) for x in line.split()])
    return np.array(array)

def save_street_network_image(max_lat, min_lat, max_lon, min_lon, filename):
    graph = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    
    street_width_meter = 3
    node_size_meter = 10
    
    lat_distance = (max_lat - min_lat) * 50
    lon_distance = (max_lon - min_lon) * 50
    
    #if this is smaller, the width should get bigger
    
    edge_linewidth = street_width_meter/min(lat_distance, lon_distance)
    node_size = node_size_meter/min(lat_distance, lon_distance)


    fig, ax = ox.plot_graph(graph, bgcolor='black', edge_color='white', node_color='white', node_size=node_size, edge_linewidth=edge_linewidth, show=False)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

def run_c_program(rows, cols):
    range_val = 10 # work in progress, don't mind it
    subprocess.run(['./process', str(rows), str(cols), str(range_val), 'input.txt'])

def run(image_path, new_width):
    print("Processing...")
    array = prepare(image_path, new_width)
    rows, cols = array.shape
    write_array_to_file(array, 'input.txt')
    run_c_program(rows, cols,)
    result_array = read_array_from_file('data.txt')
    finish(result_array)
    print("Done!")

if __name__ == "__main__":
    image_path = 'test_imgs/street.png'  # Change this to your image path
    new_width = 200
    type = input("Type '1' if you are using coordinates, type '2' if you are using a custom image: ")
    if type == "1":
        max_coords = (float(input("Max Latitude: ")), float(input("Max Longitude: ")))
        min_coords = (float(input("Min Latitude: ")), float(input("Min Longitude: ")))
        width = int(input("Width: "))
        image_path = "test_imgs/street.png"
        print("Loading streets...")
        bounds = (min_coords[0], min_coords[1], max_coords[0], max_coords[1])
        save_street_network_image(bounds[2], bounds[0], bounds[3], bounds[1], image_path)
        run(image_path, width)
    else:
        image_path = input("Image Path: ")
        width = int(input("Width (pixels): "))
        run(image_path, width)