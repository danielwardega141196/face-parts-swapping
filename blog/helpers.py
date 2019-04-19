import json
from base64 import b64encode, b64decode
from io import BytesIO

import numpy as np
from PIL import Image

from blog import settings


def convert_img_to_base64(img):
    """
    :param img: an image as a PIL object or a numpy array
    :type img: PIL.Image.Image (https://pillow.readthedocs.io/en/3.1.x/reference/Image.html) or
    numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :return: image converted to base64. The image has a special prefix - settings.BASE64_PREFIX.
    :rtype: string - str
    """
    if isinstance(img, np.ndarray):
        img = Image.fromarray(img)

    buffer = BytesIO()
    img.save(buffer, format=settings.FORMAT_OF_TMP_IMG_TO_CONVERT)
    image_in_base64_without_prefix = buffer.getvalue()
    image_in_base64_without_prefix = b64encode(image_in_base64_without_prefix).decode()
    image_in_base64_with_prefix = settings.BASE64_PREFIX + image_in_base64_without_prefix
    return image_in_base64_with_prefix


def remove_prefix_from_base64(base64_with_prefix):
    """
    :param base64_with_prefix: base64-encoded image which has a special prefix.
    The last character of this prefix is ','.
    Here are some examples of the prefixes: 'data:image/png;base64,' , 'data:image/gif;base64,' , 'data:image/jpeg;base64,'
    :type base64_with_prefix: string
    :return base64-encoded image without the prefix
    :rtype string - str
    """
    return base64_with_prefix.split(',')[1]


def replace_special_signs(file_name):
    """
    This function replaces special signs (keys of settings.SPECIAL_SIGNS_IN_FILE_NAMES)
    included in 'file_name' with their equivalents (values of settings.SPECIAL_SIGNS_IN_FILE_NAMES)
    :param file_name: name of a file
    :type file_name: string - str
    :return: file_name in which special signs was replaced by others
    :rtype: string - str
    """
    for key, value in settings.SPECIAL_SIGNS_IN_FILE_NAMES.items():
        file_name = file_name.replace(key, value)
    return file_name


def set_mode_of_pil(pil,
                    mode=settings.DEFAULT_PIL_MODE):
    """
    This function sets the mode of PIL object and returns this object.
    :param pil: PIL object representing the image
    :type pil: PIL.*
    :param mode: this param defines the type and depth of a pixel in the image
    https://pillow.readthedocs.io/en/4.1.x/handbook/concepts.html#modes
    :type mode: string - str
    :return: PIL object('pil') with the appropriate mode which was set
    :rtype: PIL.Image.Image (https://pillow.readthedocs.io/en/3.1.x/reference/Image.html)
    """
    pil = pil.convert(mode)
    return pil


def convert_base64_to_pil(image_in_base64):
    """
    :param image_in_base64: an image converted to base64
    :type image_in_base64: string - str
    :return: PIL object representing the image
    :rtype: PIL.*
    """
    decoded_base64 = b64decode(image_in_base64)
    pil = Image.open(BytesIO(decoded_base64))
    return pil


def convert_rgb_array_to_text(rgb_array):
    """
    This function converts a numpy array to a (nested) Python list
    and then converts the list to a string by using the function named 'dumps' from the 'json' module.
    https://docs.python.org/3/library/json.html#json.dumps
    :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
    :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :return: a (nested) Python list, which previously was a numpy array, converted to a string
    :rtype: string - str
    """
    return json.dumps(rgb_array.tolist())


def convert_text_to_rgb_array(text, np_dtype=np.uint8):
    """
    This function has the opposite effect to the 'convert_rgb_array_to_text' function.
    It converts a string, which was made by the function named 'dumps' from the 'json' module, to
    a (nested) Python list. Then this Python list is converted to a numpy array which has a specified dtype ('np_dtype').
    :param text: a (nested) Python list, which previously was a numpy array, converted to a string
    :type text: string - str
    :param np_dtype: numpy type (https://www.numpy.org/devdocs/user/basics.types.html)
    :return: a numpy array which has a specified dtype ('np_dtype')
    :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    """
    return np.asanyarray(json.loads(text), dtype=np_dtype)


def convert_pil_to_np_array(pil, np_dtype=np.uint8):
    """
    This function converts PIL object to a numpy array which has a specified dtype ('np_dtype').
    :param pil: PIL object representing the image
    :type pil: PIL.*
    :param np_dtype: numpy type (https://www.numpy.org/devdocs/user/basics.types.html)
    :return: a numpy array which has a specified dtype ('np_dtype')
    :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    """
    return np.array(pil, dtype=np_dtype)
