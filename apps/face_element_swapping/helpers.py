from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def get_rectangle_in_an_image(np_array, bounding_rectangle_of_polygon):
    """
    :param np_array: a numpy array
    :type np_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :param bounding_rectangle_of_polygon: tuple or list with coordinates of the start point of the rectangle
    and the width and height of this rectangle - (x, y, width, height) or [x, y, width, height]
    :type bounding_rectangle_of_polygon: tuple - () or list - (). The tuple or list should have four elements.
    :return: the part of 'np_array' indicated by 'bounding_rectangle_of_polygon'
    :rtype numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    """
    return np_array[
        bounding_rectangle_of_polygon[1] : bounding_rectangle_of_polygon[1]
        + bounding_rectangle_of_polygon[3],
        bounding_rectangle_of_polygon[0] : bounding_rectangle_of_polygon[0]
        + bounding_rectangle_of_polygon[2],
    ]


def fill_pixel_if_belongs_to_polygon(
    rgb_array, polygon, row_idx, column_idx, pixel_value
):
    """
    This function checks if point: (column_idx, row_idx) belongs to the passed polygon('polygon').
    If so the value of 'rgb_array[row_idx][column_idx]' will be set to 'pixel_value'.
    :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
    :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :param polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
    All elements in list (or tuple) should represent a polygon.
    :type polygon: list - [] or tuple - ()
    :param row_idx: row index of 'rgb_array'
    :type row_idx: integer - int
    :param column_idx: column index of 'rgb_array'
    :type column_idx: integer - int
    :param pixel_value: RGB value for the pixel
    :type pixel_value: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    The array must have following shape: (3,)
    """
    polygon = Polygon(polygon)
    point = Point(column_idx, row_idx)
    if polygon.contains(point):
        rgb_array[row_idx][column_idx] = pixel_value
