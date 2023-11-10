/**
 * This function returns the current date.
 * @returns {string} the current date. The date has the following format: dd/mm/yyyy_HH:MM.
 */
function getCurrentDate() {
    let today = new Date();

    let day = today.getDate();
    day = (day < 10 ? '0' + day : day);

    let month = today.getMonth() + 1;
    month = (month < 10 ? '0' + month : month);

    const year = today.getFullYear();

    let hour = today.getHours();
    hour = (hour < 10 ? '0' + hour : hour);

    let minutes = today.getMinutes();
    minutes = (minutes < 10 ? '0' + minutes : minutes);

    return day + '/' + month + '/' + year + '_' + hour + ':' + minutes;
}

/**
 * This function looks for an extension of the base64-encoded image('imgSrc').
 * The extension is contained in the prefix of the base64-encoded image.
 * @param {string} imgSrc - a base64-encoded image. The image must have a special prefix.
 * Here are some examples of the prefixes: 'data:image/png;base64,' ,
 *                                         'data:image/gif;base64,' ,
 *                                         'data:image/jpeg;base64,'
 * @returns {string} an extension of the passed image('imgSrc').
 */
function findFileExtension(imgSrc) {

    const startIndexOfFileExtension = imgSrc.indexOf("/") + 1;
    const endIndexOfFileExtension = imgSrc.indexOf(";");
    return imgSrc.slice(startIndexOfFileExtension, endIndexOfFileExtension);
}

/**
 * This function looks for MIME type (https://en.wikipedia.org/wiki/Media_type)
 * of the base64-encoded image('imgSrc').
 * The type is contained in the prefix of the base64-encoded image.
 * @param {string} imgSrc - a base64-encoded image. The image must have a special prefix.
 * Here are some examples of the prefixes: 'data:image/png;base64,' ,
 *                                         'data:image/gif;base64,' ,
 *                                         'data:image/jpeg;base64,'
 * @returns {string} MIME type of the passed image('imgSrc').
 */
function findMIMEtype(imgSrc) {
    const startIndexOfMIMEtype = imgSrc.indexOf(":") + 1;
    const endIndexOfMIMEtype = imgSrc.indexOf(";");
    return imgSrc.slice(startIndexOfMIMEtype, endIndexOfMIMEtype);
}

/**
 * This function enables to download the base64-encoded image('imgSrc').
 * @param {string} imgSrc - a base64-encoded image. The image must have a special prefix.
 * Here are some examples of the prefixes: 'data:image/png;base64,' ,
 *                                         'data:image/gif;base64,' ,
 *                                         'data:image/jpeg;base64,'
 * @param {string} nameOfAFile - a name that the downloaded image will have.
 * The name must end with an extension e.g. '.jpg', '.png'.
 */
function downloadPhoto(imgSrc, nameOfAFile) {
    const MIMEtype = findMIMEtype(imgSrc);
    download(imgSrc, nameOfAFile, MIMEtype);
}

/**
 * This function builds the data-* attribute.
 * @param {string} attribute_name - a name of an attribute
 * @param {string|null} attribute_value - a value of the attribute or null
 * @returns {string} the data-* attribute. The attribute has the following appearance:
 * [data-attribute_name] - if 'attribute_value' is null
 * [data-attribute_name=attribute_value] - if 'attribute_value' is not null
 */
function buildCustomData(attribute_name, attribute_value = null) {

    let data = "[" + DATA_PREFIX + attribute_name;
    if (attribute_value) {
        data += "=" + attribute_value;
    }
    data += "]";
    return data;
}

/**
 * This function sets the 'src' attribute of the <img> tag
 * assigned to the jQuery object '$img'.
 * @param {jQuery} $img - a jQuery object representing an image
 * @param {string} source - a value of the $img 'src' attribute
 */
function setImgSrc($img, source) {
    $img.attr('src', source);
}

/**
 * This function looks for the siblings(by using the jQuery method - https://api.jquery.com/siblings/)
 * of the passed jQuery object.
 * From these of the siblings, which have the class 'KEY_OF_THE_SHINING_OBJECT',
 * the class 'CLASS_OF_THE_BLOCKED_SHINING' is removed.
 * @param {jQuery} $obj - a jQuery object
 */
function unblockShiningOfSiblings($obj) {
    $obj.siblings().each(function () {
        const $this = $(this);
        if ($this.hasClass(KEY_OF_THE_SHINING_OBJECT)) {
            $this.removeClass(CLASS_OF_THE_BLOCKED_SHINING);
        }
    });
}

/**
 * This function looks for the siblings(by using the jQuery method - https://api.jquery.com/siblings/)
 * of the passed jQuery object.
 * To these of the siblings, which have the class 'KEY_OF_THE_SHINING_OBJECT',
 * the class 'CLASS_OF_THE_BLOCKED_SHINING' is added.
 * @param {jQuery} $obj - a jQuery object
 */
function blockShiningOfSiblings($obj) {
    $obj.siblings().each(function () {
        const $this = $(this);
        if ($this.hasClass(KEY_OF_THE_SHINING_OBJECT)) {
            $this.addClass(CLASS_OF_THE_BLOCKED_SHINING);
        }
    });
}