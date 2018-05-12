from multiprocessing import Process, Lock, Array
import freenect
import numpy as np
import ctypes
from ft import ftclient

PAL = [
    [165, 0, 38],
    [215, 48, 39],
    [244, 109, 67],
    [253, 174, 97],
    [254, 224, 144],
    [224, 243, 248],
    [171, 217, 233],
    [116, 173, 209],
    [69, 117, 180],
    [49, 54, 149]
]
PAL_MAX = 2048
def interpolate_int(a, b, flt):
    return int(a + (b - a) * flt)
def interpolated_color(val):
    flt = (val / PAL_MAX) * (len(PAL) - 1)
    idx = int(flt)
    flt = flt - idx
    a = PAL[idx]
    b = PAL[idx + 1]
    return [
        interpolate_int(a[0], b[0], flt),
        interpolate_int(a[1], b[1], flt),
        interpolate_int(a[2], b[2], flt)
    ]

mutex = Lock()

shared_array_base = Array(ctypes.c_uint16, 640 * 480)
shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
shared_array = shared_array.reshape(480, 640)
data_arr = shared_array

def compute_thread():
    data = None
    while True:
        with mutex:
            data = data_arr.copy()
        show_depth_image(data)

f = ftclient()

SQUARE_DIM = 10
def down_sample(image):
    shape = image.shape
    ft_shape = [35, 45]
    filter_h = (shape[0]//ft_shape[0])
    filter_w = (shape[1]// ft_shape[1])
    down_sampled = np.zeros(ft_shape)
    for h in range(ft_shape[0]):
        for w in range(ft_shape[1]):
            vert_start = h * filter_h
            vert_end = vert_start + filter_h
            horiz_start = w * filter_w
            horiz_end = horiz_start + filter_w
            img_slice = image[vert_start:vert_end, horiz_start:horiz_end]
            condition = img_slice != 2047
            img_slice = np.extract(condition, img_slice)
            mean = np.mean(img_slice) if len(img_slice) else 0
            down_sampled[h][w] = mean
    return down_sampled

def show_depth_image(depth_array):
    down_sampled = down_sample(depth_array)
    for col in range(45):
        for row in range(35):
            f.set(col, row, interpolated_color(down_sampled[row][col]))
    f.show()

def display_depth(dev, data, timestamp):
    del dev, timestamp
    arr = data.copy()
    with mutex:
        data_arr[:] = arr

t = Process(target=compute_thread, args=())
t.start()

freenect.runloop(depth=display_depth)
