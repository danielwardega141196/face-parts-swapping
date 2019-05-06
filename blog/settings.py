from PIL import Image

from apps.face_element_swapping.endpoints import GetEndpointsOfANose, GetEndpointsOfLips

DESC_OF_PHOTO_IN_DB = "{id} | {date}"
DESC_OF_PART_OF_FACE_IN_DB = "{name} | {date}"
FORMAT_OF_DATE_IN_DB = "%d-%m-%Y %H:%M:%S"

DIRECTORIES_WITH_FACES = {
    "lips": "./blog/dev/lips",
    "nose": "./blog/dev/noses"
}

ACCEPTABLE_FILE_EXTENSIONS = (".jpg", ".jpeg")

SPECIAL_SIGNS_IN_FILE_NAMES = {
    "_space_": " ",
    ".jpg": "",
    ".jpeg": ""
}

LANDMARKS_FUNCTIONS = {
    "lips": GetEndpointsOfLips.get_endpoints_of_lips,
    "nose": GetEndpointsOfANose.get_endpoints_of_a_nose
}

MESSAGES_REGARDING_MORE_OR_LESS_THAN_ONE_FACE = {
    "face_detected_successfully": False,
    "number_of_detected_faces": None
}

MESSAGES_REGARDING_EXACTLY_ONE_FACE = {
    "face_detected_successfully": True,
    "number_of_detected_faces": 1,
    "img_src": None
}

DEFAULT_PIL_MODE = "RGB"
PIL_MODE_OF_TRANSPARENT_PHOTOS = "RGBA"

FILE_EXTENSIONS_ACCORDING_TO_PIL_MODES = {
    DEFAULT_PIL_MODE: "JPEG",
    PIL_MODE_OF_TRANSPARENT_PHOTOS: "PNG"
}

BASE64_PREFIXES_ACCORDING_TO_FILE_EXTENSIONS = {
    "JPEG": "data:image/jpeg;base64,",
    "PNG": "data:image/png;base64,"
}

MINIMUM_VALUE_OF_THE_ALPHA_CHANNEL = 100
CORRECT_NUMBER_OF_CHANNELS_PER_PIXEL = 4

INDEX_OF_THE_NUMBER_OF_CHANNELS_PER_PIXEL = 2

INDEX_OF_THE_VALUE_OF_ALPHA_CHANNEL = 3

PARTS_OF_THE_FACE_WITH_THE_CUT_FIELD = ["nose"]

REQUEST_METHOD_OF_THE_FACE_LOADING = "POST"
REQUEST_METHOD_OF_THE_FACE_SWAPPING = "POST"

KEY_OF_A_PART_OF_THE_FACE = 'partOfFace'
REQUIRED_KEYS_OF_THE_FACE_LOADING_REQUEST = [KEY_OF_A_PART_OF_THE_FACE]
KEY_OF_AN_INPUT_PHOTO = 'inputPhoto'
KEY_OF_THE_ACTIVE_PART_OF_THE_FACE = 'activePartOfFace'
KEY_OF_THE_FACE_ID = 'faceId'
REQUIRED_KEYS_OF_THE_FACE_SWAPPING_REQUEST = [KEY_OF_AN_INPUT_PHOTO,
                                              KEY_OF_THE_ACTIVE_PART_OF_THE_FACE,
                                              KEY_OF_THE_FACE_ID]

HTML_OF_THE_MAIN_PAGE = 'blog/post_list.html'

MAXIMUM_SIDE_LENGTH = 710
MAXIMUM_NUMBER_OF_PIXELS = MAXIMUM_SIDE_LENGTH * MAXIMUM_SIDE_LENGTH
DEFAULT_RESIZING_FILTER = Image.LANCZOS