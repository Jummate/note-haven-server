from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.notes_view, name="notes"),
    path('<int:note_id>/', views.note_detail, name="note-detail"),
]