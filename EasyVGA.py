from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from numba import jit
import osmnx as ox

@jit(nopython=True)
def bresenham(x0, y0, x1, y1):
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = -1 if x0 > x1 else 1
    sy = -1 if y0 > y1 else 1
    err = dx - dy
    while True:
        points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points

@jit(nopython=True)
def calculate(array):
    rows, cols = array.shape
    visibility_counts = np.zeros_like(array)
    total_iterations = rows * cols
    processed_iterations = 0
    
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row, current_col] == 0:
                for test_row in range(rows):
                    for test_col in range(cols):
                        if array[test_row, test_col] == 0:
                            line_points = bresenham(current_col, current_row, test_col, test_row)
                            blocked = False
                            for point in line_points:
                                x, y = point
                                if array[y, x] == -1:
                                    blocked = True
                                    break
                            if not blocked:
                                visibility_counts[current_row, current_col] += 1
            print(int(processed_iterations/total_iterations * 10000)/100, "%")
            processed_iterations += 1
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row, current_col] == 0:
                array[current_row, current_col] = visibility_counts[current_row, current_col]
    print("Done!")
    return array

def clean(array):
    rows, cols = array.shape
    min_value = np.inf
    max_value = 0
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != -1 and array[current_row][current_col] < min_value:
                min_value = array[current_row][current_col]
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != -1:
                array[current_row][current_col] -= min_value
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != -1 and array[current_row][current_col] > max_value:
                max_value = array[current_row][current_col]
    ratio = 255 / max_value
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] == -1:
                array[current_row][current_col] = 0
            else:
                array[current_row][current_col] = array[current_row][current_col] * ratio + 1
    return array

def execute(image_path, output_path, calculate_width, threshold):
    print("Processing...")
    image = Image.open(image_path)
    original_width, original_height = image.size
    image_array = np.array(image.convert("L"))
    new_width = calculate_width
    resized_height = int(new_width * image_array.shape[0] / image_array.shape[1])
    image_array = np.array(Image.fromarray(image_array).resize((new_width, resized_height), resample=Image.BOX))
    binary_array = (image_array < threshold).astype(int)
    binary_array[binary_array == 1] = -1 
    binary_array = calculate(binary_array)
    binary_array = clean(binary_array) 
    color_map = plt.cm.jet
    color_map_colors = color_map(np.arange(256))
    color_map_colors[0] = [0, 0, 0, 1]
    modified_color_map = plt.cm.colors.ListedColormap(color_map_colors)
    colored_array = modified_color_map(binary_array / 256.0)[:, :, :3]
    colored_image = Image.fromarray((colored_array * 255).astype('uint8'), mode='RGB')
    colored_image.save(output_path)

def save_street_network_image(max_lat, min_lat, max_lon, min_lon, filename):
    graph = ox.graph_from_bbox(max_lat, min_lat, max_lon, min_lon, network_type='all')
    fig, ax = ox.plot_graph(graph, bgcolor='black', edge_color='white', node_color='white', node_size=500, edge_linewidth=20, show=False)
    plt.savefig(filename, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

def main():
    threshold = 100
    output_path = "output.png"
    type = input("Type '1' if you are using coordinates, type '2' if you are using a custom image: ")
    if type == "1":
        max_coords = (float(input("Max Latitude: ")), float(input("Max Longitude: ")))
        min_coords = (float(input("Min Latitude: ")), float(input("Min Longitude: ")))
        width = int(input("Width: "))
        
        image_path = "street.png"
        bounds = (min_coords[0], min_coords[1], max_coords[0], max_coords[1])
        save_street_network_image(bounds[2], bounds[0], bounds[3], bounds[1], image_path)
        execute(image_path, output_path, width, threshold)
    else:
        image_path = input("Image Path: ")
        width = int(input("Width: "))
        
        execute(image_path, output_path, width, threshold)
    
if __name__ == "__main__":
   main()