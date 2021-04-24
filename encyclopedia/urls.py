from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.view_page, name="viewpage"),
    path("searchpages", views.searchpages, name="searchpages"),
    path("newpage", views.new_page, name="newpage"),
    path("editpage/<str:page_title>", views.edit_page, name="editpage"),
    path("random", views.random_page, name="random")
]
