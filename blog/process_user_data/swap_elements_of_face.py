import json

import numpy as np
from PIL import Image
from django.http import JsonResponse

from apps.face_element_swapping import get_faces_landmarks
from apps.face_element_swapping.change_faces import ChangeFaceElement
from ..db_func import DBFunc
from ..helpers import convert_img_to_base64, \
    convert_base64_to_pil, \
    convert_rgb_array_to_text, \
    convert_text_to_rgb_array, \
    remove_prefix_from_base64, \
    set_mode_of_pil
from ..settings import MESSAGES_REGARDING_MORE_OR_LESS_THAN_ONE_FACE, \
    MESSAGES_REGARDING_EXACTLY_ONE_FACE, LANDMARKS_FUNCTIONS, MINIMUM_VALUE_OF_THE_ALPHA_CHANNEL, \
    DEFAULT_PIL_MODE, PIL_MODE_OF_TRANSPARENT_PHOTOS, CORRECT_NUMBER_OF_CHANNELS_PER_PIXEL, \
    INDEX_OF_THE_NUMBER_OF_CHANNELS_PER_PIXEL, INDEX_OF_THE_VALUE_OF_ALPHA_CHANNEL, PARTS_OF_THE_FACE_WITH_THE_CUT_FIELD


class ProcessUserPhoto:

    def __init__(self, input_photo, part_of_face, face_id):

        self._input_photo = input_photo
        self._part_of_face = part_of_face
        self._face_id = face_id
        self._photo_in_base64 = None
        self._src_rgb_array = None
        self._dst_rgb_array = None
        self._src_endpoints = None
        self._dst_endpoints = None
        self._transparent_pixels = []
        self._number_of_detected_faces = None
        self._more_or_less_than_one_photo = None

    @staticmethod
    def prepare_params_to_face_swapping(part_of_face,
                                        landmarks):
        """
        :param part_of_face: a specific part of the face
        :type part_of_face: string - str
        :param landmarks: characteristic points for the specific parts of a face.
        The landmarks should comes from calling one of the functions
        included in the 'LANDMARKS_FUNCTIONS' dictionary (from the file '..settings').
        :type landmarks: dictionary - {}
        :return: dictionary with the keys: 'polygon' and 'cut_field'
        :rtype: dictionary - {}
        """
        endpoints = {}
        if part_of_face.lower() in map(str.lower, PARTS_OF_THE_FACE_WITH_THE_CUT_FIELD):
            endpoints["polygon"] = landmarks["four_endpoints"]
            endpoints["cut_field"] = landmarks["six_endpoints"]
        else:
            endpoints["polygon"] = landmarks
            endpoints["cut_field"] = None
        return endpoints

    @staticmethod
    def more_or_less_than_one_face_info(number_of_detected_faces,
                                        json_format=True):
        """
        :param number_of_detected_faces: number of detected faces in an image
        :type number_of_detected_faces: integer - int
        :param json_format: param indicates if returned dictionary should be converted into a JSON object
        :type json_format: bool (True or False)
        :return dictionary where the number of detected faces is assigned to the key named 'number_of_detected_faces'
                and False (bool) is assigned to the key named 'face_detected_successfully'.
        :rtype dictionary - {} or dictionary converted into a JSON object (type - django.http.response.JsonResponse)
        It depends on the parameter 'json_format'.
        """
        data = MESSAGES_REGARDING_MORE_OR_LESS_THAN_ONE_FACE
        data["number_of_detected_faces"] = number_of_detected_faces
        if json_format:
            return JsonResponse(data)
        return data

    @staticmethod
    def processed_img_info(swapped_part_of_face,
                           json_format=True):
        """
        This function converts 'swapped_part_of_face' to Base64 and returns a dictionary with data.
        The dictionary may be converted into a JSON object.
        :param swapped_part_of_face: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        The image shows a face with a part from a different face.
        :type swapped_part_of_face: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param json_format: param indicates if returned dictionary should be converted into a JSON object
        :type json_format: bool (True or False)
        :return dictionary: {
                                "face_detected_successfully": True,
                                "number_of_detected_faces": 1,
                                "img_src": 'swapped_part_of_face' converted to Base64
                                        }
        :rtype dictionary - {} or dictionary converted into a JSON object (type  - django.http.response.JsonResponse)
        It depends on the parameter 'json_format'.
        """
        data = MESSAGES_REGARDING_EXACTLY_ONE_FACE
        data["img_src"] = convert_img_to_base64(img=swapped_part_of_face)
        if json_format:
            return JsonResponse(data)
        return data

    @staticmethod
    def prepare_endpoints_from_db(face_landmarks,
                                  part_of_face,
                                  json_format=True):
        """
        :param face_landmarks: characteristic points for specific parts of a face
        :type face_landmarks: dictionary - {} or dictionary converted into a JSON object
        (it depends on the parameter 'json_format')
        :param part_of_face: a specific part of the face whose data will be searched in the dictionary(face_landmarks)
        :type part_of_face: string - str
        :param json_format: param indicates if the passed dictionary('face_landmarks') was converted into a JSON object
        :type json_format: bool (True or False)
        :return result of calling the function 'prepare_params_to_face_swapping' from this class.
                (dictionary with the keys: 'polygon' and 'cut_field')
        :rtype dictionary - {}
        """
        if json_format:
            face_landmarks = json.loads(face_landmarks)[part_of_face]

        return ProcessUserPhoto.prepare_params_to_face_swapping(part_of_face=part_of_face,
                                                                landmarks=face_landmarks)

    @staticmethod
    def get_landmarks_of_parts_of_face(face_landmarks):
        """
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from the module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return characteristic points for the specific parts of a face.
        Each part of the face contained in the 'LANDMARKS_FUNCTIONS' dictionary
        has a function generating the characteristic points for given part of the face.
        :rtype dictionary - {}
        """
        landmarks_of_parts_of_face = {}
        for part_of_face in LANDMARKS_FUNCTIONS:
            landmarks_of_parts_of_face[part_of_face] = LANDMARKS_FUNCTIONS[part_of_face](face_landmarks)

        return landmarks_of_parts_of_face

    @staticmethod
    def prepare_transparent_pixels(rgba_array):
        """
        This function looks for the pixels, whose alpha channel value is less than
        the value of 'MINIMUM_VALUE_OF_ALPHA_CHANNEL'.
        :param rgba_array: an RGBA image converted into a numpy array (the array has following shape(y, x, 4))
        :type rgba_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :return: list of dictionaries. Each of these dictionaries has the following keys: 'row_idx', 'column_idx', 'value'.
        The key 'row_idx' represent the index of a pixel's row (integer - int).
        The key 'column_idx' represent the index of a pixel's column (integer - int).
        The key 'value' represent the RGBA color of a pixel(list which contains four integers).
        :rtype: list - []
        """
        if rgba_array.shape[INDEX_OF_THE_NUMBER_OF_CHANNELS_PER_PIXEL] != CORRECT_NUMBER_OF_CHANNELS_PER_PIXEL:
            error_info = "The passed image has the incorret number of channels per pixel. " \
                         "The correct number is equal to {correct_number_of_channels_per_pixel}.".format(
                correct_number_of_channels_per_pixel=CORRECT_NUMBER_OF_CHANNELS_PER_PIXEL)
            raise ValueError(error_info)

        transparent_pixels = []
        rows, cols, _ = np.where(
            rgba_array[:, :, [INDEX_OF_THE_VALUE_OF_ALPHA_CHANNEL]] < MINIMUM_VALUE_OF_THE_ALPHA_CHANNEL)
        for i in range(len(rows)):
            row_idx = int(rows[i])
            column_idx = int(cols[i])
            pixel_value = rgba_array[row_idx][column_idx].tolist()
            pixel_dictionary = {"row_idx": row_idx,
                                "column_idx": column_idx,
                                "value": pixel_value}
            transparent_pixels.append(pixel_dictionary)

        return transparent_pixels

    @staticmethod
    def add_transparent_pixels_to_an_rgb_image(rgb_array,
                                               transparent_pixels):
        """
        This function converts 'rgb_array' into an RGBA numpy array.
        Then the pixels included in the passed list ('transparent_pixels') will be placed in this array.
        :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param transparent_pixels: list of dictionaries.
        Each of these dictionaries has the following keys: 'row_idx', 'column_idx', 'value'.
        The key 'row_idx' represent the index of a pixel's row (integer - int).
        The key 'column_idx' represent the index of a pixel's column (integer - int).
        The key 'value' represent the RGBA color of a pixel(list which contains four integers).
        This parameter should comes from calling
        the function 'prepare_transparent_pixels' contained in this class.
        :rtype: list - []
        :return: 'rgb_array' converted into an RGBA numpy array.
        The array possess the values of pixels included in the passed list('transparent_pixels').
        :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        pil = Image.fromarray(rgb_array)
        pil_rgba = set_mode_of_pil(pil=pil, mode=PIL_MODE_OF_TRANSPARENT_PHOTOS)
        rgba_array = np.array(pil_rgba, dtype=np.uint8)

        for pixel in transparent_pixels:
            for channel_idx in range(len(pixel["value"])):
                rgba_array[pixel["row_idx"]][pixel["column_idx"]][channel_idx] = pixel["value"][channel_idx]

        return rgba_array

    def _process_existing_image(self):
        """
        This function looks for the necessary parameters to swap the same part of the face.
        In this case the user image has been saved previously in our database.
        If the number of detected faces in the image is not equal to 1 the variable
        'self._more_or_less_than_one_photo' will be set to 'True' otherwise
        the following variables: 'self._src_rgb_array', 'self._src_endpoints',
        'self._dst_rgb_array', 'self._dst_endpoints'.
        will have appropriate values and the variable 'self._more_or_less_than_one_photo' will be set to 'False'.
        """
        photo_from_db = DBFunc.get_user_photo_data(photo_in_base64=self._photo_in_base64)
        self._number_of_detected_faces = photo_from_db.number_of_detected_faces
        if self._number_of_detected_faces != 1:
            self._more_or_less_than_one_photo = True
        else:
            self._more_or_less_than_one_photo = False

            self._dst_rgb_array = convert_text_to_rgb_array(text=photo_from_db.rgb_array)
            src_face = DBFunc.get_example_photo_data(part_of_face=self._part_of_face, row_id=self._face_id)
            self._src_endpoints = ProcessUserPhoto.prepare_endpoints_from_db(face_landmarks=src_face.face_landmarks,
                                                                             part_of_face=self._part_of_face)
            self._src_rgb_array = convert_text_to_rgb_array(text=src_face.rgb_array)
            self._dst_endpoints = ProcessUserPhoto.prepare_endpoints_from_db(
                face_landmarks=photo_from_db.face_landmarks,
                part_of_face=self._part_of_face)
            self._transparent_pixels = json.loads(photo_from_db.transparent_pixels)

    def _save_info_on_a_new_image(self,
                                  faces_landmarks):
        """
        This function saves informations about a new image into our database.
        :param faces_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from the module named 'face_recognition'.
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        """
        landmarks = ProcessUserPhoto.get_landmarks_of_parts_of_face(face_landmarks=faces_landmarks)
        DBFunc.save_user_photo(photo_in_base64=self._photo_in_base64,
                               number_of_detected_faces=self._number_of_detected_faces,
                               rgb_array=convert_rgb_array_to_text(rgb_array=self._dst_rgb_array),
                               transparent_pixels=json.dumps(self._transparent_pixels),
                               face_landmarks=json.dumps(landmarks))

    def _process_new_image(self):
        """
        This function looks for the necessary parameters to swap the same part of the face.
        In this case the user image is a completely new one.
        If the number of detected faces in the image is not equal to 1 the variable
        'self._more_or_less_than_one_photo' will be set to 'True' and
        informations about this image will be saved into our database.
        In another case, the following variables: 'self._src_rgb_array', 'self._src_endpoints',
        'self._dst_rgb_array', 'self._dst_endpoints'.
        will have appropriate values, the variable 'self._more_or_less_than_one_photo' will be set to 'False'
        and informations about this image will be saved in our database.
        """
        dst_img_pil = convert_base64_to_pil(photo_in_base64=self._photo_in_base64)

        if dst_img_pil.mode != DEFAULT_PIL_MODE:
            dst_rgba_array = np.array(set_mode_of_pil(pil=dst_img_pil, mode=PIL_MODE_OF_TRANSPARENT_PHOTOS),
                                      dtype=np.uint8)
            self._transparent_pixels = ProcessUserPhoto.prepare_transparent_pixels(rgba_array=dst_rgba_array)

        dst_img_pil = set_mode_of_pil(pil=dst_img_pil, mode=DEFAULT_PIL_MODE)

        self._dst_rgb_array = np.array(dst_img_pil, dtype=np.uint8)
        faces_landmarks = get_faces_landmarks(rgb_array=self._dst_rgb_array)
        self._number_of_detected_faces = len(faces_landmarks)
        if self._number_of_detected_faces != 1:
            DBFunc.save_user_photo(photo_in_base64=self._photo_in_base64,
                                   number_of_detected_faces=self._number_of_detected_faces)
            self._more_or_less_than_one_photo = True
        else:
            landmarks_of_the_part_of_face = LANDMARKS_FUNCTIONS[self._part_of_face](faces_landmarks[0])
            src_face = DBFunc.get_example_photo_data(part_of_face=self._part_of_face, row_id=self._face_id)
            self._src_endpoints = ProcessUserPhoto.prepare_endpoints_from_db(face_landmarks=src_face.face_landmarks,
                                                                             part_of_face=self._part_of_face)
            self._dst_endpoints = ProcessUserPhoto.prepare_params_to_face_swapping(part_of_face=self._part_of_face,
                                                                                   landmarks=landmarks_of_the_part_of_face)
            self._src_rgb_array = convert_text_to_rgb_array(text=src_face.rgb_array)
            self._more_or_less_than_one_photo = False
            self._save_info_on_a_new_image(faces_landmarks=faces_landmarks[0])

    def _swap_part_of_face(self):
        """
        :return result of calling the function 'change_face_element' from the class 'ChangeFaceElement'
        (The class is located in 'apps.face_element_swapping.change_faces').
        :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        return ChangeFaceElement.change_face_element(src_rgb_array=self._src_rgb_array,
                                                     dst_rgb_array=self._dst_rgb_array,
                                                     src_polygon=self._src_endpoints["polygon"],
                                                     dst_polygon=self._dst_endpoints["polygon"],
                                                     dst_cut_field=self._dst_endpoints["cut_field"])

    def _process_user_photo(self):
        """
        This function processes user photo.
        :return: dictionary with data regarding the photo.
        The dictionary have been converted into a JSON object.
        :rtype: a JSON object (type - django.http.response.JsonResponse)
        """
        self._photo_in_base64 = remove_prefix_from_base64(base64_with_prefix=self._input_photo)

        if DBFunc.user_photo_exists(photo_in_base64=self._photo_in_base64):
            self._process_existing_image()
        else:
            self._process_new_image()

        if self._more_or_less_than_one_photo:
            return ProcessUserPhoto.more_or_less_than_one_face_info(
                number_of_detected_faces=self._number_of_detected_faces)

        swapped_part_of_face = self._swap_part_of_face()
        if self._transparent_pixels:
            swapped_part_of_face = ProcessUserPhoto.add_transparent_pixels_to_an_rgb_image(
                rgb_array=swapped_part_of_face,
                transparent_pixels=self._transparent_pixels)
        return ProcessUserPhoto.processed_img_info(swapped_part_of_face=swapped_part_of_face)

    @classmethod
    def process_user_photo(cls,
                           input_photo,
                           part_of_face,
                           face_id):
        """
        The function processes the input user photo('input_photo').
        If the photo contains more or less than one face,
        this function will return the result of calling
        the function 'more_or_less_than_one_face_info'(contained in this class).
        If the input user photo is correct,
        this function will find the photo (with the passed id - 'face_id') in the database
        and then swap the part of the face indicated by the 'part_of_face' parameter.
        :param input_photo: base64-encoded image which has a special prefix.
        Here are some examples of the prefixes: 'data:image/png;base64,' ,
                                                'data:image/gif;base64,' ,
                                                'data:image/jpeg;base64,'
        :type input_photo: string - str
        :param part_of_face: a specific part of the face
        :type part_of_face string - str
        :param face_id: id of an example face stored in our database
        :type face_id: string - str
        :return: If the photo contains more or less than one face,
        this function will return the result of calling the function 'more_or_less_than_one_face_info'
        (contained in this class). If the photo is correct, this function will return
        the result of calling the function 'processed_img_info'(also contained in this class).
        :rtype: dictionary converted into a JSON object (type - django.http.response.JsonResponse)
        """
        photo_processing = cls(input_photo=input_photo,
                               part_of_face=part_of_face,
                               face_id=face_id)
        return photo_processing._process_user_photo()
