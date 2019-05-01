/**
 * Class which determines the behaviour, appearance and details of the modal options.
 * Currently, the modal options are: '$modalUpperOption' and '$modalLowerOption'.
 */
class ModalOptions {

    /**
     * This function unchecks all modal options.
     * None of them looks as the chosen one.
     * Currently, the modal options are: '$modalUpperOption' and '$modalLowerOption'.
     */
    static uncheckAllModalOptions() {
        $modalUpperOption.removeClass(CLASS_OF_THE_CHOSEN_MODAL_OPTION);
        blockShiningOfSiblings($modalUpperOption);
        $modalLowerOption.removeClass(CLASS_OF_THE_CHOSEN_MODAL_OPTION);
        blockShiningOfSiblings($modalLowerOption);
    }

    /**
     * This function distinguishes the passed modal option '$modalOption'.
     * This option looks as the chosen one.
     * @param {jQuery} $modalOption - jQuery object representing a modal option
     */
    static distinguishModalOption($modalOption) {
        $modalOption.addClass(CLASS_OF_THE_CHOSEN_MODAL_OPTION);
        unblockShiningOfSiblings($modalOption);
    }

    /**
     * This function assigns 'photoIndex'(passed as a parameter)
     * as the value for the key 'KEY_OF_THE_INDEX_OF_A_PHOTO'
     * (the dictionary associated with the '$modalOption' object).
     * @param {jQuery} $modalOption - jQuery object representing a modal option
     * @param {number} photoIndex - an integer representing the value of the key 'KEY_OF_THE_INDEX_OF_A_PHOTO'
     * in the dictionary associated with the '$modalOption' object.
     */
    static setIndexOfModalOption($modalOption, photoIndex) {
        $modalOption.data(KEY_OF_THE_INDEX_OF_A_PHOTO, photoIndex);
    }

    /**
     * This function sets the index('photoIndex') and the source('source')
     * of the photo assigned to '$modalOption'.
     * @param {jQuery} $modalOption - jQuery object representing a modal option
     * @param {string} source - a value of the 'src' attribute in the photo assigned to '$modalOption'.
     * @param {number} photoIndex - an integer representing the value of the key 'KEY_OF_THE_INDEX_OF_A_PHOTO'
     * in the dictionary associated with the '$modalOption' object.
     */
    static setAttrAndData($modalOption, source, photoIndex) {
        ModalOptions.setIndexOfModalOption($modalOption, photoIndex);
        setImgSrc($modalOption, source);
    }
}