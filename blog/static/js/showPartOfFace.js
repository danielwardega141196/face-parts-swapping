/** Class which enables to show a part of the face chosen by user. */
class ShowPartOfFace {
    /**
     * Create an instance of the 'ShowPartOfFace' class.
     * @param {jQuery} $partOfFaceButton - object representing a button
     * which enables to choose a part of the face.
     */
    constructor($partOfFaceButton) {

        this.button = $partOfFaceButton;
        this.partOfFace = $partOfFaceButton;

    }

    /**
     * This function returns the value of the class variable 'this._partOfFace'.
     */
    get partOfFace() {
        return this._partOfFace;
    }

    /**
     * This function assigns the value for the key 'KEY_OF_A_PART_OF_THE_FACE'
     * (the dictionary associated with the '$partOfFaceButton' object)
     * to the class variable 'this._partOfFace'(by using the jQuery method named 'data'
     * https://api.jquery.com/data/)
     * @param {jQuery} $partOfFaceButton - jQuery object representing a button
     * which enables to choose a part of the face.
     */
    set partOfFace($partOfFaceButton) {
        this._partOfFace = $partOfFaceButton.data(KEY_OF_A_PART_OF_THE_FACE);
    }

    /**
     * This function downloads photos of a specified part of the face and if the download is successful,
     * the photos will be loaded into HTML.
     * @param {string} partOfFace - a specific part of the face
     * @returns {boolean} true if the photos have been successfully downloaded and loaded,
     * false if an error has occurred.
     */
    static downloadExampleFaces(partOfFace) {
        let downloadSuccessful;

        $.ajax({
            url: LOAD_FACES_URL,
            method : "post",
            async: false,
            dataType : "json",
            data: {"partOfFace": partOfFace},
        }).done(function (res) {
            const divWithExampleFaces = ShowPartOfFace.createDivWithExampleFaces(partOfFace, res["example_faces"]);
            $exampleFacesDiv.append(divWithExampleFaces);
            downloadedPartsOfFace[partOfFace] = true;
            console.log("Example faces have been successfully downloaded.");
            downloadSuccessful = true;
        }).fail(function (msg) {
            console.warn("During downloading example faces an error occured.");
            console.warn("Type of error: ", jqXHR);
            console.warn("Status: ", textStatus);
            console.warn("Error:", errorThrown);
            downloadSuccessful = false;
        });
        return downloadSuccessful;
    }

    /**
     * This function will make that all the elements related to
     * the part of the face assigned to the class variable 'this._partOfFace'
     * will be visible on the main page.
     */
    setActivePartOfFace() {
        activePartOfFace = this.partOfFace;
        $acitveExampleFaces.hide();
        $acitveExampleFaces = $(buildCustomData(KEY_OF_THE_INDEX_OF_THE_ACTIVE_PART, activePartOfFace));
        $acitveExampleFaces.show();
        numberOfExampleFaces = $acitveExampleFaces.find(buildCustomData(KEY_OF_THE_INDEX_OF_AN_EXAMPLE_PHOTO)).length / 2;
        $buttonPartOfFace.removeClass(CLASS_OF_THE_BLOCKED_CHOOSE_BUTTON);
        this.button.addClass(CLASS_OF_THE_BLOCKED_CHOOSE_BUTTON);
        exampleFaceIndex = 0;
        showSpecifiedPhoto(exampleFaceIndex);
        activeExamplePhotoId = null;
        blockShiningOfSiblings($swapFacesButton);
        $chosenPartOfFace.attr('src', sourceOfExamplePartOfFace);
        $partOfFaceText.text(activePartOfFace);
        collapseTheNavBar();
        $(buildCustomData(KEY_OF_THE_CHOOSE_PART_OF_FACE_OBJECT)).removeClass(CLASS_OF_THE_BUTTON_WITH_BLOCKED_EXAMPLE_FACE);
    }

    /**
     * This function will download and load all the elements related to
     * the part of the face assigned to the class variable 'this._partOfFace'.
     * These elements will be visible on the main page.
     * @returns {boolean} true if all the elements have been positively loaded,
     * false if an error has occurred during the download
     */
    loadFaces() {
        var downloadSuccessful = true;
        if (!downloadedPartsOfFace[this.partOfFace]) {
            downloadSuccessful = ShowPartOfFace.downloadExampleFaces(this.partOfFace);
        } else {
            this.setActivePartOfFace();
            return true;
        }
        if (downloadSuccessful) {
            this.setActivePartOfFace();
            return true;
        }
        return false;
    }

