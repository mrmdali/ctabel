from django.urls import path
from . import views

urlpatterns = [
    path('add-person/', views.AddPersonView.as_view())
]
