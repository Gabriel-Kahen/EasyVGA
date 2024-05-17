import subprocess
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

def prepare(image_path, new_width, threshold):
    image = Image.open(image_path)
    original_width, original_height = image.size
    image_array = np.array(image.convert("L"))
    resized_height = int(new_width * image_array.shape[0] / image_array.shape[1])
    image_array = np.array(Image.fromarray(image_array).resize((new_width, resized_height), resample=Image.BOX))
    arr = (image_array < threshold).astype(int)
    arr[arr == 1] = -1
    return np.array(arr)

def finish(array):
    array = np.array(array)
    color_map = plt.cm.jet
    color_map_colors = color_map(np.arange(256))
    color_map_colors[0] = [0, 0, 0, 1]
    color_map_colors[1] = [0, 0, 0, 1]
    modified_color_map = plt.cm.colors.ListedColormap(color_map_colors)
    rows, cols = array.shape
    min_value = np.inf
    max_value = 1
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
    colored_array = modified_color_map(array / 256.0)[:, :, :3]
    colored_image = Image.fromarray((colored_array * 255).astype('uint8'), mode='RGB')
    colored_image.save("app/static/images/output.png")

def run_c_program(rows, cols, range_val, array):        
    array_elements_str = " ".join(map(str, array.flatten()))
    process = subprocess.run(["app/process", str(rows), str(cols), str(range_val), array_elements_str], capture_output=True)
    stdout = process.stdout
    stderr = process.stderr