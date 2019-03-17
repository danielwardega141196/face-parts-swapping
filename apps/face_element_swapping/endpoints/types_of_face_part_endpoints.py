from collections import namedtuple

PointsToAdjustNoses = namedtuple('PointsToAdjustNoses',
                                 ["bottom_left_corner",
                                  "bottom_right_corner",
                                  "top_right_corner",
                                  "top_left_corner"])

CutFieldOfNoses = namedtuple("CutFieldOfNoses",
                             ["bottom_left_corner",
                              "bottom_right_corner",
                              "middle_right_point",
                              "top_right_corner",
                              "top_left_corner",
                              "middle_left_point"])

EndpointsOfLips = namedtuple("EndpointsOfLips",
                              ["left_endpoint",
                               "top_endpoint",
                               "right_endpoint",
                               "bottom_endpoint"])
