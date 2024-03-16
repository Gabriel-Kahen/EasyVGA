from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import time

def image_to_array(image_path, new_width, threshold):
    image = Image.open(image_path)
    width, height = image.size
    image = image.resize((new_width, int(new_width * height / width))).convert("L")
    image_array = np.array(image)
    binary_array = (image_array < threshold).astype(int)
    for row in range(binary_array.shape[0]):
        for col in range(binary_array.shape[1]):
            if binary_array[row][col] == 1:
                binary_array[row][col] = -1
    return binary_array

def array_to_txt(array):
    with open('output.txt', 'w') as file:
        for row in range(array.shape[0]):
            for col in range(array.shape[1]):
                if array[row][col] == 0:
                    file.write(" ")
                file.write(str(array[row][col]) + " ")
            file.write("\n")

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

def calculate(array):
    start_time = time.time()  # Start the stopwatch
    rows, cols = array.shape
    visibility_counts = [[0] * cols for _ in range(rows)]
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] == 0:
                for test_row in range(rows):
                    for test_col in range(cols):
                        if array[test_row][test_col] == 0:
                            line_points = bresenham(current_col, current_row, test_col, test_row)
                            blocked = False
                            for point in line_points:
                                x, y = point
                                if array[y][x] == -1:
                                    blocked = True
                                    break
                            if not blocked:
                                visibility_counts[current_row][current_col] += 1

    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] == 0:
                array[current_row][current_col] = visibility_counts[current_row][current_col]

    end_time = time.time()  # Stop the stopwatch
    execution_time = end_time - start_time  # Calculate execution time
    print("Execution Time:", execution_time, "seconds")

    return array


def clean(array):
    rows = array.shape[0]
    cols = array.shape[1]
    min = float("inf")
    max = float("0")
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != -1 and array[current_row][current_col] < min:
                min = array[current_row][current_col]
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != -1:
                array[current_row][current_col] -= min
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] != -1 and array[current_row][current_col] > max:
                max = array[current_row][current_col]
    ratio = 255/max
    for current_row in range(rows):
        for current_col in range(cols):
            if array[current_row][current_col] == -1:
                array[current_row][current_col] = 0
            else:
                array[current_row][current_col] = array[current_row][current_col] * ratio + 1
    return array

def array_to_colored_image(array):
    color_map = plt.colormaps['jet']
    color_map_colors = color_map(np.arange(256))
    color_map_colors[0] = [0, 0, 0, 1]
    modified_color_map = plt.cm.colors.ListedColormap(color_map_colors)
    colored_array = modified_color_map(array / 256.0)[:, :, :3]
    colored_image = Image.fromarray((colored_array * 255).astype('uint8'), mode='RGB')
    return colored_image
    
def execute(image_path, output_path, calculate_width, threshold):
    image = Image.open(image_path)
    original_width, original_height = image.size
    arr = image_to_array(image_path, calculate_width, threshold)
    arr = calculate(arr)
    arr = clean(arr)
    final_image = array_to_colored_image(arr)
    #final_image = final_image.resize((original_width, original_height), Image.LANCZOS) #gotta figure out what sampling filter to use
    final_image.save(output_path)

#image_path = 'test1.png'
#image_path = 'test2.png'
image_path = "test3.png"
output_path = 'output.png'
calculate_width = 40
threshold = 100

execute(image_path, output_path, calculate_width, threshold)