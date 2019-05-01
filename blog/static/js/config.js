/**
 * Variables representing jQuery objects.
 */
const $mainInput = $("#main-input");
const $mainForm = $("#data-form");

const $correctPhotoButton = $("[data-correct-photo]");
const $correctPhotoModal = $("[data-correct-photo-modal]");
const $closeCorrectPhotoModal = $("[data-close-correct-photo-modal]");

const $navbarActiveIcon = $("[data-navbar-active-icon]");
const $navbarInactiveIcon = $("[data-navbar-inactive-icon]");

const $exampleFaceModal = $("[data-example-face-modal]");
const $modalMainPhoto = $("[data-modal-main-photo]");
const $modalUpperOption = $("[data-modal-upper-option]");
const $modalLowerOption = $("[data-modal-lower-option]");
const $nextModalPhoto = $("[data-next-modal-photo]");
const $previousModalPhoto = $("[data-prev-modal-photo]");
const $modalChooseButton = $("[data-modal-choose-button]");
const $closeExampleFaceModal = $("[data-close-example-face-modal]");

const $descDuringPhotoProcessing = $("[data-proc-desc]");
const $transparentCarets = $("[data-transparent-caret]");

const $partOfFaceText = $("[data-part-of-face-text]");

const $buttonPartOfFace = $("[data-part-of-face]");
const $navButton = $("[data-nav-button]");
const $swapFacesButton = $("[data-swap]");
const $downloadPhotoButton = $("[data-download]");

const $nextFace = $("[data-next-face]");
const $previousFace = $("[data-prev-face]");
const $chosenPartOfFace = $("[data-chosen-example-face]");

const $exampleFacesDiv = $("[data-example-faces]");
const $userInputPhoto = $("[data-user-input-photo]");

/**
 * Global variables that won't be changed in code.
 */
const sourceOfExamplePartOfFace = $chosenPartOfFace.attr('src');
const startInputPhoto = $userInputPhoto.attr('src');

/**
 * Global variables that will be changed in code.
 */
let activePartOfFace = "lips";
let $acitveExampleFaces = $("[data-" + KEY_OF_THE_INDEX_OF_THE_ACTIVE_PART + "=" + activePartOfFace + "]");
let numberOfExampleFaces = $acitveExampleFaces.find("[data-" + KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO + "]").length / 2;

let activeExamplePhotoId;
let exampleFaceIndex = 0;

let downloadedPartsOfFace = {};

let abilityToChangePartOfFace = true;
let loadingPartOfFaceInProgress = false;
