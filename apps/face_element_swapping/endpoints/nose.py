from .helpers import point_dividing_a_line_segment, point_along_a_line_distanced_from_another_point
from .settings import SETTINGS_OF_THE_ENDPOINTS
from .types_of_face_part_endpoints import FourEndpointsOfANose, SixEndpointsOfANose


class GetEndpointsOfANose:

    @staticmethod
    def get_bottom_left_and_bottom_right_endpoints(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the bottom left endpoint and the bottom right endpoint
        :rtype: tuple - (), ((x,y), (x,y))
        """

        left_point_of_the_bottom_straight = point_dividing_a_line_segment(A=face_landmarks["nose_tip"][
            SETTINGS_OF_THE_ENDPOINTS["nose"]["INDEX_OF_THE_LEFTMOST_LANDMARK_OF_NOSE_TIP"]],
                                                                          B=face_landmarks["top_lip"][
                                                                              SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                                  "INDEX_OF_THE_LEFTMOST_LANDMARK_OF_TOP_LIP"]],
                                                                          offset_from_A=
                                                                          SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                              "PERCENT_OF_THE_DISTANCE_BETWEEN_THE_LEFTMOST_LANDMARK_OF_NOSE_TIP_AND_THE_LEFTMOST_LANDMARK_OF_TOP_LIP"])

        right_point_of_the_bottom_straight = point_dividing_a_line_segment(A=face_landmarks["nose_tip"][
            SETTINGS_OF_THE_ENDPOINTS["nose"]["INDEX_OF_THE_RIGHTMOST_LANDMARK_OF_NOSE_TIP"]],
                                                                           B=face_landmarks["top_lip"][
                                                                               SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                                   "INDEX_OF_THE_RIGHTMOST_LANDMARK_OF_THE_TOP_LIP"]],
                                                                           offset_from_A=
                                                                           SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                               "PERCENT_OF_THE_DISTANCE_BETWEEN_THE_RIGHTMOST_LANDMARK_OF_NOSE_TIP_AND_THE_RIGHTMOST_LANDMARK_OF_TOP_LIP"])

        bottom_left_endpoint = point_along_a_line_distanced_from_another_point(A=left_point_of_the_bottom_straight,
                                                                               B=right_point_of_the_bottom_straight,
                                                                               offset_from_A=
                                                                               SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                                   "OFFSET_FROM_THE_LINE_BETWEEN_NOSE_AND_LIPS"])

        bottom_right_endpoint = point_along_a_line_distanced_from_another_point(A=right_point_of_the_bottom_straight,
                                                                                B=left_point_of_the_bottom_straight,
                                                                                offset_from_A=
                                                                                SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                                    "OFFSET_FROM_THE_LINE_BETWEEN_NOSE_AND_LIPS"])
        return bottom_left_endpoint, bottom_right_endpoint

    @staticmethod
    def get_eyebrows_endpoints(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the rightmost landmark of left eyebrow and the leftmost landmark of right eyebrow
        :rtype: tuple - (), ((x,y), (x,y))
        """
        the_rightmost_landmark_of_left_eyebrow = face_landmarks["left_eyebrow"][
            SETTINGS_OF_THE_ENDPOINTS["nose"]["INDEX_OF_THE_RIGHTMOST_LANDMARK_OF_LEFT_EYEBROW"]]
        the_leftmost_landmark_of_right_eyebrow = face_landmarks["right_eyebrow"][
            SETTINGS_OF_THE_ENDPOINTS["nose"]["INDEX_OF_THE_LEFTMOST_LANDMARK_OF_RIGHT_EYEBROW"]]

        return the_rightmost_landmark_of_left_eyebrow, the_leftmost_landmark_of_right_eyebrow

    @staticmethod
    def get_four_endpoints(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: four points which a particular nose is contained between
        :rtype:  kind of 'namedtuple' (from module named 'collections', https://docs.python.org/3/library/collections.html#collections.namedtuple)
        with the following fields: 'bottom_left_endpoint', 'bottom_right_endpoint', 'top_right_endpoint', 'top_left_endpoint'
        """

        the_rightmost_landmark_of_left_eyebrow, the_leftmost_landmark_of_right_eyebrow = GetEndpointsOfANose.get_eyebrows_endpoints(
            face_landmarks=face_landmarks)
        bottom_left_endpoint, bottom_right_endpoint = GetEndpointsOfANose.get_bottom_left_and_bottom_right_endpoints(
            face_landmarks=face_landmarks)

        top_left_endpoint = point_along_a_line_distanced_from_another_point(A=the_rightmost_landmark_of_left_eyebrow,
                                                                            B=bottom_left_endpoint,
                                                                            offset_from_A=
                                                                            SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                                "OFFSET_FROM_EYEBROWS"])
        top_right_endpoint = point_along_a_line_distanced_from_another_point(A=the_leftmost_landmark_of_right_eyebrow,
                                                                             B=bottom_right_endpoint,
                                                                             offset_from_A=
                                                                             SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                                 "OFFSET_FROM_EYEBROWS"])

        return FourEndpointsOfANose(bottom_left_endpoint=bottom_left_endpoint,
                                    bottom_right_endpoint=bottom_right_endpoint,
                                    top_right_endpoint=top_right_endpoint,
                                    top_left_endpoint=top_left_endpoint)

    @staticmethod
    def get_middle_left_and_middle_right_endpoints(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: coordinates of the middle left endpoint and the middle right endpoint
        :rtype: tuple - (), ((x,y), (x,y))
        """

        the_rightmost_landmark_of_left_eye = face_landmarks["left_eye"][
            SETTINGS_OF_THE_ENDPOINTS["nose"]["INDEX_OF_THE_RIGHTMOST_LANDMARK_OF_LEFT_EYE"]]
        the_leftmost_landmark_of_right_eye = face_landmarks["right_eye"][
            SETTINGS_OF_THE_ENDPOINTS["nose"]["INDEX_OF_THE_LEFTMOST_LANDMARK_OF_RIGHT_EYE"]]

        middle_left_endpoint = point_dividing_a_line_segment(A=the_rightmost_landmark_of_left_eye,
                                                             B=the_leftmost_landmark_of_right_eye,
                                                             offset_from_A=SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                 "OFFSET_FROM_THE_ENDPOINTS_OF_EYES"])
        middle_right_endpoint = point_dividing_a_line_segment(A=the_leftmost_landmark_of_right_eye,
                                                              B=the_rightmost_landmark_of_left_eye,
                                                              offset_from_A=SETTINGS_OF_THE_ENDPOINTS["nose"][
                                                                  "OFFSET_FROM_THE_ENDPOINTS_OF_EYES"])
        return middle_left_endpoint, middle_right_endpoint

    @staticmethod
    def get_six_endpoints(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return: six points which a particular nose is contained between
        :rtype:  kind of 'namedtuple' (from module named 'collections', https://docs.python.org/3/library/collections.html#collections.namedtuple)
        with the following fields: 'bottom_left_endpoint', 'bottom_right_endpoint', 'middle_right_endpoint', 'top_right_endpoint', 'top_left_endpoint', 'middle_left_endpoint'
        """
        bottom_left_endpoint, bottom_right_endpoint = GetEndpointsOfANose.get_bottom_left_and_bottom_right_endpoints(
            face_landmarks=face_landmarks)
        middle_left_endpoint, middle_right_endpoint = GetEndpointsOfANose.get_middle_left_and_middle_right_endpoints(
            face_landmarks=face_landmarks)
        top_left_endpoint, top_right_endpoint = GetEndpointsOfANose.get_eyebrows_endpoints(
            face_landmarks=face_landmarks)

        return SixEndpointsOfANose(bottom_left_endpoint=bottom_left_endpoint,
                                   bottom_right_endpoint=bottom_right_endpoint,
                                   middle_right_endpoint=middle_right_endpoint,
                                   top_right_endpoint=top_right_endpoint,
                                   top_left_endpoint=top_left_endpoint,
                                   middle_left_endpoint=middle_left_endpoint)

    @staticmethod
    def get_endpoints_of_a_nose(face_landmarks, six_endpoints_mode=True):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :param six_endpoints_mode: params indicates if the object representing more endpoints describing the nose should be also returned
        :type six_endpoints_mode: bool (True or False)
        :return: endpoints which nose is contained between
        :rtype: dictionary - {} with the key "four_endpoints" and optionally "six_endpoints"
        """
        nose_endpoints = {
            "four_endpoints": GetEndpointsOfANose.get_four_endpoints(face_landmarks=face_landmarks)
        }
        if six_endpoints_mode:
            nose_endpoints["six_endpoints"] = GetEndpointsOfANose.get_six_endpoints(face_landmarks=face_landmarks)

        return nose_endpoints


get_nose_endpoints = GetEndpointsOfANose.get_endpoints_of_a_nose
