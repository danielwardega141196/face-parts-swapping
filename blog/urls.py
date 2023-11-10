from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    re_path(
        r'^change_part_of_face/$', views.change_part_of_face, name='change_part_of_face'
    ),
    re_path(r'^load_faces/$', views.load_faces, name='load_faces'),
]
