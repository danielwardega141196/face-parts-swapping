from django.db import models
from django.utils import timezone

from .settings import DESC_OF_PHOTO_IN_DB, \
    FORMAT_OF_DATE_IN_DB, \
    DESC_OF_PART_OF_FACE_IN_DB


class Photo(models.Model):
    """
         Database table responsible for storing user input photos.
         This table has the following columns:

            id - unique row key (generated automatically)
            :type id: int

            photo_in_base64 - user photo which was converted to base64
            :type photo_in_base64: string

            rgb_array - user photo converted into an nested Python list with the shape (height x width x 3).
            This array should contain RGB values and must be converted to a string.
            :type rgb_array: string

            transparent_pixels: list of dictionaries.
            Each of these dictionaries has the following keys: 'row_idx', 'column_idx', 'value'.
            The list must be converted to a string.
            :type transparent_pixels: string

            number_of_detected_faces: number of detected faces in the user photo
            :type number_of_detected_faces: integer - int

            face_landmarks - dictionary of characteristic points of the specific parts of the face.
                             The dictionary must be converted to a string.
            :type face_landmarks: string

            timestamp - date of entry of the photo into the database.
            :type timestamp: class named 'datetime' from the library named 'datetime'.
    """

    id = models.AutoField(primary_key=True, unique=True)
    photo_in_base64 = models.TextField()
    rgb_array = models.TextField(default=None,
                                 blank=True,
                                 null=True)
    transparent_pixels = models.TextField(default=None,
                                          blank=True,
                                          null=True)
    number_of_detected_faces = models.IntegerField()
    face_landmarks = models.TextField(default=None,
                                      blank=True,
                                      null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return DESC_OF_PHOTO_IN_DB.format(id=self.id,
                                          date=self.timestamp.strftime(FORMAT_OF_DATE_IN_DB))


class PartOfFace(models.Model):
    """
         Database table responsible for storing photos concerning the specific part of the face.
         This table has the following columns:

            id - unique row key (generated automatically)
            :type id: int

            photo_name - name of the photo
            :type photo_name: string with maximum length of 50 signs

            photo_in_base64 - the photo converted to base64
            :type photo_in_base64: string

            rgb_array - the photo converted into an nested Python list with the shape (height x width x 3).
            This array contains RGB values and was converted to a string.
            :type rgb_array: string

            face_landmarks - dictionary of characteristic points of the specific parts of the face
                             The dictionary was converted to a string.
            :type face_landmarks: string

            timestamp - date of entry of the photo into the database.
            :type timestamp: class named 'datetime' from the library named 'datetime'.
    """
    id = models.AutoField(primary_key=True, unique=True)
    photo_name = models.CharField(max_length=100)
    photo_in_base64 = models.TextField()
    rgb_array = models.TextField()
    face_landmarks = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return DESC_OF_PART_OF_FACE_IN_DB.format(name=self.photo_name,
                                                 date=self.timestamp.strftime(FORMAT_OF_DATE_IN_DB))


class ExampleLip(PartOfFace):
    """
        Database table responsible for storing photos concerning lips.
    """
    pass


class ExampleNose(PartOfFace):
    """
        Database table responsible for storing photos concerning noses.
    """
    pass


DB_OBJECTS = {
    "lips": ExampleLip,
    "nose": ExampleNose
}
