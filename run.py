import subprocess
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
import os

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

def run_c_program(rows, cols):
    range_val = 10 # work in progress, don't mind it
    subprocess.run(['./process', str(rows), str(cols), str(range_val), 'input.txt'])

def main(image_path, new_width):
    array = prepare(image_path, new_width)
    rows, cols = array.shape
    write_array_to_file(array, 'input.txt')
    run_c_program(rows, cols,)
    result_array = read_array_from_file('data.txt')
    finish(result_array)

if __name__ == "__main__":
    image_path = 'test_imgs/street.png'  # Change this to your image path
    new_width = 200
    main(image_path, new_width)