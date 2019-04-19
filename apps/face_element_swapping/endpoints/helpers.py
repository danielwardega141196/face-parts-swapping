from face_recognition import face_landmarks

from .settings import TYPES_OF_ENDPOINTS


def point_dividing_a_line_segment(A, B, offset_from_A):
    """
    :param A: coordinates of the start point of a line in 2D Space ([x, y] or (x, y))
    :type A: list - [] or tuple - ()
    :param B: coordinates of the end point of a line in 2D Space ([x, y] or (x, y))
    :type B: list - [] or tuple - ()
    :param offset_from_A: percent of the Euclidean distance between A and B where 0 % is equal to 0 and 100% is equal to 1.
    :type offset_from_A: float
    :return: coordinates of point along a line from A to B.
    The point is located between points A and B
    and is away from point A by the length equal to : (Euclidean distance between A and B) * offset_from_A
    A--C------B
    :rtype tuple - ()
    """

    x = (1 - offset_from_A) * A[0] + offset_from_A * B[0]
    y = (1 - offset_from_A) * A[1] + offset_from_A * B[1]

    return int(round(x)), int(round(y))


def find_endpoint(coordinates,
                  mode="TOP"):

    """
    :param coordinates: list of tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...))
    :type coordinates: list - [] or tuple - ()
    :param mode: this parameter indicates which endpoint we look for.
    Allowed values of this parameter:
        "LEFT" :  we look for the point with the minimum 'x' value
        "RIGHT": we look for the point with the maximum 'x' value
        "BOTTOM": we look for the point with the minimum 'y' value
        "TOP": we look for the point with the maximum 'y' value
    :type mode: string
    :return coordinates of the wanted endpoint
    :rtype list - [] or tuple - ()
    """
    endpoint_settings = TYPES_OF_ENDPOINTS.get(mode, TYPES_OF_ENDPOINTS["TOP"])
    index_of_a_coordinate = endpoint_settings["INDEX_OF_A_COORDINATE"]
    comparison_operator = endpoint_settings["COMPARSION_OPERATOR"]

    wanted_point = coordinates[0]
    for idx in range(1, len(coordinates)):
        if comparison_operator(coordinates[idx][index_of_a_coordinate], wanted_point[index_of_a_coordinate]):
            wanted_point = coordinates[idx]
    return wanted_point


def get_point_relative_to_another_point(endpoint, midpoint):
    """
    :param endpoint: coordinates of the start point of a line in 2D Space ([x, y] or (x, y))
    :type endpoint: list - [] or tuple - ()
    :param midpoint: coordinates of the midpoint of a line in 2D Space ([x, y] or (x, y))
    :type midpoint: list - [] or tuple - ()
    :return coordinates of the end point of a line in 2D Space ([x, y] or (x, y))
    :rtype tuple - ()
    """
    return (2 * midpoint[0] - endpoint[0],
            2 * midpoint[1] - endpoint[1])


def point_along_a_line_distanced_from_another_point(A, B, offset_from_A):
    """
    :param A: coordinates of a point of the straight in 2D Space ([x, y] or (x, y))
    :type A: list - [] or tuple - ()
    :param B: coordinates of an another point of the straight in 2D Space ([x, y] or (x, y))
    :type B: list - [] or tuple - ()
    :param offset_from_A: percent of the Euclidean distance between A and B where 0 % is equal to 0 and 100% is equal to 1.
    :type offset_from_A: float
    :return coordinates of the point on same straight.
    The point is located next to point A and is away from it by the length equal to : (Euclidean distance between A and B) * offset_from_A
    C--A------B
    :rtype tuple - ()
    """
    point_inside_a_line = point_dividing_a_line_segment(A=A,
                                                        B=B,
                                                        offset_from_A=offset_from_A)

    point_outside_a_line = get_point_relative_to_another_point(endpoint=point_inside_a_line,
                                                               midpoint=A)
    return point_outside_a_line



def get_faces_landmarks(rgb_array):
    """
    :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
    :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
    :return: a list of dictionaries of face feature locations (eyes, nose, etc)
    :rtype list - []
    """
    face_landmarks_list = face_landmarks(rgb_array)
    return face_landmarks_list
