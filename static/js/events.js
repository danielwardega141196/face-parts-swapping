/**
 *  When you click on the dynamically created HTML object (which has the assigned key KEY_OF_THE_ZOOM_OBJECT)
 *  the modal with the bigger faces, will be prepared and shown.
 */
$(document).on("click", buildCustomData(KEY_OF_THE_ZOOM_OBJECT), function () {

    moreOrLessThanTwoExampleFaces();
    $descDuringPhotoProcessing.hide();
    $modalMainPhoto.show();
    ModalOptions.uncheckAllModalOptions();
    $downloadPhotoButton.hide();
    $modalChooseButton.show();
    $closeExampleFaceModal.show();
    $exampleFaceModal.modal('show');
    $exampleFaceModal.data(KEY_OF_THE_MODAL_WITH_THE_FACE_SWAPPING, false);
    const $currentPhoto = $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, exampleFaceIndex)).find(buildCustomData(KEY_OF_THE_FACE_ID));
    ModalOptions.setAttrAndData($modalMainPhoto, $currentPhoto.attr('src'), exampleFaceIndex);
    ModalOptions.setAttrAndData($modalUpperOption, $currentPhoto.attr('src'), exampleFaceIndex);
    ModalOptions.distinguishModalOption($modalUpperOption);
    const nextPhotoIndex = (exampleFaceIndex + 1) % numberOfExampleFaces;
    const $nextPhoto = $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, nextPhotoIndex)).find(buildCustomData(KEY_OF_THE_FACE_ID));
    ModalOptions.setAttrAndData($modalLowerOption, $nextPhoto.attr('src'), nextPhotoIndex);
});

/**
 * When you click on the dynamically created HTML object (which has the assigned key 'KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT')
 * the visible example photo will be set as the one containing a part of the face that user want to have.
 * If any user photo had been inputted, there would be an opportunity to swap a part of the face.
 */
$(document).on("click", buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT), function () {
    chooseExamplePhoto();
    const sourceOfTheUserInputPhoto = $userInputPhoto.attr("src");
    if (sourceOfTheUserInputPhoto !== startInputPhoto) {
        unblockShiningOfSiblings($swapFacesButton);
    }
    $(buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT)).removeClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
    $(this).addClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
});

/**
 * When opening a modal, the current main page position is
 * assigned to the variable 'pagePosition' and the class 'CLASS_OF_AN_OPENED_MODAL'
 * is added to 'body'.
 */
$allModals.on('show.bs.modal', function (e) {
    const $body = $('body');
    pagePosition = $body.scrollTop();
    $body.addClass(CLASS_OF_AN_OPENED_MODAL);
});

/**
 * When closing a modal,
 * the class 'CLASS_OF_AN_OPENED_MODAL' is removed from 'body' and
 * the position of the main page is set to the value of the 'pagePosition' variable.
 */
$allModals.on('hidden.bs.modal', function () {
    const $body = $('body');
    $body.removeClass(CLASS_OF_AN_OPENED_MODAL);
    $body.animate({ scrollTop: pagePosition },
                  DELAY_OF_THE_COME_BACK_TO_THE_PREVIOUS_POSITION);
});

/**
 * When you click on '$correctPhotoButton',
 * the modal, which shows correct and incorrect photos, will be displayed.
 */
$correctPhotoButton.click(function () {
    $correctPhotoModal.modal('show');
});

/**
 * When you click on '$closeCorrectPhotoModal',
 * the modal, which shows correct and incorrect photos, will be hidden.
 */
$closeCorrectPhotoModal.click(function () {
    $correctPhotoModal.modal('hide');
});

/**
 * When you click on '$closeExampleFaceModal',
 * the modal with the bigger faces, will be hidden.
 */
$closeExampleFaceModal.click(function () {
    $exampleFaceModal.modal('hide');
});

/**
 * When you click on '$buttonPartOfFace',
 * an another part of the face will be available.
 */
$buttonPartOfFace.click(function () {
    loadPartOfFace($(this));
});

/**
 * When you click on '$nextModalPhoto',
 * '$modalLowerOption' will become '$modalUpperOption'
 * and an another photo of the available part of the face will be loaded into '$modalLowerOption'.
 */
$nextModalPhoto.click(function () {
    ModalOptions.uncheckAllModalOptions();
    const currentPhotoIndex = $modalLowerOption.data(KEY_OF_THE_INDEX_OF_A_PHOTO);
    ModalOptions.setAttrAndData($modalUpperOption, $modalLowerOption.attr('src'), currentPhotoIndex);
    const choosenModalPhotoIndex = $modalMainPhoto.data(KEY_OF_THE_INDEX_OF_A_PHOTO);
    if (currentPhotoIndex === choosenModalPhotoIndex) {
        ModalOptions.distinguishModalOption($modalUpperOption);
    }
    const nextPhotoIndex = (currentPhotoIndex + 1) % numberOfExampleFaces;
    const $nextPhoto = $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, nextPhotoIndex)).find(buildCustomData(KEY_OF_THE_FACE_ID));
    ModalOptions.setAttrAndData($modalLowerOption, $nextPhoto.attr('src'), nextPhotoIndex);
    if (nextPhotoIndex === choosenModalPhotoIndex) {
        ModalOptions.distinguishModalOption($modalLowerOption);
    }
});

/**
 * When you click on '$previousModalPhoto',
 * '$modalUpperOption' will become '$modalLowerOption'
 * and an another photo of the available part of the face will be loaded into '$modalUpperOption'.
 */
