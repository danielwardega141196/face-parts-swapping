/**
 *  Code included inside this function will only run once
 *  when the page Document Object Model (DOM) is ready for JavaScript code to execute.
 */
$(document).ready(function () {
    loadPartOfFace($(buildCustomData(KEY_OF_A_PART_OF_THE_FACE, activePartOfFace)));
    $mainInput.attr('accept', ACCEPTABLE_JS_EXTENSIONS_OF_USER_PHOTO.join(","));
});

/**
 * When a user clicks on the button concerning the face swapping,
 * we will check if the face swapping is in progress.
 * If the face swapping is in progress nothing will happen.
 * Then we will check(by using the function 'smallDeviceModeActive' stored in this file)
 * if the small device mode is active.
 * If so, the website will be prepared in a slightly different way.
 * Then we will check(by using the function 'validateDataToSend' stored in this file)
 * if a user made all necessary activities. If so, the face swapping will start.
 */
$mainForm.submit(function (e) {
    e.preventDefault();

    if (!abilityToChangePartOfFace) {
        console.warn("The face swapping is being in progress.");
        return;
    }
    if (smallDeviceModeActive()) {
        chooseExamplePhoto();
        $(buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT)).removeClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
        $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, exampleFaceIndex)).find(buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT)).addClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
    }
    if (validateDataToSend()) {
        const swap = new swapPartOfFace();
        swap.processUserPhoto();
    }
});

/**
 * If a user choose a correct photo
 * (a file with the extension contained in the list 'ACCEPTABLE_JS_EXTENSIONS_OF_USER_PHOTO'),
 * this photo will be set as the chosen user photo ($userInputPhoto).
 * Otherwise, an alert message ('INCORRECT_EXTENSION_OF_A_USER_PHOTO') will be shown.
 */
$mainInput.change(function () {
    const reader = new FileReader();
    const fileData = $(this)[0].files[0];
    const fileExtension = fileData.type;
    if (ACCEPTABLE_JS_EXTENSIONS_OF_USER_PHOTO.includes(fileExtension)) {
        reader.readAsDataURL(fileData);
        reader.onload = function () {
            setImgSrc($userInputPhoto, reader.result);
            if (activeExamplePhotoId) {
                unblockShiningOfSiblings($swapFacesButton);
            }
        };
    } else {
        alert(INCORRECT_EXTENSION_OF_A_USER_PHOTO);
    }
});

/**
 * This function chooses an example photo from the photos regarding the active part of face.
 * @param {number|string} indexOfFace - the value of the key named 'example-face' in the dictionary
 * associated with every div containing a photo.
 */
function showSpecifiedPhoto(indexOfFace) {
    $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO)).hide();
    $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, indexOfFace.toString())).show();
}

/**
 * This function shows a part of the face represented by the jQuery object ($button).
 * @param {jQuery} $button - object representing a button
 * which enables to choose a part of the face.
 */
function loadPartOfFace($button) {
    if (loadingPartOfFaceInProgress) {
        console.warn("Chosen part of the face is being loaded.");
        return;
    }
    loadingPartOfFaceInProgress = true;
    const changePartOfFace = new ShowPartOfFace($button);
    $.when(changePartOfFace.loadFaces()).then(function () {
        loadingPartOfFaceInProgress = false;
    });
}

/**
 * If the global variable named 'numberOfExampleFaces' is gross than 2,
 * objects '$nextModalPhoto' and '$previousModalPhoto', which represent carets, will be shown.
 * Otherwise, the transparent versions of the carets ($transparentCarets) will be shown.
 */
function moreOrLessThanTwoExampleFaces() {
    if (numberOfExampleFaces > 2) {
        $nextModalPhoto.show();
        $previousModalPhoto.show();
        $transparentCarets.hide()
    } else {
        $nextModalPhoto.hide();
        $previousModalPhoto.hide();
        $transparentCarets.show();
    }
}

/**
 * This function will set the visible example photo
 * as the one containing a part of the face that user want to have.
 * Id of this photo will be assigned to the global variable 'activeExamplePhotoId'.
 */
function chooseExamplePhoto() {
    const $activeExampleFace = $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, exampleFaceIndex)).find(buildCustomData(KEY_OF_THE_FACE_ID));
    setImgSrc($chosenPartOfFace, $activeExampleFace.attr('src'));
    activeExamplePhotoId = $activeExampleFace.data(KEY_OF_THE_FACE_ID);
}

/**
 * This function checks if the small device mode is active.
 * @returns {boolean} true if the small device mode is active,false if not.
 */
function smallDeviceModeActive() {
    return $navbarActiveIcon.is(':visible') || $navbarInactiveIcon.is(':visible')
}

/**
 * This function checks if a user made all necessary activities to swap a part of the face.
 * If any activity has been omitted, a suitable message would be displayed.
 * @returns {boolean} true if all necessary activities have been done, false if not.
 */
function validateDataToSend() {
    const sourceOfTheUserInputPhoto = $userInputPhoto.attr("src");
    if (sourceOfTheUserInputPhoto === startInputPhoto) {
        alert(NO_USER_PHOTO_INFO);
        console.warn(NO_USER_PHOTO_INFO);
        return false;
    }
    if (!activeExamplePhotoId) {
        const warningMessage = EXAMPLE_FACE_NO_CHOSEN.replace('partOfFace', activePartOfFace);
        alert(warningMessage);
        console.warn(warningMessage);
        return false;
    }
    return true;
}

/**
 * This function will collapse the navigation bar in
 * if the small device mode is active.
 */
function collapseTheNavBar(){
    if ($navButton.is(':visible')) {
        if ($buttonPartOfFace.is(':visible')){
            $navButton.click();
        }
    }
}