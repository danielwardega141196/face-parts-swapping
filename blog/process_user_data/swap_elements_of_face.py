import json

import numpy as np
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
    MESSAGES_REGARDING_EXACTLY_ONE_FACE, LANDMARKS_FUNCTIONS


class ProcessUserPhoto:

    def __init__(self, input_photo, part_of_face, face_id):

        self._input_photo = input_photo
        self._part_of_face = part_of_face
        self._face_id = face_id
        self._image_in_base64 = None
        self._photo_from_db = None
        self._src_np_array = None
        self._dst_np_array = None
        self._src_endpoints = None
        self._dst_endpoints = None
        self._number_of_detected_faces = None
        self._more_or_less_than_one_photo = None

    @staticmethod
    def prepare_params_to_face_swapping(part_of_face, landmarks):
        """
        :param part_of_face: a specific part of the face
        :type part_of_face: string - str
        :param landmarks: characteristic points for the specific parts of a face.
        :type landmarks dictionary - {}
        :return: dictionary with keys: 'polygon' and 'cut_field'
        :rtype dictionary - {}
        """
        endpoints = {}
        if part_of_face == "nose":
            endpoints["polygon"] = landmarks["four_endpoints"]
            endpoints["cut_field"] = landmarks["six_endpoints"]
        else:
            endpoints["polygon"] = landmarks
            endpoints["cut_field"] = None

        return endpoints

    @staticmethod
    def more_or_less_than_one_face_info(number_of_detected_faces, json_format=True):
        """
        :param number_of_detected_faces: number of detected faces in an image
        :type number_of_detected_faces: integer - int
        :param json_format: param indicates if returned dictionary should be converted into a JSON object
        :type json_format: bool (True or False)
        :return dictionary where the number of detected faces is assigned to key named 'number_of_detected_faces'
                and False (bool) is assigned to key named 'face_detected_successfully'
        :rtype dictionary - {} or dictionary converted into a JSON object (type - django.http.response.JsonResponse)
        It depends on the parameter 'json_format'.
        """
        data = MESSAGES_REGARDING_MORE_OR_LESS_THAN_ONE_FACE
        data["number_of_detected_faces"] = number_of_detected_faces
        if json_format:
            return JsonResponse(data)
        return data

    @staticmethod
    def processed_img_info(swapped_part_of_face, json_format=True):
        """
        This function convert 'swapped_part_of_face' to Base64 and returns dictionary with data.
        The dictionary may be converted into a JSON object.
        :param swapped_part_of_face: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        The image shows a face with a part from other face.
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
    def prepare_endpoints_from_db(face_landmarks, part_of_face, json_format=True):
        """
        :param face_landmarks: characteristic points for specific parts of a face
        :type face_landmarks: dictionary - {} or dictionary converted into a JSON object (it depends on the parameter 'json_format')
        :param part_of_face: a specific part of the face whose data will be searched in the dictionary (face_landmarks)
        :type part_of_face: string - str
        :param json_format: param indicates if passed dictionary was converted into a JSON object
        :type json_format: bool (True or False)
        :return result of invoking function 'ProcessUserPhoto.prepare_params_to_face_swapping'
                (dictionary with keys: 'polygon' and 'cut_field')
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
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :return characteristic points for the specific parts of a face.
        Each part of face contained in LANDMARKS_FUNCTIONS
        has a function generating the characteristic points for given part of the face.
        :rtype dictionary - {}
        """
        landmarks_of_parts_of_face = {}
        for part_of_face in LANDMARKS_FUNCTIONS:
            landmarks_of_parts_of_face[part_of_face] = LANDMARKS_FUNCTIONS[part_of_face](face_landmarks)

        return landmarks_of_parts_of_face

    def _process_existing_image(self):
        """
        This function looks for the necessary parameters to swap two parts of a face.
        In this case the user's image has been saved previously in our database.
        If the number of detected faces in the image is not equal to 1 the variable
        'self._more_or_less_than_one_photo' will be set to 'True' otherwise
        the following variables: 'self._src_np_array', 'self._src_endpoints', 'self._dst_np_array', 'self._dst_endpoints'
        will have appropriate values and the variable 'self._more_or_less_than_one_photo' will be set to 'False'
        """
        self._photo_from_db = DBFunc.get_user_photo_data(photo_in_base64=self._image_in_base64)
        self._number_of_detected_faces = self._photo_from_db.number_of_detected_faces
        if self._number_of_detected_faces != 1:
            self._more_or_less_than_one_photo = True
        else:
            self._more_or_less_than_one_photo = False

            self._dst_np_array = convert_text_to_rgb_array(text=self._photo_from_db.rgb_array)
            src_face = DBFunc.get_part_of_face(part_of_face=self._part_of_face, id=self._face_id)
            self._src_endpoints = ProcessUserPhoto.prepare_endpoints_from_db(face_landmarks=src_face.face_landmarks,
                                                                             part_of_face=self._part_of_face)

            self._src_np_array = convert_text_to_rgb_array(text=src_face.rgb_array)
            self._dst_endpoints = ProcessUserPhoto.prepare_endpoints_from_db(
                face_landmarks=self._photo_from_db.face_landmarks,
                part_of_face=self._part_of_face)

    def _save_info_on_a_new_image(self, faces_landmarks):
        """
        This function saves informations about a new image into our database.
        :param faces_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        """
        landmarks = ProcessUserPhoto.get_landmarks_of_parts_of_face(face_landmarks=faces_landmarks)
        DBFunc.save_user_photo(photo_in_base64=self._image_in_base64,
                               number_of_detected_faces=self._number_of_detected_faces,
                               rgb_array=convert_rgb_array_to_text(rgb_array=self._dst_np_array),
                               face_landmarks=json.dumps(landmarks))

    def _process_new_image(self):
        """
        This function looks for the necessary parameters to swap two parts of a face.
        In this case the user's image is a completely new one.
        If the number of detected faces in the image is not equal to 1 the variable
        'self._more_or_less_than_one_photo' will be set to 'True' and
        informations about this image will be saved into our database.
        In another case, the following variables: 'self._src_np_array', 'self._src_endpoints', 'self._dst_np_array', 'self._dst_endpoints'
        will have appropriate values, the variable 'self._more_or_less_than_one_photo' will be set to 'False'
        and informations about this image will be saved in our database.
        """
        pil = set_mode_of_pil(pil=convert_base64_to_pil(image_in_base64=self._image_in_base64))
        self._dst_np_array = np.array(pil, dtype=np.uint8)

        faces_landmarks = get_faces_landmarks(rgb_array=self._dst_np_array)
        self._number_of_detected_faces = len(faces_landmarks)
        if self._number_of_detected_faces != 1:
            DBFunc.save_user_photo(photo_in_base64=self._image_in_base64,
                                   number_of_detected_faces=self._number_of_detected_faces)

            self._more_or_less_than_one_photo = True
        else:
            landmarks_of_the_face = LANDMARKS_FUNCTIONS[self._part_of_face](faces_landmarks[0])

            src_face = DBFunc.get_part_of_face(part_of_face=self._part_of_face, id=self._face_id)

            self._src_endpoints = ProcessUserPhoto.prepare_endpoints_from_db(face_landmarks=src_face.face_landmarks,
                                                                             part_of_face=self._part_of_face)
            self._dst_endpoints = ProcessUserPhoto.prepare_params_to_face_swapping(part_of_face=self._part_of_face,
                                                                                   landmarks=landmarks_of_the_face)
            self._src_np_array = convert_text_to_rgb_array(text=src_face.rgb_array)

            self._more_or_less_than_one_photo = False
            self._save_info_on_a_new_image(faces_landmarks=faces_landmarks[0])

    def _swap_part_of_face(self):
        """
        :return result of invoking function 'ChangeFaceElement.change_face_element'
        :rtype: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        return ChangeFaceElement.change_face_element(src_rgb_array=self._src_np_array,
                                                     dst_rgb_array=self._dst_np_array,
                                                     src_polygon=self._src_endpoints["polygon"],
                                                     dst_polygon=self._dst_endpoints["polygon"],
                                                     dst_cut_field=self._dst_endpoints["cut_field"])

    def _process_user_photo(self):
        """
        This function processes user's photo.
        :return dictionary with data regarding the photo.
        The dictionary have been converted into a JSON object.
        :rtype JSON object (type - django.http.response.JsonResponse)
        """
        self._image_in_base64 = remove_prefix_from_base64(base64_with_prefix=self._input_photo)

        if DBFunc.user_photo_exists(photo_in_base64=self._image_in_base64):
            self._process_existing_image()
        else:
            self._process_new_image()

        if self._more_or_less_than_one_photo:
            return ProcessUserPhoto.more_or_less_than_one_face_info(
                number_of_detected_faces=self._number_of_detected_faces)

        swapped_part_of_face = self._swap_part_of_face()
        return ProcessUserPhoto.processed_img_info(swapped_part_of_face=swapped_part_of_face)

    @classmethod
    def process_user_photo(cls, input_photo, part_of_face, face_id):
        """
        :param input_photo: base64-encoded image which has a special prefix.
        Here are some examples of the prefixes: 'data:image/png;base64,' , 'data:image/gif;base64,' , 'data:image/jpeg;base64,'
        :type input_photo: string - str
        :param part_of_face: a specific part of the face
        :type part_of_face string - str
        :param face_id: id of an example face stored in our database
        :type face_id: string - str
        :return informations about user's photo.
        :rtype: dictionary converted into a JSON object (type - django.http.response.JsonResponse)
        """
        photo_processing = cls(input_photo=input_photo,
                               part_of_face=part_of_face,
                               face_id=face_id)
        return photo_processing._process_user_photo()
