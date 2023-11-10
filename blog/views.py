from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .db_func import DBFunc
from .process_user_data import ProcessUserPhoto
from .settings import (
    HTML_OF_THE_MAIN_PAGE,
    KEY_OF_A_PART_OF_THE_FACE,
    KEY_OF_AN_INPUT_PHOTO,
    KEY_OF_THE_ACTIVE_PART_OF_THE_FACE,
    KEY_OF_THE_FACE_ID,
    REQUEST_METHOD_OF_THE_FACE_LOADING,
    REQUEST_METHOD_OF_THE_FACE_SWAPPING,
    REQUIRED_KEYS_OF_THE_FACE_LOADING_REQUEST,
    REQUIRED_KEYS_OF_THE_FACE_SWAPPING_REQUEST,
)


def post_list(request):
    """
    This function renders the initial view of the page.
    :param request: a http requests from the FrontEnd.
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: a http response made on the basis of the html page
    (indicated by the 'HTML_OF_THE_MAIN_PAGE' variable)
    :rtype: django.http.response.HttpResponse
    """

    return render(request, HTML_OF_THE_MAIN_PAGE)


@api_view([REQUEST_METHOD_OF_THE_FACE_LOADING])
@method_decorator(csrf_exempt, name='dispatch')
def load_faces(request):
    """
    This handler looks for the data of
    all photos concerning the specific part of the face,
    The name of this part of the face should be contained in the request.
    :param request: a http requests from the FrontEnd.
    The correct request should contain all the keys from
    the 'REQUIRED_KEYS_OF_THE_FACE_LOADING_REQUEST' list.
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: dictionary where the list, which contains the data of
    all photos concerning the specific part of the face, is
    assigned to the key named 'example_faces'.
    :rtype: dictionary converted into a JSON object (type - django.http.response.JsonResponse)
    :raises ValueError: if the request doesn't contain a key
    from the 'REQUIRED_KEYS_OF_THE_FACE_LOADING_REQUEST' list.
    """

    for required_key in REQUIRED_KEYS_OF_THE_FACE_LOADING_REQUEST:
        if required_key not in request.POST:
            raise ValueError(
                "The required key '{required_key}' "
                "is not contained in the request.".format(required_key=required_key)
            )

    part_of_face = request.POST.get(KEY_OF_A_PART_OF_THE_FACE)
    example_faces = DBFunc.get_all_photos_of_a_part_of_the_face(
        part_of_face=part_of_face
    )
    data = {"example_faces": example_faces}
    return JsonResponse(data)


@api_view([REQUEST_METHOD_OF_THE_FACE_SWAPPING])
@method_decorator(csrf_exempt, name='dispatch')
def change_part_of_face(request):
    """
    :param request: a http requests from the FrontEnd.
    The correct request should contain all the keys from
    the 'REQUIRED_KEYS_OF_THE_FACE_SWAPPING_REQUEST' list.
    :type request: django.core.handlers.wsgi.WSGIRequest
    :return: result of calling the function 'process_user_photo'
    (class 'ProcessUserPhoto' from the file './process_user_data/swap_elements_of_face.py').
    :rtype: dictionary converted into a JSON object (type - django.http.response.JsonResponse)
    :raises ValueError: if the request doesn't contain a key
    from the 'REQUIRED_KEYS_OF_THE_FACE_SWAPPING_REQUEST' list.
    """

    for required_key in REQUIRED_KEYS_OF_THE_FACE_SWAPPING_REQUEST:
        if required_key not in request.POST:
            raise ValueError(
                "The required key '{required_key}' "
                "is not contained in the request.".format(required_key=required_key)
            )

    input_photo = request.POST.get(KEY_OF_AN_INPUT_PHOTO)
    part_of_face = request.POST.get(KEY_OF_THE_ACTIVE_PART_OF_THE_FACE)
    face_id = request.POST.get(KEY_OF_THE_FACE_ID)

    return ProcessUserPhoto.process_user_photo(
        input_photo=input_photo, part_of_face=part_of_face, face_id=face_id
    )
