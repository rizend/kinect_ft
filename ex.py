from freenect import sync_get_depth as get_depth, sync_get_video as get_video
from ft import ftclient

f = ftclient()

error_color = (255, 0, 0)

SQUARE_DIM = 13

def extract_depth_pixel(arr, row, col):
    values = []
    val = 0
    for i in range(SQUARE_DIM):
        for j in range(SQUARE_DIM):
            val = arr[row * SQUARE_DIM + i][col * SQUARE_DIM + j]
            if val != 0 and val != 2047:
                values.append(val)
    if len(values) < 1:
        return error_color
    values.sort()
    val = values[len(values) // 2]
    val = val // 4
    if val > 255:
        return [0, val - 256, 0]
    return [0, 0, val]

def show_depth_image(depth_array):
    for col in range(45):
        for row in range(35):
            f.set(col, row, extract_depth_pixel(depth_array, row, col))
    f.show()

def doloop():
    global depth, rgb
    while True:
        # Get a fresh frame
        (depth,_) = get_depth()
        show_depth_image(depth)

doloop()
