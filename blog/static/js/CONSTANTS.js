const LOAD_FACES_URL = "/load_faces/";
const PROCESS_PHOTO_URL = "/change_part_of_face/";

const PHOTO_PROCESSING = "YOUR PHOTO</br>IS BEING</br>PROCESSED";
const NO_FACES_DETECTED_ICON = "THERE ARE</br>NO FACES</br>ON THE PHOTO</br>PLEASE</br>CHOOSE</br>ANOTHER ONE";
const TOO_MANY_FACES_DETECTED_ICON = "THERE ARE</br>TOO MANY FACES</br>ON THE PHOTO</br>PLEASE</br>CHOOSE</br>ANOTHER ONE";
const ERROR_ICON = "AN ERROR</br>OCCURRED</br>PLEASE</br>TRY AGAIN";

const NO_USER_PHOTO_INFO = "You haven't chosen your photo.";
const EXAMPLE_FACE_NO_CHOSEN = "You haven't chosen partOfFace you want to have.";

const KEY_OF_A_PART_OF_THE_FACE = "part-of-face";
const KEY_OF_THE_INDEX_OF_A_PHOTO = "photoIndex";
const KEY_OF_THE_MODAL_WITH_THE_FACE_SWAPPING = "face-swapping-modal";
const KEY_OF_THE_FACE_ID = "face-id";
const KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO = "example-face";
const KEY_OF_THE_ZOOM_OBJECT = "zoom";
const KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT = "choose-part-of-face";
const KEY_OF_THE_SHINING_OBJECT = "shining";
const KEY_OF_THE_INDEX_OF_THE_ACTIVE_PART = "example-part-of-face";

const CLASS_OF_THE_BLOCKED_CHOOSE_BUTTON = "choose-button-block";
const CLASS_BLOCKING_THE_SCREEN = "disabled";
const CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE = "block-example-face-btn";
const CLASS_OF_THE_BLOCKED_SHINING = "hidden-shining";
const CLASS_OF_THE_CHOSEN_MODAL_OPTION = "chosen-modal-option";

const ACCEPTABLE_EXTENSIONS_OF_USER_PHOTO = ["png", "jpeg"];
const ACCEPTABLE_JS_EXTENSIONS_OF_USER_PHOTO = ACCEPTABLE_EXTENSIONS_OF_USER_PHOTO.map(extension => {
    return "image/" + extension
});
const INCORRECT_EXTENSION_OF_A_USER_PHOTO = "You have chosen an incorrect file. " +
    "The correct file should have one of the following extensions: " + ACCEPTABLE_EXTENSIONS_OF_USER_PHOTO.join(", ") + ".";

const DATA_PREFIX = "data-";

const NAME_OF_A_DOWNLOADED_FILE = "Daniel_Wardega_Face_Swapping";

