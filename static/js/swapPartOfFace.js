/**
 * Class which enables to replace a part of the face
 * located on the inputted user photo by the same part of the face
 * located on the chosen example photo.
 */
class swapPartOfFace {
    /**
     * Create an instance of the 'swapPartOfFace' class.
     */
    constructor() {
        this.shiningElements = $exampleFaceModal;
    }

    /**
     * This function returns the value of the class variable 'this._shiningElements'.
     */
    get shiningElements() {
        return this._shiningElements;
    }

    /**
     * This function looks for 'the shining elements'
     * (the elements which have the assigned key 'KEY_OF_THE_SHINING_OBJECT')
     * and assigns them to the class variable 'this._shiningElements'.
     * @param {jQuery} $modal - jQuery object representing a modal
     * which may contain 'the shining elements' (the elements which have the assigned key 'KEY_OF_THE_SHINING_OBJECT')
     */
    set shiningElements($modal) {
        this._shiningElements = $modal.find("[data-" + KEY_OF_THE_SHINING_OBJECT + "]");
    }

    /**
     * This function makes all the shining elements,
     * assigned to the class variable 'this._shiningElements',
     * start shining.
     */
    showShiningElements() {
        this.shiningElements.removeClass(CLASS_OF_THE_BLOCKED_SHINING);
    }

    /**
     * This function makes all the shining elements,
     * assigned to the class variable 'this._shiningElements',
     * stop shining.
     */
    hideShiningElements() {
        this.shiningElements.addClass(CLASS_OF_THE_BLOCKED_SHINING);
    }

    /**
     * This function will prepare and  show the modal of the face swapping
     * and block the whole screen.
     */
    static startProcessingUserPhoto() {
        swapPartOfFace.prepareTheModal();
        swapPartOfFace.showTheModal();
        abilityToChangePartOfFace = false;
        $closeExampleFaceModal.hide();
        swapPartOfFace.blockTheScreen();
    }

    /**
     * This function will set the photo received from the backend('img_src') as the main modal photo($modalMainPhoto).
     * There will be also a possibility to download the photo.
     * @param {string} img_src - processed user photo converted to base64.
     */
    static prepareProcessedPhoto(img_src) {
        $descDuringPhotoProcessing.hide();
        setImgSrc($modalMainPhoto, img_src);
        $modalMainPhoto.show();
        $downloadPhotoButton.show();
    }

    /**
     * This function process the data received from the backend
     * according to the value of the key named 'face_detected_successfully' in the received dictionary('res').
     * @param {{face_detected_successfully: boolean, img_src: string, number_of_detected_faces: number}} res -
     * the dictionary received from the backend.
     */
    static processPositivelyBackendResponse(res) {
        if (res["face_detected_successfully"]) {
            swapPartOfFace.prepareProcessedPhoto(res["img_src"]);
        } else {
            swapPartOfFace.dealWithTheIncorrectNumberOfFaces(res["number_of_detected_faces"]);
        }
    }

    /**
     * This function enables to go through all the process regarding the face swapping.
     */
    processUserPhoto() {
        this.showShiningElements();
        swapPartOfFace.startProcessingUserPhoto();
        const thisTmp = this;

        $.ajax({
            url : PROCESS_PHOTO_URL,
            method : "post",
            dataType : "json",
            data : swapPartOfFace.getDataToSend(),
            timeout: TIMEOUT_OF_THE_PHOTO_PROCESSING
        }).done(function (res) {
            swapPartOfFace.processPositivelyBackendResponse(res);
        }).fail(function (msg) {
            $descDuringPhotoProcessing.html(ERROR_ICON);
            setTimeout(function(){window.location.reload();},
                        DELAY_OF_THE_PAGE_RELOADING);
        }).always(function () {
            abilityToChangePartOfFace = true;
            thisTmp.hideShiningElements();
            swapPartOfFace.unblockTheScreen();
            $closeExampleFaceModal.show();
        });
    }

    /**
     * This function enables to display a message regarding the incorrect number of faces.
     * @param {number} numberOfDetectedFaces - the number of detected faces on the user photo.
     */
    static dealWithTheIncorrectNumberOfFaces(numberOfDetectedFaces) {
        if (numberOfDetectedFaces < 1) {
            $descDuringPhotoProcessing.html(NO_FACES_DETECTED_ICON);
        } else if (numberOfDetectedFaces > 1) {
            $descDuringPhotoProcessing.html(TOO_MANY_FACES_DETECTED_ICON);
        }
    }

    /**
     * This function will prepare the modal of the face swapping.
     */
    static prepareTheModal() {
        setImgSrc($modalUpperOption, $userInputPhoto.attr('src'));
        $modalUpperOption.addClass(CLASS_OF_THE_CHOSEN_MODAL_OPTION);
        setImgSrc($modalLowerOption, $chosenPartOfFace.attr('src'));
        $modalLowerOption.addClass(CLASS_OF_THE_CHOSEN_MODAL_OPTION);
        $modalMainPhoto.hide();
        $downloadPhotoButton.hide();

        $descDuringPhotoProcessing.show();
        $descDuringPhotoProcessing.html(PHOTO_PROCESSING);

        $nextModalPhoto.hide();
        $previousModalPhoto.hide();
        $transparentCarets.hide();
        $modalChooseButton.hide();
    }

    /**
     * This function will show the modal of the face swapping.
     */
    static showTheModal() {
        $exampleFaceModal.modal('show');
        $exampleFaceModal.data(KEY_OF_THE_MODAL_WITH_THE_FACE_SWAPPING, true);
    }

    /**
     * This function completes the data to sent to the backend.
     * The value of the global variable 'activePartOfFace' will be assigned to the dictionary key 'activePartOfFace'.
     * The source of the user photo(the value of 'src' attribute of the global variable '$userInputPhoto') will be assigned to the dictionary key 'inputPhoto'.
     * The value of the global variable 'activeExamplePhotoId' will be assigned to the dictionary key 'faceId'.
     * @returns {{activePartOfFace: string, inputPhoto: string, faceId: number}} - a dictionary that should be sent to the backend
     */
    static getDataToSend() {
        return {
            "activePartOfFace": activePartOfFace,
            "inputPhoto": $userInputPhoto.attr("src"),
            "faceId": activeExamplePhotoId
        }
    }

    /**
     * This function blocks the whole screen. Clicks are ignored.
     */
    static blockTheScreen() {
        $('body').addClass(CLASS_BLOCKING_THE_SCREEN);
        $exampleFaceModal.addClass(CLASS_BLOCKING_THE_SCREEN);
    }

    /**
     * This function unblocks the screen. Clicks are acceptable.
     */
    static unblockTheScreen() {
        $('body').removeClass(CLASS_BLOCKING_THE_SCREEN);
        $exampleFaceModal.removeClass(CLASS_BLOCKING_THE_SCREEN);
    }
}