#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

void printArray(int **array, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%d ", array[i][j]);
        }
        printf("\n");
    }
}

void string_to_2d_array(int rows, int cols, char* chars, int **array) {
    char *token = strtok(chars, "[], ");
    int index = 0;
    while (token != NULL) {
        array[index / cols][index % cols] = atoi(token);
        index++;
        token = strtok(NULL, "[], ");
    }
}

void writeArrayToFile(int **arr, int rows, int cols, const char *filename) {
    FILE *file = fopen(filename, "w");
    if (file == NULL) {
        printf("Error opening file.\n");
        return;
    }

    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            fprintf(file, "%d ", arr[i][j]);
        }
        fprintf(file, "\n");
    }

    fclose(file);
    printf("Array written to %s successfully.\n", filename);
}

int** createArray(int rows, int cols) {
    int **array = (int **)malloc(rows * sizeof(int *));
    if (!array) {
        printf("Error: Memory allocation failed\n");
        return NULL;
    }

    for (int i = 0; i < rows; i++) {
        array[i] = (int *)malloc(cols * sizeof(int));
        if (!array[i]) {
            printf("Error: Memory allocation failed\n");
            for (int j = 0; j < i; j++) {
                free(array[j]);
            }
            free(array);
            return NULL;
        }
    }
    return array;
}

bool inBounds(int x, int y, int width, int height) {
    return x >= 0 && x < width && y >= 0 && y < height;
}

void countVisibleZeros(int **image_array, int width, int height, int **result) {
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            if (image_array[y][x] == 0) {
                int count = 0;

                for (int yy = 0; yy < height; yy++) {
                    for (int xx = 0; xx < width; xx++) {
                        if (image_array[yy][xx] == 0 && (x != xx || y != yy)) {
                            bool visible = true;

                            int dx = xx - x;
                            int dy = yy - y;
                            int steps = abs(dx) > abs(dy) ? abs(dx) : abs(dy);
                            float xStep = (float)dx / steps;
                            float yStep = (float)dy / steps;
                            float xCheck = x + 0.5;
                            float yCheck = y + 0.5;

                            for (int i = 0; i < steps; i++) {
                                xCheck += xStep;
                                yCheck += yStep;

                                int xi = (int)xCheck;
                                int yi = (int)yCheck;

                                if (!inBounds(xi, yi, width, height) || image_array[yi][xi] == -1) {
                                    visible = false;
                                    break;
                                }
                            }

                            if (visible) {
                                count++;
                            }
                        }
                    }
                }

                result[y][x] = count;
            }
        }
    }
}

int main(int argc, char *argv[]) {

    if (argc < 4) {
        printf("Usage: %s <rows> <cols> <range> <array elements...>\n", argv[0]);
        return 1;
    }

    int rows = atoi(argv[1]);
    int cols = atoi(argv[2]);
    int range = atoi(argv[3]);
    
    int** input = createArray(rows, cols);
    int** result = createArray(rows, cols);

    string_to_2d_array(rows, cols, argv[4], input);

    countVisibleZeros(input, cols, rows, result);

    writeArrayToFile(result, rows, cols, "data.txt");

    return 0;
}

// compile: gcc process.c -o process

//still have to make the algorithm better
//and add range bruh