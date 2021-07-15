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

    path('object-list/', views.ObjectListView.as_view()),
    path('object-list-active/', views.ObjectActiveListView.as_view()),
    path('object-list-inactive/', views.ObjectInactiveListView.as_view()),
    path('object-create/', views.ObjectCreateView.as_view()),
    path('object-retrieve-update/<int:pk>/', views.ObjectRetrieveUpdateView.as_view()),
    path('object-inactivate/<int:pk>/', views.ObjectInactivateView.as_view()),
    path('object-activate/<int:pk>/', views.ObjectActivateView.as_view()),
]