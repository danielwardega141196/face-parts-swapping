from .models import DB_OBJECTS, Photo


class DBFunc:
    @staticmethod
    def save_user_photo(
        photo_in_base64,
        number_of_detected_faces,
        rgb_array=None,
        face_landmarks=None,
        transparent_pixels=None,
    ):
        """
        This function saves user photos in the database table
        represented by 'Photo' object (from the file '.models').
        :param photo_in_base64: an RGB photo converted to base64
        :type photo_in_base64: string - str
        :param number_of_detected_faces: number of detected faces in the photo
        :type number_of_detected_faces: integer - int
        :param rgb_array: the same photo converted into a numpy array (the array has following shape(y, x, 3))
        :type rgb_array: numpy.ndarray (https://docs.scipy.org/doc/numpy/reference/generated/numpy.ndarray.html)
        :param face_landmarks: characteristic points for the specific parts of a face.
        A dictionary representing these points should come from calling
        the function 'get_landmarks_of_parts_of_face'
        (class 'ProcessUserPhoto' from the file './process_user_data/swap_elements_of_face.py').
        After all this dictionary must be converted to a string.
        :type face_landmarks: string - str
        :param transparent_pixels: list of dictionaries.
        Each of these dictionaries has the following keys: 'row_idx', 'column_idx', 'value'.
        The key 'row_idx' represent the index of a pixel's row (integer - int).
        The key 'column_idx' represent the index of a pixel's column (integer - int).
        The key 'value' represent the RGBA color of a pixel(list which contains four integers).
        This parameter should comes from calling the function 'prepare_transparent_pixels'
        (class 'ProcessUserPhoto' from the file './process_user_data/swap_elements_of_face.py').
        After all this list must be converted to a string.
        :type transparent_pixels: string - str
        """
        Photo.objects.create(
            photo_in_base64=photo_in_base64,
            rgb_array=rgb_array,
            transparent_pixels=transparent_pixels,
            number_of_detected_faces=number_of_detected_faces,
            face_landmarks=face_landmarks,
        )

    @staticmethod
    def get_user_photo_data(photo_in_base64):
        """
        :param photo_in_base64: a photo converted to base64
        :type photo_in_base64: string - str
        :return: an instance of the 'Photo' class (from the file '.models')
        representing the row containing the photo or
        None if the photo doesn't exist in the database.
        :rtype: an instance of the 'Photo' class (from the file '.models') or None
        """
        if DBFunc.user_photo_exists(photo_in_base64=photo_in_base64):
            return Photo.objects.get(photo_in_base64=photo_in_base64)
        return None

    @staticmethod
    def user_photo_exists(photo_in_base64):
        """
        This function checks if a photo(converted to base64) exists
        in the database table represented by the 'Photo' object (from the file '.models').
        :param photo_in_base64: a photo converted to base64
        :type photo_in_base64: string - str
        :return: True if the photo exists, False if not
        :rtype: bool (True or False)
        """
        return Photo.objects.filter(photo_in_base64=photo_in_base64).exists()

    @staticmethod
    def example_photo_exists(part_of_face, photo_name, photo_in_base64):
        """
        This function checks if a photo with the specified name('photo name'),
        converted to base64, exists in the database table indicated by the passed parameter 'part_of_face'.
        :param part_of_face: a specific part of the face
        This param must be a key of DB_OBJECTS dictionary (from the file '.models')
        whose values represent database tables.
        :type part_of_face: string - str
        :param photo_name: name of the photo
        :type photo_name: string - str
        :param photo_in_base64: a photo converted to base64
        :type photo_in_base64: string - str
        :return: True if the photo exists, False if not
        :rtype: bool (True or False)
        :raises ValueError: if the passed parameter 'part_of_face' is not a key of DB_OBJECTS dictionary
        """
        if part_of_face not in DB_OBJECTS:
            available_parts_of_face = ", ".join(
                map(lambda key: "'" + str(key) + "'", DB_OBJECTS.keys())
            )
            error_info = (
                "The provided part of the face ('{part_of_face}') "
                "is not available. "
                "Available parts of the face: "
                "{available_parts_of_face}.".format(
                    part_of_face=part_of_face,
                    available_parts_of_face=available_parts_of_face,
                )
            )
            raise ValueError(error_info)

        return (
            DB_OBJECTS[part_of_face]
            .objects.filter(photo_name=photo_name, photo_in_base64=photo_in_base64)
            .exists()
        )

    @staticmethod
    def save_example_photo(
        part_of_face, photo_name, photo_in_base64, rgb_array, face_landmarks
    ):
        """
        This function saves the photo, which concern a specific part of the face, into the appropriate database table.
        :param part_of_face: a specific part of the face
        This param must be a key of DB_OBJECTS dictionary (from the file '.models')
        whose values represent database tables.
        :type part_of_face: string - str
        :param photo_name: name of the photo
        :type photo_name: string - str
        :param photo_in_base64: a photo converted to base64
        :type photo_in_base64: string - str
        :param rgb_array: the same photo converted to an array with the shape (height x width x 3).
        This array must be converted to a string.
        :type rgb_array: string - str
        :param face_landmarks: characteristic points for the specific parts of a face.
        A dictionary representing these points should come from calling
        the function 'get_landmarks_of_parts_of_face'
        (class 'ProcessUserPhoto' from the file './process_user_data/swap_elements_of_face.py').
        After all this dictionary must be converted to a string.
        :type face_landmarks: string - str
        """
        if part_of_face not in DB_OBJECTS:
            available_parts_of_face = ", ".join(
                map(lambda key: "'" + str(key) + "'", DB_OBJECTS.keys())
            )
            error_info = (
                "The provided part of the face ('{part_of_face}') "
                "is not available. "
                "Available parts of the face: "
                "{available_parts_of_face}.".format(
                    part_of_face=part_of_face,
                    available_parts_of_face=available_parts_of_face,
                )
            )
            raise ValueError(error_info)

        DB_OBJECTS[part_of_face].objects.create(
            photo_name=photo_name,
            photo_in_base64=photo_in_base64,
            rgb_array=rgb_array,
            face_landmarks=face_landmarks,
        )

    @staticmethod
    def get_example_photo_data(part_of_face, row_id):
        """
        :param part_of_face: a specific part of the face
        This param must be a key of DB_OBJECTS dictionary (from the file '.models')
        whose values represent database tables.
        :type part_of_face: string - str
        :param row_id: id of a row in the database table.
        :type row_id: integer - int
        :return: object representing the row with the passed (as a parameter) id ('row_id') or None if
        a row with this id doesn't exist.
        :rtype: object representing a class which inherit from the class 'PartOfFace'(from the file '.models') or None
        :raises ValueError: if the passed parameter 'part_of_face' is not a key of DB_OBJECTS dictionary
        """
        if part_of_face not in DB_OBJECTS:
            available_parts_of_face = ", ".join(
                map(lambda key: "'" + str(key) + "'", DB_OBJECTS.keys())
            )
            error_info = (
                "The provided part of the face ('{part_of_face}') "
                "is not available. "
                "Available parts of the face: "
                "{available_parts_of_face}.".format(
                    part_of_face=part_of_face,
                    available_parts_of_face=available_parts_of_face,
                )
            )
            raise ValueError(error_info)

        db_row = DB_OBJECTS[part_of_face].objects.filter(id=row_id)
        if db_row.exists():
            return db_row.first()
        return None

    @staticmethod
    def get_all_photos_of_a_part_of_the_face(part_of_face):
        """
        :param part_of_face: a specific part of the face
        This param must be a key of DB_OBJECTS dictionary (from the file '.models')
        whose values represent database tables.
        :type part_of_face: string - str
        :return: list of all photos in the database table(indicated by the passed parameter 'part_of_face').
        The list consists of dictionaries.
        Each dictionary has the following fields: 'id', 'name', 'source'.
        :rtype: list - []
        :raises ValueError: if the passed parameter 'part_of_face' is not a key of DB_OBJECTS dictionary.
        """
        if part_of_face not in DB_OBJECTS:
            available_parts_of_face = ", ".join(
                map(lambda key: "'" + str(key) + "'", DB_OBJECTS.keys())
            )
            error_info = (
                "The provided part of the face ('{part_of_face}') "
                "is not available. "
                "Available parts of the face: "
                "{available_parts_of_face}.".format(
                    part_of_face=part_of_face,
                    available_parts_of_face=available_parts_of_face,
                )
            )
            raise ValueError(error_info)

        data = [
            {"id": row.id, "name": row.photo_name, "source": row.photo_in_base64}
            for row in DB_OBJECTS[part_of_face].objects.all()
        ]

        return data
