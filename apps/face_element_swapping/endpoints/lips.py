from .helpers import point_dividing_a_line_segment, \
    find_endpoint, \
    point_along_a_line_distanced_from_another_point
from .settings import SETTINGS_OF_THE_ENDPOINTS
from .types_of_face_part_endpoints import EndpointsOfLips


class GetEndpointsOfLips:

    @staticmethod
    def get_top_endpoint_of_lips(face_landmarks):

        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the top endpoint of lips
        :rtype: list - [] or tuple - ()
        """

        the_lowest_landmark_of_nose_tip = face_landmarks["nose_tip"][
            SETTINGS_OF_THE_ENDPOINTS["lips"]["INDEX_OF_THE_LOWEST_LANDMARK_OF_NOSE_TIP"]]

        the_highest_landmark_of_top_lip = face_landmarks["top_lip"][
            SETTINGS_OF_THE_ENDPOINTS["lips"]["INDEX_OF_THE_HIGHEST_LANDMARK_OF_TOP_LIP"]]

        top_endpoint_of_lips = point_dividing_a_line_segment(A=the_lowest_landmark_of_nose_tip,
                                                             B=the_highest_landmark_of_top_lip,
                                                             offset_from_A=SETTINGS_OF_THE_ENDPOINTS["lips"][
                                                                 "PERCENT_OF_THE_DISTANCE_BETWEEN_THE_LOWEST_LANDMARK_OF_NOSE_TIP_AND_THE_HIGHEST_LANDMARK_OF_TOP_LIP"])
        return top_endpoint_of_lips

    @staticmethod
    def get_bottom_endpoint_of_lips(face_landmarks):

        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the bottom endpoint of lips
        :rtype: list - [] or tuple - ()
        """

        the_lowest_landmark_of_chin = face_landmarks["chin"][
            SETTINGS_OF_THE_ENDPOINTS["lips"]["INDEX_OF_THE_LOWEST_LANDMARK_OF_CHIN"]]

        the_lowest_landmark_of_bottom_lip = face_landmarks["bottom_lip"][
            SETTINGS_OF_THE_ENDPOINTS["lips"]["INDEX_OF_THE_LOWEST_LANDMARK_OF_BOTTOM_LIP"]]

        bottom_endpoint_of_lips = point_dividing_a_line_segment(A=the_lowest_landmark_of_bottom_lip,
                                                                B=the_lowest_landmark_of_chin,
                                                                offset_from_A=SETTINGS_OF_THE_ENDPOINTS["lips"][
                                                                    "PERCENT_OF_THE_DISTANCE_BETWEEN_THE_LOWEST_LANDMARK_OF_CHIN_AND_THE_LOWEST_LANDMARK_OF_BOTTOM_LIP"])
        return bottom_endpoint_of_lips

    @staticmethod
    def get_the_leftmost_and_the_rightmost_points_of_lips(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: the leftmost point of lips and the rightmost point of lips
        :rtype: tuple - ()
        """

        both_lips = face_landmarks["top_lip"] + face_landmarks["bottom_lip"]

        # Of all the points regarding lips we choose the leftmost point.
        the_leftmost_point_of_lips = find_endpoint(list_of_coordinates=both_lips,
                                                   mode="LEFT")
        # Of all the points regarding lips we choose the rightmost point.
        the_rightmost_point_of_lips = find_endpoint(list_of_coordinates=both_lips,
                                                    mode="RIGHT")

        return the_leftmost_point_of_lips, the_rightmost_point_of_lips


    @staticmethod
    def get_left_endpoint_of_lips(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the left endpoint of lips
        :rtype: list - [] or tuple - ()
        """
        the_leftmost_point_of_lips, the_rightmost_point_of_lips = GetEndpointsOfLips.get_the_leftmost_and_the_rightmost_points_of_lips(face_landmarks=face_landmarks)
        left_endpoint_of_lips = point_along_a_line_distanced_from_another_point(A=the_leftmost_point_of_lips,
                                                                                B=the_rightmost_point_of_lips,
                                                                                offset_from_A=
                                                                                SETTINGS_OF_THE_ENDPOINTS["lips"][
                                                                                    "OFFSET_FROM_THE_LEFTMOST_POINT_AND_RIGHTMOST_POINT_OF_LIPS"])
        return left_endpoint_of_lips

    @staticmethod
    def get_right_endpoint_of_lips(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the right endpoint of lips
        :rtype: list - [] or tuple - ()
        """

        the_leftmost_point_of_lips, the_rightmost_point_of_lips = GetEndpointsOfLips.get_the_leftmost_and_the_rightmost_points_of_lips(face_landmarks=face_landmarks)
        right_endpoint_of_lips = point_along_a_line_distanced_from_another_point(A=the_rightmost_point_of_lips,
                                                                                 B=the_leftmost_point_of_lips,
                                                                                 offset_from_A=
                                                                                 SETTINGS_OF_THE_ENDPOINTS["lips"][
                                                                                     "OFFSET_FROM_THE_LEFTMOST_POINT_AND_RIGHTMOST_POINT_OF_LIPS"])

        return right_endpoint_of_lips

    @staticmethod
    def get_endpoints_of_lips(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: points which lips are contained between
        :rtype:  kind of 'namedtuple' (from module named 'collections', https://docs.python.org/3/library/collections.html#collections.namedtuple)
        with the following fields: 'left_endpoint', 'top_endpoint', 'right_endpoint', 'bottom_endpoint'
        """

        left_endpoint_of_lips = EndpointsOfLips.get_left_endpoint_of_lips(face_landmarks=face_landmarks)
        top_endpoint_of_lips = EndpointsOfLips.get_top_endpoint_of_lips(face_landmarks=face_landmarks)
        right_endpoint_of_lips = EndpointsOfLips.get_right_endpoint_of_lips(face_landmarks=face_landmarks)
        bottom_endpoint_of_lips = EndpointsOfLips.get_bottom_endpoint_of_lips(face_landmarks=face_landmarks)

        return EndpointsOfLips(left_endpoint=left_endpoint_of_lips,
                               top_endpoint=top_endpoint_of_lips,
                               right_endpoint=right_endpoint_of_lips,
                               bottom_endpoint=bottom_endpoint_of_lips)
