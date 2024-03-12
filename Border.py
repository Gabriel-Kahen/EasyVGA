from PIL import Image
import numpy as np

def image_to_array(image_path, new_width, threshold):
    image = Image.open(image_path)
    width, height = image.size
    image = image.resize((new_width, int(new_width * height / width))).convert("L")
    image_array = np.array(image)
    binary_array = (image_array > threshold).astype(np.uint8)
    return binary_array

def is_surrounded(row, col, array):
    #try to optimize
    for r in range(-1, 2):
        for c in range(-1, 2):
            if r == 0 and c == 0:
                continue  
            current_row, current_col = row + r, col + c
            if 0 <= current_row < len(array) and 0 <= current_col < len(array[0]):
                if array[current_row][current_col] != 0:
                    return False
    return True

def make_txt_file(arr):
    with open('output.txt', 'w') as file:
        for row in arr:
            file.write(' '.join(map(str, row)) + '\n')
            
def make_border_array(arr):
    num_rows, num_cols = arr.shape
    border_arr = np.full((num_rows, num_cols), "0", dtype=object)
    for r in range(num_rows):
        for c in range(num_cols):
            if arr[r][c] == 0:
                if not is_surrounded(r, c, arr):
                    border_arr[r][c] = 1
            else:
                border_arr[r][c] = 0
    return border_arr
    
def array_to_image(arr, output_path):
    # Convert the array to a PIL image
    image = Image.fromarray((arr * 255).astype('uint8'), mode='L')
    # Save the image to the specified output path
    image.save(output_path)
    
#image_path = '12x12PLUS.png'
image_path = 'GABE.png'
#image_path = 'testgraph.png'
output_path = 'output.png'
width = 2000
threshold = 100

arr = image_to_array(image_path, width, threshold)
border_arr = make_border_array(arr)
array_to_image(border_arr, output_path)