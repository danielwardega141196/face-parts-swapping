from math import ceil

import cv2
import numpy as np

from .helpers import fill_pixel_if_belongs_to_polygon, get_rectangle_in_an_image
from .settings import (
    DEFAULT_CLASSIFIER,
    PERCENT_OF_NEAREST_NEIGHBOURS,
    RGB_MASK_FILLING_COLOR,
)


class ChangeFaceElement:
    def __init__(
        self,
        src_rgb_array=None,
        dst_rgb_array=None,
        src_polygon=None,
        dst_polygon=None,
        dst_cut_field=None,
        cropped_src_rgb_array=None,
        cropped_dst_rgb_array=None,
    ):
        self.src_rgb_array = src_rgb_array
        self.dst_rgb_array = dst_rgb_array
        self.src_polygon = src_polygon
        self.dst_polygon = dst_polygon
        self.dst_cut_field = dst_cut_field
        self.mask = dst_rgb_array
        self.tmp_dst_rgb_array = dst_rgb_array
        self.cropped_src_rgb_array = cropped_src_rgb_array
        self.cropped_dst_rgb_array = cropped_dst_rgb_array
        self.bounding_rectangle_of_src_polygon = src_polygon
        self.bounding_rectangle_of_dst_polygon = dst_polygon

    @property
    def src_rgb_array(self):
        return self._src_rgb_array

    @src_rgb_array.setter
    def src_rgb_array(self, src_rgb_array):
        self._src_rgb_array = src_rgb_array

    @property
    def dst_rgb_array(self):
        return self._dst_rgb_array

    @dst_rgb_array.setter
    def dst_rgb_array(self, dst_rgb_array):
        self._dst_rgb_array = dst_rgb_array

    @property
    def src_polygon(self):
        return self._src_polygon

    @src_polygon.setter
    def src_polygon(self, src_polygon):
        self._src_polygon = src_polygon

    @property
    def dst_polygon(self):
        return self._dst_polygon

    @dst_polygon.setter
    def dst_polygon(self, dst_polygon):
        self._dst_polygon = dst_polygon

    @property
    def dst_cut_field(self):
        return self._dst_cut_field

    @dst_cut_field.setter
    def dst_cut_field(self, dst_cut_field):
        self._dst_cut_field = dst_cut_field

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, dst_rgb_array):
        if dst_rgb_array is not None:
            self._mask = np.zeros_like(dst_rgb_array)
        else:
            self._mask = None

    @property
    def tmp_dst_rgb_array(self):
        return self._tmp_dst_rgb_array

    @tmp_dst_rgb_array.setter
    def tmp_dst_rgb_array(self, dst_rgb_array):
        if dst_rgb_array is not None:
            self._tmp_dst_rgb_array = dst_rgb_array.copy()
        else:
            self._tmp_dst_rgb_array = None

    @property
    def cropped_src_rgb_array(self):
        return self._cropped_src_rgb_array

    @cropped_src_rgb_array.setter
    def cropped_src_rgb_array(self, cropped_src_rgb_array):
        self._cropped_src_rgb_array = cropped_src_rgb_array

    @property
    def cropped_dst_rgb_array(self):
        return self._cropped_dst_rgb_array

    @cropped_dst_rgb_array.setter
    def cropped_dst_rgb_array(self, cropped_dst_rgb_array):
        self._cropped_dst_rgb_array = cropped_dst_rgb_array

    @property
    def bounding_rectangle_of_src_polygon(self):
        return self._bounding_rectangle_of_src_polygon

    @bounding_rectangle_of_src_polygon.setter
    def bounding_rectangle_of_src_polygon(self, src_polygon):
        if src_polygon is not None:
            self._bounding_rectangle_of_src_polygon = (
                ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=src_polygon)
            )
        else:
            self._bounding_rectangle_of_src_polygon = None

    @property
    def bounding_rectangle_of_dst_polygon(self):
        return self._bounding_rectangle_of_dst_polygon

    @bounding_rectangle_of_dst_polygon.setter
    def bounding_rectangle_of_dst_polygon(self, dst_polygon):
        if dst_polygon is not None:
            self._bounding_rectangle_of_dst_polygon = (
                ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=dst_polygon)
            )
        else:
            self._bounding_rectangle_of_dst_polygon = None

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
    def get_cropped_polygon(polygon):
        """
        The function subtracts the 'x' value of the start point of the bounding rectangle (bounding_rectangle_of_polygon[0])
        from each 'x' value of points of the polygon.
        The function subtracts the 'y' value of the start point of the bounding rectangle (bounding_rectangle_of_polygon[1])
        from each 'y' value of points of the polygon.
        :param polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                        All elements in list (or tuple) should represent a polygon.
        :type polygon: list - [] or tuple - ()
        :return list of tuples
        :rtype list - []
        """
        bounding_rectangle_of_polygon = (
            ChangeFaceElement.get_bounding_rectangle_of_polygon(polygon=polygon)
        )
        cropped_polygon = [
            (
                point[0] - bounding_rectangle_of_polygon[0],
                point[1] - bounding_rectangle_of_polygon[1],
            )
            for point in polygon
        ]

        return cropped_polygon

    @staticmethod
    def get_warp_mats(src_polygon, dst_polygon):
        """
        :param src_polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                            All elements in list (or tuple) should represent a source polygon.
        :type src_polygon: list - [] or tuple - ()
        :param dst_polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                            All elements in list (or tuple) should represent a destination polygon.
        :type dst_polygon: list - [] or tuple - ()
        :return 3 x 3 matrix of a perspective transform between the source polygon (src_polygon) and the destination polygon (dst_polygon).
        :rtype numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        cropped_src_polygon = ChangeFaceElement.get_cropped_polygon(polygon=src_polygon)
        cropped_dst_polygon = ChangeFaceElement.get_cropped_polygon(polygon=dst_polygon)

        # By clicking the link below you can see
        # more information on the function 'getPerspectiveTransform' from module 'cv2'
        # https://docs.opencv.org/2.4/modules/imgproc/doc/geometric_transformations.html#cv2.getPerspectiveTransform
        warp_mats = cv2.getPerspectiveTransform(
            np.float32(cropped_src_polygon), np.float32(cropped_dst_polygon)
        )
        return warp_mats

    @staticmethod
    def get_vector_of_pixels(rgb_array, bounding_rectangle_of_polygon, unique=True):
        """
        :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param bounding_rectangle_of_polygon: tuple or list with coordinates of the start point of the rectangle
               and the width and height of this rectangle - (x, y, width, height) or [x, y, width, height]
        :type bounding_rectangle_of_polygon: tuple - () or list - (). The tuple or list should have four elements.
        :param unique: params indicates if returned vector will contain only unique pixel values
        :type unique: bool (True or False)
        :return: vector of all pixels or vector of unique pixels (it depends on the parameter 'unique')
        :rtype numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        data = get_rectangle_in_an_image(
            np_array=rgb_array,
            bounding_rectangle_of_polygon=bounding_rectangle_of_polygon,
        )
        shape = data.shape
        data = np.reshape(data, (shape[0] * shape[1], shape[2]))
        if unique:
            data = np.unique(data, axis=0)
        return data

    @staticmethod
    def adjust_image_colors_via_classifier(
        classifier, training_image, image_to_adjust, polygon_of_images
    ):
        """
        This function replaces pixels of 'image_to_adjust' that are included in 'polygon_of_images'.
        Every newer pixel value is taken from the set of pixels of 'training_image' that are included in 'polygon_of_images'.
        :param classifier: object representing a classifier.
        The classifier is based on the kNN algorithm (https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm).
        The first parameter of this classifier must be the number of neighbors(integer - int).
        Examples of the classifiers:
            https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
            https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html
        :param training_image: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        Pixels of this image will be used to fitting the classifier.
        :type training_image: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param image_to_adjust: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        Some of the pixels in this image will be replaced by
        the pixels of the second image that are the most similar to them in terms of color.
        :type image_to_adjust: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param polygon_of_images: list of tuple of points in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...))
        All points in this list or tuple form a polygon.
        Pixels of 'image_to_adjust' that are inside the polygon will be replaced.
        :type polygon_of_images: list - [] or tuple - ()
        :return: 'image_to_adjust' in which pixels inside 'polygon_of_images' have been replaced.
        :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        bounding_rectangle_of_polygon = (
            ChangeFaceElement.get_bounding_rectangle_of_polygon(
                polygon=polygon_of_images
            )
        )
        training_data = ChangeFaceElement.get_vector_of_pixels(
            rgb_array=training_image,
            bounding_rectangle_of_polygon=bounding_rectangle_of_polygon,
        )
        training_data_avg = np.average(training_data, axis=0)
        training_data_std = np.std(training_data, axis=0)

        normalized_training_data = (
            training_data - training_data_avg
        ) / training_data_std
        training_labels = range(training_data.shape[0])

        data_to_adjust = ChangeFaceElement.get_vector_of_pixels(
            rgb_array=image_to_adjust,
            bounding_rectangle_of_polygon=bounding_rectangle_of_polygon,
            unique=False,
        )
        data_to_adjust = (data_to_adjust - training_data_avg) / training_data_std

        classifier = classifier(
            n_neighbors=ceil(PERCENT_OF_NEAREST_NEIGHBOURS * training_data.shape[0])
        )
        classifier.fit(normalized_training_data, training_labels)
        labels = classifier.kneighbors(data_to_adjust, return_distance=False)

        label_idx = 0
        for row_idx in range(
            bounding_rectangle_of_polygon[1],
            bounding_rectangle_of_polygon[1] + bounding_rectangle_of_polygon[3],
        ):
            for column_idx in range(
                bounding_rectangle_of_polygon[0],
                bounding_rectangle_of_polygon[0] + bounding_rectangle_of_polygon[2],
            ):
                pixel_value = np.round(
                    np.average(training_data[labels[label_idx]], axis=0)
                ).astype(np.uint8)
                fill_pixel_if_belongs_to_polygon(
                    rgb_array=image_to_adjust,
                    polygon=polygon_of_images,
                    row_idx=row_idx,
                    column_idx=column_idx,
                    pixel_value=pixel_value,
                )
                label_idx += 1

        return image_to_adjust

    def _fill_pixels(
        self,
        row_idx,
        column_idx,
        cropped_dst_rgb_array_row_idx,
        cropped_dst_rgb_array_column_idx,
    ):
        """
        This function fills chosen pixels of 'self.tmp_dst_rgb_array' and 'self.mask'.
        :param row_idx: current row index of 'self.tmp_dst_rgb_array' and 'self.mask'
        :type row_idx: integer - int
        :param column_idx: current column index of 'self.tmp_dst_rgb_array' and 'self.mask'
        :type column_idx: integer - int
        :param cropped_dst_rgb_array_row_idx: current row index of 'self._cropped_dst_rgb_array'
        :type cropped_dst_rgb_array_row_idx: integer - int
        :param cropped_dst_rgb_array_column_idx: current column index of 'self._cropped_dst_rgb_array'
        :type cropped_dst_rgb_array_column_idx: integer - int
        """
        fill_pixel_if_belongs_to_polygon(
            rgb_array=self.tmp_dst_rgb_array,
            polygon=self.dst_polygon,
            row_idx=row_idx,
            column_idx=column_idx,
            pixel_value=self._cropped_dst_rgb_array[cropped_dst_rgb_array_row_idx][
                cropped_dst_rgb_array_column_idx
            ],
        )

        fill_pixel_if_belongs_to_polygon(
            rgb_array=self.mask,
            polygon=self.dst_polygon,
            row_idx=row_idx,
            column_idx=column_idx,
            pixel_value=RGB_MASK_FILLING_COLOR,
        )

    def _fill_polygon_in_an_image(self):
        """
        This function fills pixels of 'self.mask' and 'self.tmp_dst_rgb_array'.
        Every newer pixel value is taken from the set of pixels of 'training_image' that are included in 'polygon_of_images'.
        """
        cropped_dst_rgb_array_row_idx = 0
        for row_idx in range(
            self.bounding_rectangle_of_dst_polygon[1],
            self.bounding_rectangle_of_dst_polygon[1]
            + self.bounding_rectangle_of_dst_polygon[3],
        ):
            cropped_dst_rgb_array_column_idx = 0
            for column_idx in range(
                self.bounding_rectangle_of_dst_polygon[0],
                self.bounding_rectangle_of_dst_polygon[0]
                + self.bounding_rectangle_of_dst_polygon[2],
            ):
                self._fill_pixels(
                    row_idx=row_idx,
                    column_idx=column_idx,
                    cropped_dst_rgb_array_row_idx=cropped_dst_rgb_array_row_idx,
                    cropped_dst_rgb_array_column_idx=cropped_dst_rgb_array_column_idx,
                )

                cropped_dst_rgb_array_column_idx += 1
            cropped_dst_rgb_array_row_idx += 1

    @classmethod
    def fill_polygon_in_a_rectangle(
        cls, dst_rgb_array, dst_polygon, cropped_dst_rgb_array
    ):
        """
        This function fills pixels of 'dst_rgb_array' that are included in 'dst_polygon'.
        Newer pixels values are contained in 'cropped_dst_rgb_array'.
        The function makes also the output image looks uniformly.
        :param dst_rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        :type dst_rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param dst_polygon: list of tuple of points in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...))
        All points in this list or tuple form a polygon.
        :type dst_polygon: list - [] or tuple - ()
        :param cropped_dst_rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        :type cropped_dst_rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """

        fill_polygon = cls(
            dst_rgb_array=dst_rgb_array,
            dst_polygon=dst_polygon,
            cropped_dst_rgb_array=cropped_dst_rgb_array,
        )

        fill_polygon._fill_polygon_in_an_image()
        center = (
            (
                2 * fill_polygon.bounding_rectangle_of_dst_polygon[0]
                + fill_polygon.bounding_rectangle_of_dst_polygon[2]
            )
            // 2,
            (
                2 * fill_polygon.bounding_rectangle_of_dst_polygon[1]
                + fill_polygon.bounding_rectangle_of_dst_polygon[3]
            )
            // 2,
        )

        return cv2.seamlessClone(
            fill_polygon.tmp_dst_rgb_array,
            fill_polygon.dst_rgb_array,
            fill_polygon.mask,
            center,
            cv2.NORMAL_CLONE,
        )

    def _get_cropped_rgb_arrays(self):
        """
        This function looks for the appropriate values of
        'self.cropped_src_rgb_array' and 'self.cropped_dst_rgb_array'.
        """
        self.cropped_src_rgb_array = get_rectangle_in_an_image(
            np_array=self.src_rgb_array,
            bounding_rectangle_of_polygon=self.bounding_rectangle_of_src_polygon,
        )

        warp_mats = ChangeFaceElement.get_warp_mats(
            src_polygon=self.src_polygon, dst_polygon=self.dst_polygon
        )

        self.cropped_dst_rgb_array = cv2.warpPerspective(
            self.cropped_src_rgb_array,
            warp_mats,
            (
                self.bounding_rectangle_of_dst_polygon[2],
                self.bounding_rectangle_of_dst_polygon[3],
            ),
            None,
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE,
        )

    @classmethod
    def change_face_element(
        cls, src_rgb_array, dst_rgb_array, src_polygon, dst_polygon, dst_cut_field=None
    ):
        """
        This function moves the source polygon(src_polygon) contained in source image(src_rgb_array)
        to the destination polygon(dst_polygon) contained in destination image(dst_rgb_array).
        If dst_cut_field is not None the output image has only these new pixels that are contained in 'dst_cut_field'.
        :param src_rgb_array: an RGB source image converted into a numpy array (the array has following shape(y, x, 3))
        :type src_rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param dst_rgb_array: an RGB destination image converted into a numpy array (the array has following shape(y, x, 3))
        :type dst_rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param src_polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                            All elements in list (or tuple) should represent a source polygon.
        :type src_polygon: list - [] or tuple - ()
        :param dst_polygon: list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
                            All elements in list (or tuple) should represent a destination polygon.
        :type dst_polygon: list - [] or tuple - ()
        :param dst_cut_field: None, list or tuple of coordinates in 2D Space ([(x, y),(x, y),(x, y)...] or ((x, y),(x, y),(x, y)...)).
        :type dst_cut_field: None, list - [] or tuple - ()
        :return: an RGB image converted into a numpy array.
        The image has exactly the same shape as 'dst_rgb_array'
        and contains 'src_polygon' from 'src_rgb_array'.
        :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        change_face_element = cls(
            src_rgb_array=src_rgb_array,
            dst_rgb_array=dst_rgb_array,
            src_polygon=src_polygon,
            dst_polygon=dst_polygon,
            dst_cut_field=dst_cut_field,
        )

        change_face_element._get_cropped_rgb_arrays()
        if dst_cut_field:
            dst_polygon = dst_cut_field

        mixed_image = ChangeFaceElement.fill_polygon_in_a_rectangle(
            dst_rgb_array=dst_rgb_array,
            dst_polygon=dst_polygon,
            cropped_dst_rgb_array=change_face_element.cropped_dst_rgb_array,
        )

        return ChangeFaceElement.adjust_image_colors_via_classifier(
            classifier=DEFAULT_CLASSIFIER,
            training_image=dst_rgb_array,
            image_to_adjust=mixed_image,
            polygon_of_images=dst_polygon,
        )
