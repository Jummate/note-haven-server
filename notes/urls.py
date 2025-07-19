from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.notes_view, name="notes"),
    path('<uuid:note_id>/', views.note_detail, name="note-detail"),
    path('<uuid:note_id>/archive', views.archive_note, name="archive-note"),
]