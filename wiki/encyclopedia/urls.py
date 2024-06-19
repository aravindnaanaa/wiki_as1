from django.urls import path

from . import views
app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("New", views.newpage, name="newpage"),
    path("random", views.random_page, name="randompage"),
    path("edit/<str:name>", views.edit, name="edit"),
    path("<str:name>", views.cpages, name="callme"),
    
    
]