$previousModalPhoto.click(function () {
    ModalOptions.uncheckAllModalOptions();
    const currentPhotoIndex = $modalUpperOption.data(KEY_OF_THE_INDEX_OF_A_PHOTO);
    ModalOptions.setAttrAndData($modalLowerOption, $modalUpperOption.attr('src'), currentPhotoIndex);
    const choosenModalPhotoIndex = $modalMainPhoto.data(KEY_OF_THE_INDEX_OF_A_PHOTO);
    if (currentPhotoIndex === choosenModalPhotoIndex) {
        ModalOptions.distinguishModalOption($modalLowerOption);
    }
    const previousPhotoIndex = (numberOfExampleFaces + (currentPhotoIndex - 1)) % numberOfExampleFaces;
    const $previousPhoto = $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, previousPhotoIndex)).find(buildCustomData(KEY_OF_THE_FACE_ID));
    ModalOptions.setAttrAndData($modalUpperOption, $previousPhoto.attr('src'), previousPhotoIndex);
    if (previousPhotoIndex === choosenModalPhotoIndex) {
        ModalOptions.distinguishModalOption($modalUpperOption);
    }
});

/**
 * When you click on '$modalUpperOption'
 * and '$exampleFaceModal' shows the bigger versions of example photos,
 * $modalUpperOption will be distinguished(by using the method named 'distinguishModalOption' from the class 'ModalPhotos')
 * and its source and index will be assigned to $modalMainPhoto
 * (by using the method named 'setAttrAndData' from the class 'ModalOptions').
 */
$modalUpperOption.click(function () {

    if (!$exampleFaceModal.data(KEY_OF_THE_MODAL_WITH_THE_FACE_SWAPPING)) {
        ModalOptions.uncheckAllModalOptions();
        ModalOptions.distinguishModalOption($modalUpperOption);
        ModalOptions.setAttrAndData($modalMainPhoto, $(this).attr('src'), $(this).data(KEY_OF_THE_INDEX_OF_A_PHOTO));
    }
});

/**
 * When you click on '$modalLowerOption'
 * and '$exampleFaceModal' shows the bigger versions of example photos,
 * $modalLowerOption will be distinguished(by using the method named 'distinguishModalOption' from the class 'ModalOptions')
 * and its source and index will be assigned to $modalMainPhoto
 * (by using the method named 'setAttrAndData' from the class 'ModalOptions').
 */
$modalLowerOption.click(function () {
    if (!$exampleFaceModal.data(KEY_OF_THE_MODAL_WITH_THE_FACE_SWAPPING)) {
        ModalOptions.uncheckAllModalOptions();
        ModalOptions.distinguishModalOption($modalLowerOption);
        ModalOptions.setAttrAndData($modalMainPhoto, $(this).attr('src'), $(this).data(KEY_OF_THE_INDEX_OF_A_PHOTO));
    }
});

/**
 * When you click on '$modalChooseButton'
 * the main modal ($modalMainPhoto) photo will be visible on the main page.
 * It will be also chosen as the one containing a part of the face that user want to have.
 * The modal ($exampleFaceModal), which shows the bigger versions of example photos, will be hidden.
 * If any user photo had been inputted, there would be an opportunity to swap a part of the face.
 */
$modalChooseButton.click(function () {
    exampleFaceIndex = $modalMainPhoto.data(KEY_OF_THE_INDEX_OF_A_PHOTO);
    showSpecifiedPhoto(exampleFaceIndex);
    $(buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT)).removeClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
    $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO, exampleFaceIndex.toString())).find(buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT)).addClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
    chooseExamplePhoto();
    const sourceOfTheUserInputPhoto = $userInputPhoto.attr("src");
    if (sourceOfTheUserInputPhoto !== startInputPhoto) {
        unblockShiningOfSiblings($swapFacesButton);
    }
    $exampleFaceModal.modal('hide');
});

/**
 * When you click on '$nextFace',
 * the next photo of the available part of the face will be visible on the main page.
 */
$nextFace.click(function () {
    exampleFaceIndex = (exampleFaceIndex + 1) % numberOfExampleFaces;
    showSpecifiedPhoto(exampleFaceIndex);
    this.blur();
});

/**
 * When you click right mouse button on '$nextFace'
 * the appearance of this element won't change.
 */
$nextFace.contextmenu(function () {
    this.blur();
});


/**
 * When you click on '$nextFace',
 * the previous photo of the available part of the face will be visible on the main page.
 */
$previousFace.click(function () {
    exampleFaceIndex = (numberOfExampleFaces + (exampleFaceIndex - 1)) % numberOfExampleFaces;
    showSpecifiedPhoto(exampleFaceIndex);
    this.blur();
});

/**
 * When you click right mouse button on '$previousFace'
 * the appearance of this element won't change.
 */
$previousFace.contextmenu(function () {
    this.blur();
});


/**
 * When you click on '$downloadPhotoButton',
 * the main modal ('$modalMainPhoto') photo will be downloaded.
 */
$downloadPhotoButton.click(function () {
    const imgSrc = $modalMainPhoto.attr('src');
    const nameOfAFile = NAME_OF_A_DOWNLOADED_FILE + "_" + getCurrentDate() + "." + findFileExtension(imgSrc);
    downloadPhoto(imgSrc, nameOfAFile);
});

/**
 * When you click on '$navButton' an another version of the navbar icon will be visible.
 */
$navButton.click(function () {
    if ($buttonPartOfFace.is(':visible')) {
        $(this).css("background-color", "black");
        $navbarActiveIcon.show();
        $navbarInactiveIcon.hide();
    } else {
        $(this).css("background-color", "white");
        $navbarActiveIcon.hide();
        $navbarInactiveIcon.show();
    }
});