    /**
     * This function builds HTML of the 'div' which contains photos and details
     * concerning the passed part of the face (partOfFace).
     * @param {string} partOfFace - a specific part of the face
     * @typedef {{id:number, name:string, source:string}} exampleFace - dictionary
     * containing an example photo concerning the passed part of the face(partOfFace).
     * Each of the dictionaries should have the following keys:
     * id - id of a row, which contains the photo, in the database table of
     * the passed part of the face (partOfFace).
     * name - name of the photo
     * source - the photo converted to base64
     * @param {Array.<exampleFace>} exampleFacesData - list of the 'exampleFace' dictionaries.
     * @returns {string} div containing photos and details
     * of the passed part of the face (partOfFace).
     */
    static createDivWithExampleFaces(partOfFace, exampleFacesData) {
        var divData = '<div data-example-part-of-face="' + partOfFace + '">';
        for (var i in exampleFacesData) {
            var photoData = exampleFacesData[i];
            divData += '<div class="d-md-block d-sm-none d-none">';
            if (i == 0) {
                divData += '<div data-example-face=' + i + ' class="row w-100 justify-content-md-around" style="margin: 0;">';
            } else {
                divData += '<div data-example-face=' + i + ' class="row w-100 justify-content-md-around" style="margin: 0; display: none;">';
            }
            divData += '<div class="col-md-12" style="margin-top: 1%;">' +
                            '<div class="row justify-content-md-center padding-0-1">' +
                                '<div class="col-md-4" style="margin-right: 3%;">' +
                                    '<div class="row justify-content-md-around">' +
                                        '<div class="col-md-12 d-md-flex align-items-md-center justify-content-md-center" style="height: 250px;">' +
                                            '<img data-face-id=' + photoData["id"] + ' class="rounded-circle" src="' + photoData["source"] + '">' +
                                        '</div>' +
                                    '</div>' +
                                '</div>' +
                                '<div data-example-photo-options class="col-md-4 d-flex align-items-center justify-content-md-center row" style="margin-left: 3%;">' +
                                    '<p data-example-photo-name class="col-md-11" >' + photoData["name"] + '</p>' +
                                    '<button data-zoom class="col-md-11 example-face-btns-md btn btn-outline-dark">ZOOM IN </button>' +
                                    '<button data-choose-part-of-face class="col-md-11 example-face-btns-md btn btn-outline-dark" >CHOOSE </button>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                '</div>';
            divData += '<div class="d-md-none d-sm-block d-block">';
            if (i == 0) {
                divData += '<div data-example-face=' + i + ' class="row w-100 justify-content-sm-around justify-content-around" style="margin: 0;">';
            } else {
                divData += '<div data-example-face=' + i + ' class="row w-100 justify-content-sm-around justify-content-around" style="margin: 0; display: none;">';
            }
            divData += '<div class="col-sm-12 col-12">' +
                            '<div class="row justify-content-around">' +
                                '<div data-part-of-face-text class="col-sm-12 col-12 main-font-sm center-hori-vert" style="margin-top: 3%;color: white">' +
                                    partOfFace +
                                '</div>' +
                                '<div data-want-to-have class="col-sm-12 col-12 btn btn-outline-dark main-font-sm disabled" style="margin-bottom: 1px;">' +
                                        'YOU WANT TO' +
                                '</div>' +
                            '</div>' +
                        '</div>';
            divData += '<div class="col-sm-12 col-12">' +
                            '<div class="row justify-content-sm-around justify-content-around">' +
                                '<div class="col-sm-11 col-11 ' +
                                            'd-sm-flex d-flex ' +
                                            'align-items-sm-center align-items-center ' +
                                            'justify-content-sm-center justify-content-center" style="height: 235px;">' +
                                    '<img data-face-id=' + photoData["id"] + ' class="rounded-circle" src="' + photoData["source"] + '">' +
                                '</div>' +
                                '<p data-example-photo-name class="col-sm-12 col-12" style="margin-top: 5%;">' + photoData["name"] + '</p>' +
                                '<button data-zoom class="col-sm-10 col-10 btn btn-outline-dark example-face-btns-sm font-sm" style="margin-bottom: 2%;">ZOOM IN</button>' +
                            '</div>' +
                        '</div>' +
                '</div>' +
            '</div>';
        }
        return divData;
    }
}
