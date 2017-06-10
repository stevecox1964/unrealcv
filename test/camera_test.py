'''
Verify whether the camera system can respond to commands correctly.
These tests can not verify whether the results are generated correctly, since we need nothing about the correct answer. The correctness test will be done in an environment specific test. such as in `rr_test.py`.

Every test function starts with prefix `test_`, so that pytest can automatically discover these functions during execution.
'''
from unrealcv import client
from conftest import env, checker
import cv2
from StringIO import StringIO
import numpy as np
from PIL import Image


def imread_png(res):
    PILimg = Image.open(StringIO(res))
    img = np.array(PILimg)
    return img

def imread_npy(res):
    return np.load(StringIO(res))

def imread_file(res):
    return cv2.imread(res)

def test_camera_control(env):
    client.connect()
    cmds = [
        'vget /camera/0/location',
        'vget /camera/0/rotation',
        # 'vset /camera/0/location 0 0 0', # BUG: If moved out the game bounary, the pawn will be deleted, so that the server code will crash with a nullptr error.
        # 'vset /camera/0/rotation 0 0 0',
    ]
    for cmd in cmds:
        res = client.request(cmd)
        assert checker.not_error(res)

def test_png_mode(env):
    '''
    Get image as a png binary, make sure no exception happened
    '''
    client.connect()
    cmds = [
        'vget /camera/0/lit png',
        'vget /camera/0/object_mask png',
        'vget /camera/0/normal png',
    ]
    for cmd in cmds:
        res = client.request(cmd)
        assert checker.not_error(res)
        im = imread_png(res)

def test_npy_mode(env):
    '''
    Get data as a numpy array
    '''
    client.connect()
    cmd = 'vget /camera/0/depth npy'
    res = client.request(cmd)
    assert checker.not_error(res)

    # Do these but without assert, if exception happened, this test failed
    arr = imread_npy(res)

def test_file_mode(env):
    '''
    Save data to disk as image file
    '''
    client.connect()
    cmds = [
        'vget /camera/0/lit test.png',
        'vget /camera/0/object_mask test.png',
        'vget /camera/0/normal test.png',
        'vget /camera/0/depth test.png',
        'vget /camera/0/depth test.exr', # This is very likely to fail in Linux
    ]
    for cmd in cmds:
        res = client.request(cmd)
        assert checker.not_error(res)

        im = imread_file(res)



if __name__ == '__main__':
    test_binary_mode(None)
    # test_file_mode(None)
