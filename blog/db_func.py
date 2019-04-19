from .models import Photo, DB_OBJECTS


class DBFunc:

    @staticmethod
    def save_photo(photo_in_base64, number_of_detected_faces,
                   rgb_array=None, face_landmarks=None):
        """
        This function saves user photos in the database table
        represented by 'Photo' object (from the file '.models').
        :param photo_in_base64: RGB photo converted to base64
        :type photo_in_base64: string - str
        :param number_of_detected_faces: number of detected faces in the photo
        :type number_of_detected_faces: integer - int
        :param rgb_array: the same photo converted into a numpy array (the array has following shape(y, x, 3))
        :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param face_landmarks: characteristic points for the specific parts of a face.
        A dictionary represeting these points should come from invoking
        the function 'get_landmarks_of_parts_of_face' (class 'ProcessUserPhoto' from the file '.models').
        :type face_landmarks: dictionary - {}
        """
        Photo.objects.create(photo_in_base64=photo_in_base64,
                             rgb_array=rgb_array,
                             number_of_detected_faces=number_of_detected_faces,
                             face_landmarks=face_landmarks)

    @staticmethod
    def get_user_photo_data(photo_in_base64):
        """
        :param photo_in_base64: photo converted to base64
        :type photo_in_base64: string - str
        :return: an instance of the 'Photo' class (from the file '.models')
        representing the row containing the photo or
        None if the photo doesn't exist in the database
        :rtype: an instance of the 'Photo' class (from the file '.models') or None
        """
        if DBFunc.user_photo_exists(photo_in_base64=photo_in_base64):
            return Photo.objects.get(photo_in_base64=photo_in_base64)
        return None

    @staticmethod
    def user_photo_exists(photo_in_base64):
        """
        This function checks if a photo(converted to base64) exists
        in the database table represented by 'Photo' object (from the file '.models').
        :param photo_in_base64: photo converted to base64
        :type photo_in_base64: string - str
        :return: True if the photo exists, False if not
        :rtype: bool (True or False)
        """
        return Photo.objects.filter(photo_in_base64=photo_in_base64).exists()

    @staticmethod
    def example_photo_exists(part_of_face,
                             photo_name,
                             photo_in_base64):

        """
        This function checks if a photo with the specified name('photo name'),
        converted to base64 exists in the database table indicated by 'part_of_face'.
        :param part_of_face: a specific part of the face
        This param must be a key of DB_OBJECTS dictionary (from the file '.models')
        whose values represent database tables.
        :type part_of_face: string - str
        :param photo_name: name of the photo
        :type photo_name: string - str
        :param photo_in_base64: photo converted to base64
        :type photo_in_base64: string - str
        :return: True if the photo exists, False if not
        :rtype: bool (True or False)
        :raises ValueError: if 'part_of_face' (passed as a parameter) is not a key of DB_OBJECTS dictionary
        """
        if part_of_face not in DB_OBJECTS:
            available_parts_of_face = ", ".join(map(lambda key: "'" + str(key) + "'", DB_OBJECTS.keys()))
            error_info = "The provided part of the face ('{part_of_face}') " \
                         "is not available. " \
                         "Available parts of the face: " \
                         "{available_parts_of_face}.".format(part_of_face=part_of_face,
                                                             available_parts_of_face=available_parts_of_face)
            raise ValueError(error_info)

        return DB_OBJECTS[part_of_face].objects.filter(photo_name=photo_name,
                                                       photo_in_base64=photo_in_base64).exists()

    @staticmethod
    def get_part_of_face(part_of_face, id):
        """
        :param part_of_face: a specific part of the face
        This param must be a key of DB_OBJECTS dictionary (from the file '.models')
        whose values represent database tables.
        :type part_of_face: string - str
        :param id: id of a row in the database table.
        :type id: integer - int
        :return:  object representing the row with passed (as a parameter) id or None if
        a row with this id doesn't exist
        :rtype: object representing a class which inherit from 'ParfOfFace'(from the file '.models') or None
        :raises ValueError: if 'part_of_face' (passed as a parameter) is not a key of DB_OBJECTS dictionary
        """

        if part_of_face not in DB_OBJECTS:
            available_parts_of_face = ", ".join(map(lambda key: "'" + str(key) + "'", DB_OBJECTS.keys()))
            error_info = "The provided part of the face ('{part_of_face}') " \
                         "is not available. " \
                         "Available parts of the face: " \
                         "{available_parts_of_face}.".format(part_of_face=part_of_face,
                                                             available_parts_of_face=available_parts_of_face)
            raise ValueError(error_info)

        db_row = DB_OBJECTS[part_of_face].objects.filter(id=id)
        if db_row.exists():
            return db_row.first()
        return None
