from django.db import models
from django.utils import timezone

from .settings import DESC_OF_PHOTO_IN_DB, \
    FORMAT_OF_DATE_IN_DB


class Photo(models.Model):
    """
         Database table responsible for storing user input photos.
         This table has the following columns:

            id - unique row key (generated automatically)
            :type id: int

            photo_in_base64 - user photo which was converted to base64
            :type photo_in_base64: string

            rgb_array - user photo converted to array with shape [height x width x 3].
                        This array contains RGB values and was converted to string via json.
            :type rgb_array: string

            number_of_detected_faces - number of faces on user photo
            :type number_of_detected_faces: int

            face_landmarks - dictionary of characteristic points of the specific parts of the face
                             The dictionary was converted to string via json.
            :type face_landmarks: string

            timestamp -  date of the entry of photo into the database
            :type timestamp: class named 'datetime' from library named 'datetime'
    """

    id = models.AutoField(primary_key=True, unique=True)
    photo_in_base64 = models.TextField()

    rgb_array = models.TextField(default=None,
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
