from collections import namedtuple

FourEndpointsOfANose = namedtuple("FourEndpointsOfANose",
                                 ["bottom_left_endpoint",
                                  "bottom_right_endpoint",
                                  "top_right_endpoint",
                                  "top_left_endpoint"])

SixEndpointsOfANose = namedtuple("SixEndpointsOfANose",
                                ["bottom_left_endpoint",
                                 "bottom_right_endpoint",
                                 "middle_right_endpoint",
                                 "top_right_endpoint",
                                 "top_left_endpoint",
                                 "middle_left_endpoint"])

EndpointsOfLips = namedtuple("EndpointsOfLips",
                              ["left_endpoint",
                               "top_endpoint",
                               "right_endpoint",
                               "bottom_endpoint"])
