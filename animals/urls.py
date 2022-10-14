from django.urls import path

from .views import AnimalView, AnimalDetailView

urlpatterns = [
    path("animals/", AnimalView.as_view()),
    path("animals/<int:animal_id>/", AnimalDetailView.as_view()),
]
