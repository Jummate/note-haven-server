from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.tags_view, name="tags"),
]