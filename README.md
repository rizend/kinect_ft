install cmake, libusb, python, numpy, python-dev, cython on your platform of choice

optional: opencv (w/ py wrappers), Matplotlib


    git clone https://github.com/OpenKinect/libfreenect && cd libfreenect
    mkdir build && cd build
    cmake .. -DBUILD_PYTHON=ON
    make
    sudo make install
    sudo cp ../platform/linux/udev/51-kinect.rules /etc/udev/rules.d/
    sudo sh -c 'udevadm control --reload-rules && udevadm trigger'

On linux if python can't find the `freenect` package after installation:

    export LD_LIBRARY_PATH="/usr/local/lib"
    export PYTHONPATH="/usr/local/lib/python3.6/site-packages/"

