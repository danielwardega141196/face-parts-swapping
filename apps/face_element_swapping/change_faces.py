import cv2
import numpy as np
from shapely.geometry.polygon import Polygon
from .settings import DEFAULT_CLASSIFIER, \
    PERCENT_OF_NEAREST_NEIGHBOURS, \
    MASK_FILLING_COLOR
from math import ceil
from .helpers import fill_pixel_if_belongs_to_polygon, \
    get_rectangle_in_an_image

class ChangeFaceElement:

    @staticmethod
    def get_bounding_rectangle_of_polygon(polygon):
        """
        Function calculates the up-right bounding rectangle of a point set (polygon).
        Its effects are similar to function named 'boundingRect' from module 'cv2'.
        (https://docs.opencv.org/3.1.0/dd/d49/tutorial_py_contour_features.html)
        :param polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                        All elements in list (or tuple) should represent a polygon.
        :type polygon: list - [] or tuple - ()
        :return the tuple with coordinates of the start point of a rectangle
                and the width and height of this rectangle - (x, y, width, height)
        :rtype tuple - (). the tuple will have four elements
        """
        polygon_to_adjust = np.float32([polygon])
        bounding_rectangle_of_polygon = cv2.boundingRect(polygon_to_adjust)
        return bounding_rectangle_of_polygon


    @staticmethod
    def get_cropped_polygon(polygon, bounding_rectangle_of_polygon):
        """
        The function subtracts the 'x' value of the start point of the bounding rectangle (bounding_rectangle_of_polygon[0])
        from each 'x' value of points of the polygon.
        The function subtracts the 'y' value of the start point of the bounding rectangle (bounding_rectangle_of_polygon[1])
        from each 'y' value of points of the polygon.
        :param polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                        All elements in list (or tuple) should represent a polygon.
        :type polygon: list - [] or tuple - ()
        :param bounding_rectangle_of_polygon: the tuple with coordinates of the start point of the rectangle
               and the width and height of this rectangle - (x, y, width, height)
        :type bounding_rectangle_of_polygon: tuple - (). The tuple should have at least two elements
            (the coordinates of the start point of the bounding rectangle - (x, y))
        :return list of tuples
        :rtype list - []
        """
        cropped_polygon = [(point[0] - bounding_rectangle_of_polygon[0],
                            point[1] - bounding_rectangle_of_polygon[1]) for point in polygon]

        return cropped_polygon

    @staticmethod
    def get_warp_mats(src_polygon,
                      dst_polygon,
                      bounding_rectangle_of_src_polygon,
                      bounding_rectangle_of_dst_polygon):

        """
        :param src_polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                            All elements in list (or tuple) should represent a source polygon.
        :type src_polygon: list - [] or tuple - ()
        :param dst_polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                            All elements in list (or tuple) should represent a destination polygon.
        :type dst_polygon: list - [] or tuple - ()
        :param bounding_rectangle_of_src_polygon: the tuple with coordinates of the start point of the rectangle
               and the width and height of this rectangle - (x, y, width, height)
               This rectangle should contain the source polygon inside.
        :type bounding_rectangle_of_src_polygon: tuple - (). The tuple should have at least two elements
            (the coordinates of the start point of the bounding rectangle - (x, y))
        :param bounding_rectangle_of_dst_polygon: the tuple with coordinates of the start point of the rectangle
               and the width and height of this rectangle - (x, y, width, height)
               This rectangle should contain the destination polygon inside.
        :type bounding_rectangle_of_dst_polygon: tuple - (). The tuple should have at least two elements
            (the coordinates of the start point of the bounding rectangle - (x, y))
        :return 3 x 3 matrix of a perspective transform between the source polygon (src_polygon) and the destination polygon (dst_polygon).
        :rtype numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        cropped_src_polygon = ChangeFaceElement.get_cropped_polygon(polygon=src_polygon,
                                                                    bounding_rectangle_of_polygon=bounding_rectangle_of_src_polygon)
        cropped_dst_polygon = ChangeFaceElement.get_cropped_polygon(polygon=dst_polygon,
                                                                    bounding_rectangle_of_polygon=bounding_rectangle_of_dst_polygon)


        # By clicking the link below you can see
        # more information on the function 'getPerspectiveTransform' from module 'cv2'
        # https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#cv2.getPerspectiveTransform
        warp_mats = cv2.getPerspectiveTransform(np.float32(cropped_src_polygon),
                                                np.float32(cropped_dst_polygon))
        return warp_mats

    @staticmethod
    def blur_image_colors_via_classifier(classifier,
                                         image_to_blur,
                                         training_image,
                                         rectangle_of_image_to_blur,
                                         polygon_of_image_to_blur):

        # @Todo Add a documentation

        training_data = get_rectangle_in_an_image(matrix=training_image,
                                                  rectangle=rectangle_of_image_to_blur)

        shape_of_training_image = training_data.shape
        training_data = np.reshape(training_data, (shape_of_training_image[0] * shape_of_training_image[1],
                                                    shape_of_training_image[2]))
        training_data = np.unique(training_data, axis=0)
        normalized_training_data = (training_data - np.average(training_data, axis=0)) / np.std(training_data, axis=0)

        training_labels = range(training_data.shape[0])
        classifier = classifier(ceil(PERCENT_OF_NEAREST_NEIGHBOURS * training_data.shape[0]))
        classifier.fit(normalized_training_data, training_labels)

        data = get_rectangle_in_an_image(matrix=image_to_blur,
                                         rectangle=rectangle_of_image_to_blur)

        shape_of_data = data.shape
        data = np.reshape(data, (shape_of_data[0] * shape_of_data[1],
                                 shape_of_data[2]))
        data = (data - np.average(training_data, axis=0)) / np.std(training_data, axis=0)
        labels = classifier.kneighbors(data, return_distance=False)

        dst_polygon_object = Polygon(polygon_of_image_to_blur)
        label_idx = 0
        for row_idx in range(rectangle_of_image_to_blur[1],
                             rectangle_of_image_to_blur[1] + rectangle_of_image_to_blur[3]):

            for column_idx in range(rectangle_of_image_to_blur[0],
                                    rectangle_of_image_to_blur[0] + rectangle_of_image_to_blur[2]):

                pixel_value = np.round(np.average(training_data[labels[label_idx]], axis=0)).astype(np.uint8)
                fill_pixel_if_belongs_to_polygon(matrix=image_to_blur,
                                                 polygon=dst_polygon_object,
                                                 row_idx=row_idx,
                                                 column_idx=column_idx,
                                                 pixel_value=pixel_value)
                label_idx += 1

        return image_to_blur


    @staticmethod
    def fill_polygon_in_a_rectangle(dst_rgb_array,
                                    dst_polygon,
                                    cropped_dst_rgb_array,
                                    bounding_rectangle_of_dst_polygon):

        # @Todo Add a documentation

        dst_polygon_object = Polygon(dst_polygon)
        dst_rgb_array_copy = dst_rgb_array.copy()
        dst_mask = np.zeros_like(dst_rgb_array)

        cropped_dst_rgb_array_row_index = 0
        for row_idx in range(bounding_rectangle_of_dst_polygon[1],
                             bounding_rectangle_of_dst_polygon[1] + bounding_rectangle_of_dst_polygon[3]):
            cropped_dst_rgb_array_column_index = 0
            for column_idx in range(bounding_rectangle_of_dst_polygon[0],
                                    bounding_rectangle_of_dst_polygon[0] + bounding_rectangle_of_dst_polygon[2]):

                fill_pixel_if_belongs_to_polygon(matrix=dst_rgb_array_copy,
                                                 polygon=dst_polygon_object,
                                                 row_idx=row_idx,
                                                 column_idx=column_idx,
                                                 pixel_value=cropped_dst_rgb_array[cropped_dst_rgb_array_row_index][cropped_dst_rgb_array_column_index])

                fill_pixel_if_belongs_to_polygon(matrix=dst_mask,
                                                 polygon=dst_polygon_object,
                                                 row_idx=row_idx,
                                                 column_idx=column_idx,
                                                 pixel_value=MASK_FILLING_COLOR)
                cropped_dst_rgb_array_column_index += 1
            cropped_dst_rgb_array_row_index += 1

        center = ((2 * bounding_rectangle_of_dst_polygon[0] + bounding_rectangle_of_dst_polygon[2]) // 2,
                  (2 * bounding_rectangle_of_dst_polygon[1] + bounding_rectangle_of_dst_polygon[3]) // 2)

        mixed_image = cv2.seamlessClone(dst_rgb_array_copy,
                                        dst_rgb_array,
                                        dst_mask,
                                        center,
                                        cv2.NORMAL_CLONE)
        return mixed_image

    @staticmethod
    def changeFaceElement(src_rgb_array,
                          dst_rgb_array,
                          src_polygon,
                          dst_polygon,
                          dst_cut_field=None):

        # @Todo Add a documentation

        bounding_rectangle_of_src_polygon = ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=src_polygon)
        bounding_rectangle_of_dst_polygon = ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=dst_polygon)

        cropped_src_rgb_array = src_rgb_array[bounding_rectangle_of_src_polygon[1]:
                                              bounding_rectangle_of_src_polygon[1] + bounding_rectangle_of_src_polygon[3],
                                              bounding_rectangle_of_src_polygon[0]:
                                              bounding_rectangle_of_src_polygon[0] + bounding_rectangle_of_src_polygon[2]]

        warp_mats = ChangeFaceElement.get_warp_mats(src_polygon=src_polygon,
                                                    dst_polygon=dst_polygon,
                                                    bounding_rectangle_of_src_polygon=bounding_rectangle_of_src_polygon,
                                                    bounding_rectangle_of_dst_polygon=bounding_rectangle_of_dst_polygon)

        cropped_dst_rgb_array = cv2.warpPerspective(cropped_src_rgb_array,
                                                    warp_mats,
                                                    (bounding_rectangle_of_dst_polygon[2],
                                                     bounding_rectangle_of_dst_polygon[3]),
                                                    None,
                                                    flags=cv2.INTER_LINEAR,
                                                    borderMode=cv2.BORDER_REPLICATE
                                                    )
        if dst_cut_field:
            dst_polygon = dst_cut_field

        mixed_image =  ChangeFaceElement.fill_polygon_in_a_rectangle(dst_rgb_array=dst_rgb_array,
                                                                     dst_polygon=dst_polygon,
                                                                     cropped_dst_rgb_array=cropped_dst_rgb_array,
                                                                     bounding_rectangle_of_dst_polygon=bounding_rectangle_of_dst_polygon)

        return ChangeFaceElement.blur_image_colors_via_classifier(classifier=DEFAULT_CLASSIFIER,
                                                                  image_to_blur=mixed_image,
                                                                  training_image=dst_rgb_array,
                                                                  rectangle_of_image_to_blur=bounding_rectangle_of_dst_polygon,
                                                                  polygon_of_image_to_blur=dst_polygon)