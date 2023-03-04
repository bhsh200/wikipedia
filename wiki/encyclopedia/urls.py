from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.title, name="title"),
    path("newpage",views.newPage,name="newpage"),
    path("wiki/<str:edit_name>/edit", views.editPage, name="editpage"),
    path("random", views.randomPage, name="randompage"),
    path("search", views.searchPage, name="search")
    ]
