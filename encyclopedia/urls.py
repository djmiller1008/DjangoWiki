from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry_name>", views.entry, name="entry"),
    path("search_results", views.search_results, name="search_results"),
    path("new", views.new, name="new"),
    path("edit/<str:entry_title>", views.edit, name="edit")
]
