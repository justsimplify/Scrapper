from django.urls import path

from . import views

urlpatterns = [
    path('<path:encoded_url>/<int:depth>', views.index),
]