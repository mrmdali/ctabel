from django.urls import path, include
from . import views

urlpatterns = [
    path('construction-list/', views.ConstructionListView.as_view()),
    path('construction-list-active/', views.ConstructionActiveListView.as_view()),
    path('construction-list-inactive/', views.ConstructionInactiveListView.as_view()),
    path('construction-create/', views.ConstructionCreateView.as_view()),
    path('construction-retrieve-update/<int:pk>/', views.ConstructionRetrieveUpdateView.as_view()),
    path('construction-inactivate/<int:pk>/', views.ConstructionInactivateView.as_view()),
    path('construction-activate/<int:pk>/', views.ConstructionActivateView.as_view()),
]