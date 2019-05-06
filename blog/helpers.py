import json
from base64 import b64encode, b64decode
from io import BytesIO

import numpy as np
from PIL import Image

from .settings import DEFAULT_PIL_MODE, \
    PIL_MODE_OF_TRANSPARENT_PHOTOS, \
    FILE_EXTENSIONS_ACCORDING_TO_PIL_MODES, \
    BASE64_PREFIXES_ACCORDING_TO_FILE_EXTENSIONS, \
    SPECIAL_SIGNS_IN_FILE_NAMES, \
    MAXIMUM_NUMBER_OF_PIXELS, \
    MAXIMUM_SIDE_LENGTH, \
    DEFAULT_RESIZING_FILTER


def convert_img_to_base64(img):
    """
    :param img: an image as a PIL object or a numpy array
    :type img: PIL.Image.Image (https://pillow.readthedocs.io/en/3.1.x/reference/Image.html) or
    numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :return: the passed image converted to base64.
    The image has a special prefix suitable for its extension.
    The prefixes are contained in the dictionary 'BASE64_PREFIXES_ACCORDING_TO_FILE_EXTENSIONS'
    (in the file '.settings'.)
    :rtype: string - str
    """
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img.astype(np.uint8))

    if img.mode != DEFAULT_PIL_MODE:
        img = set_mode_of_pil(pil=img, mode=PIL_MODE_OF_TRANSPARENT_PHOTOS)

    buffer = BytesIO()
    tmp_file_extension = FILE_EXTENSIONS_ACCORDING_TO_PIL_MODES[img.mode]
    img.save(buffer, format=tmp_file_extension)
    image_in_base64_without_prefix = buffer.getvalue()
    image_in_base64_without_prefix = b64encode(image_in_base64_without_prefix).decode()

    image_in_base64_with_prefix = BASE64_PREFIXES_ACCORDING_TO_FILE_EXTENSIONS[
                                      tmp_file_extension] + image_in_base64_without_prefix
    return image_in_base64_with_prefix


def remove_prefix_from_base64(base64_with_prefix):
    """
    :param base64_with_prefix: base64-encoded image which has a special prefix.
    The last character of this prefix is ','.
    Here are some examples of the prefixes: 'data:image/png;base64,',
                                            'data:image/gif;base64,',
                                            'data:image/jpeg;base64,'
    :type base64_with_prefix: string
    :return base64-encoded image without the prefix
    :rtype string - str
    """
    return base64_with_prefix.split(',')[1]


def replace_special_signs(file_name):
    """
    This function replaces special signs (keys of the SPECIAL_SIGNS_IN_FILE_NAMES dictionary)
    included in 'file_name' with their equivalents (values of the SPECIAL_SIGNS_IN_FILE_NAMES dictionary).
    :param file_name: name of a file
    :type file_name: string - str
    :return: file_name in which special signs was replaced by others
    :rtype: string - str
    """
    for key, value in SPECIAL_SIGNS_IN_FILE_NAMES.items():
        file_name = file_name.replace(key, value)
    return file_name


def set_mode_of_pil(pil, mode):
    """
    This function sets the mode of the PIL object('pil') and returns this object.
    :param pil: PIL object representing an image
    :type pil: PIL.*
    :param mode: this param defines the type and depth of a pixel in the image
    (https://pillow.readthedocs.io/en/4.1.x/handbook/concepts.html#modes)
    :type mode: string - str
    :return: PIL object('pil') with the appropriate mode
    :rtype: PIL.Image.Image (https://pillow.readthedocs.io/en/3.1.x/reference/Image.html)
    """
    pil = pil.convert(mode)
    return pil


def convert_base64_to_pil(photo_in_base64):
    """
    This function converts the base64-encoded image to a PIL object.
    :param photo_in_base64: an image converted to base64.
    The string doesn't have any prefix.
    :type photo_in_base64: string - str
    :return: PIL object representing the image
    :rtype: PIL.*
    """
    decoded_base64 = b64decode(photo_in_base64)
    pil = Image.open(BytesIO(decoded_base64))
    return pil


def convert_rgb_array_to_text(rgb_array):
    """
    This function converts a numpy array to a (nested) Python list
    and then converts the list to a string by using the function named 'dumps' from the 'json' module.
    (https://docs.python.org/3/library/json.html#json.dumps).
    :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
    :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :return: a (nested) Python list, which previously was a numpy array, converted to a string
    :rtype: string - str
    """
    return json.dumps(rgb_array.tolist())


def convert_text_to_rgb_array(text, np_dtype=np.uint8):
    """
    This function has the opposite effect to the 'convert_rgb_array_to_text' function (also included in this file).
    It converts a string, which was made by the function named 'dumps' from the 'json' module, to
    a (nested) Python list. Then this Python list is converted to a numpy array which has a specific dtype('np_dtype').
    :param text: a (nested) Python list, which previously was a numpy array, converted to a string
    :type text: string - str
    :param np_dtype: numpy type (https://www.numpy.org/devdocs/user/basics.types.html)
    :return: a numpy array which has a specific dtype ('np_dtype')
    :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    """
    return np.asanyarray(json.loads(text), dtype=np_dtype)


def convert_pil_to_np_array(pil, np_dtype=np.uint8):
    """
    This function converts the PIL object('pil') to a numpy array which has a specific dtype('np_dtype').
    :param pil: PIL object representing an image
    :type pil: PIL.*
    :param np_dtype: numpy type (https://www.numpy.org/devdocs/user/basics.types.html)
    :return: a numpy array which has a specific dtype('np_dtype')
    :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    """
    return np.array(pil, dtype=np_dtype)


def correct_size(img,
                 maximum_number_of_pixels=MAXIMUM_NUMBER_OF_PIXELS):
    """
    This function checks if the number of pixels
    in the passed image ('img') is is less or equal
    to 'maximum_number_of_pixels' (passed as a parameter).
    :param img: PIL object representing an image
    :type img: PIL.*
    :param maximum_number_of_pixels: the maximum number of pixels
    the passed image ('img') can contain.
    :type maximum_number_of_pixels: integer - int
    :return: True if the number of pixels in the image
    is less or equal to 'maximum_number_of_pixels', false if not.
    :rtype: bool(True or False)
    """
    height, width = img.size
    return height * width <= maximum_number_of_pixels


def resize_img(img,
               maximum_side_length=MAXIMUM_SIDE_LENGTH,
               resizing_filter=DEFAULT_RESIZING_FILTER):
    """
    This function resizes the passed image keeping the aspect ratio.
    The longer side will have a length equal to 'maximum_side_length'
    (passed as a parameter).
    :param img: PIL object representing an image
    :type img: PIL.*
    :param maximum_side_length: the maximum side length
    the passed image ('img') can have.
    :type maximum_side_length: integer - int
    :param resizing_filter: an integer representing
    filter that will be used for resampling.
    :type resizing_filter: integer - int
    :return: PIL object representing the resized image
    :rtype: PIL.*
    """
    height, width = img.size
    if height > width:
        new_height = maximum_side_length
        new_width = int(maximum_side_length * (width / height))
    else:
        new_height = int(maximum_side_length * (height / width))
        new_width = maximum_side_length
    img = img.resize((new_height, new_width), resizing_filter)
    return img
