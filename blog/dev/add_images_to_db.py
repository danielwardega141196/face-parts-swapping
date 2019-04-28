"""
    This file should be executed at the level of the main directory of this repository.
"""
import json
import logging
import os
import sys

import django
from PIL import Image

# loading all necessary dependencies
sys.path.append('./')
os.environ["DJANGO_SETTINGS_MODULE"] = "myproject.settings"
django.setup()

from blog.settings import ACCEPTABLE_FILE_EXTENSIONS, \
    LANDMARKS_FUNCTIONS, DIRECTORIES_WITH_FACES

from blog.helpers import convert_img_to_base64, replace_special_signs, \
    convert_rgb_array_to_text, convert_pil_to_np_array
from blog.db_func import DBFunc
from apps.face_element_swapping import get_faces_landmarks

# Choosing the right part of the face for which we look for photos
# Currently, the following parts of the face are available:
# nose | lips
# Remember, when you want to add some image files,
# put them in the appropriate folder which is specified in 'settings.DIRECTORIES_WITH_FACES'
PART_OF_FACE = "lips"


class SaveFacesIntoDB:

    def __init__(self, part_of_face, directory_containing_imgs):

        self._part_of_face = part_of_face
        self._directory_containing_imgs = directory_containing_imgs
        self._current_image = None
        self._pil = None
        self._image_in_base64 = None
        self._image_name = None

    @staticmethod
    def get_names_of_image_files(directory_containing_imgs):
        """
        :param directory_containing_imgs: path to the directory which contains
               photos concerning particular part of the face(part_of_face).
        :type directory_containing_imgs: string - str
        :return: list containing paths to images with a acceptable extension(ACCEPTABLE_FILE_EXTENSIONS)
        :rtype: list - []
        """
        image_files = [image for image in os.listdir(directory_containing_imgs)
                       if image.endswith(ACCEPTABLE_FILE_EXTENSIONS)]
        return image_files

    def _deal_with_number_of_faces(self, number_of_detected_faces,
                                   face_landmarks,
                                   rgb_array):
        """
        If the number of detected faces(number_of_detected_faces) in the image is equal to 1
        this function detect the landmarks of the specified part of face (self._part_of_face)
        and save all information about the image into the database, otherwise only a specific message is displayed.

        :param number_of_detected_faces: number of detected faces in an image
        :type number_of_detected_faces: integer - int
        :param face_landmarks: landmarks of a single face generated
        by the function 'face_landmarks' from module named 'face_recognition'
        (link to the module named 'face_recognition' - https://pypi.org/project/face_recognition/)
        :type face_landmarks: dictionary - {}
        :param rgb_array: an RGB image converted into a numpy array (the array has following shape(y, x, 3))
        :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        """
        if number_of_detected_faces == 1:
            face_landmarks = LANDMARKS_FUNCTIONS[self._part_of_face](face_landmarks)
            face_landmarks = json.dumps({self._part_of_face: face_landmarks})

            DBFunc.save_example_photo(part_of_face=self._part_of_face,
                                      photo_in_base64=self._image_in_base64,
                                      photo_name=self._image_name,
                                      rgb_array=convert_rgb_array_to_text(rgb_array=rgb_array),
                                      face_landmarks=face_landmarks)

            info_msg = "Facial landmarks of the photo named '{photo_name}' " \
                       "have been successfully detected and saved into the database.". \
                format(photo_name=self._image_name)
            print(info_msg)
            logging.info(info_msg)
        elif number_of_detected_faces == 0:
            warn_msg = "No faces were detected on the photo named: '{photo_name}'.". \
                format(photo_name=self._image_name)
            print(warn_msg)
            logging.warning(warn_msg)
        else:
            warn_msg = "Too many faces (number_of_detected_faces) were detected " \
                       "on the photo named: '{photo_name}'.". \
                format(number_of_detected_faces=number_of_detected_faces,
                       photo_name=self._image_name)
            print(warn_msg)
            logging.warning(warn_msg)

    def _process_single_image(self):
        """
            This function process an image.
            If the image hadn't been previously saved into the database
            the function would search for the facial landmarks and then save the image into the database,
            otherwise only a message is displayed.
        """
        if not DBFunc.example_photo_exists(part_of_face=self._part_of_face,
                                           photo_name=self._image_name,
                                           photo_in_base64=self._image_in_base64):

            rgb_array = convert_pil_to_np_array(pil=self._pil)
            face_landmarks = get_faces_landmarks(rgb_array=rgb_array)

            number_of_detected_faces = len(face_landmarks)

            self._deal_with_number_of_faces(number_of_detected_faces=number_of_detected_faces,
                                            face_landmarks=face_landmarks[0],
                                            rgb_array=rgb_array)
        else:
            info_msg = "Facial landmarks of the photo named '{photo_name}' " \
                       "have been detected and saved previously.".format(photo_name=self._image_name)
            print(info_msg)
            logging.info(info_msg)

    def _save_faces_into_db(self):
        """
            This function saves informations about the correct photos into the database.
            The correct photo has a acceptable extension(ACCEPTABLE_FILE_EXTENSIONS) and
            only shows only one face.
        """
        image_files = SaveFacesIntoDB.get_names_of_image_files(
            directory_containing_imgs=self._directory_containing_imgs)
        for self._current_image in image_files:
            path_to_the_image = os.path.join(self._directory_containing_imgs, self._current_image)

            # When we have the path to the file, we create 'PIL' object
            self._pil = Image.open(path_to_the_image)
            self._image_in_base64 = convert_img_to_base64(img=self._pil)
            self._image_name = replace_special_signs(file_name=self._current_image)
            self._process_single_image()

    @classmethod
    def save_faces_into_db(cls, part_of_face, directory_containing_imgs):
        """
            This function enables to searching for images with human faces
            inside a specified directory(directory_containing_imgs).
            These images are converted to base64 as well as to np.array.
            For each image we detect the landmarks of the specified part of face (part_of_face).
            Then we save all this data into the appropriate database table.
            :param part_of_face: a specific part of the face
            :type part_of_face: string - str
            :param directory_containing_imgs: Path to the directory which contains
            photos concerning particular part of face(part_of_face).
            :type directory_containing_imgs: string - str
        """
        save_faces = cls(part_of_face=part_of_face,
                         directory_containing_imgs=directory_containing_imgs)

        save_faces._save_faces_into_db()


if __name__ == "__main__":
    SaveFacesIntoDB.save_faces_into_db(part_of_face=PART_OF_FACE,
                                       directory_containing_imgs=DIRECTORIES_WITH_FACES[PART_OF_FACE])
