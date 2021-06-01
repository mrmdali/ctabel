from django.urls import path
from . import views

urlpatterns = [
    path('position-list/', views.PositionListView.as_view(), name='position-list'),
    path('position-inactive-list/', views.PositionInactiveListView.as_view(), name='position-inactive-list'),
    path('position-create/', views.PositionCreateView.as_view(), name='position-create'),
    path('position-retrieve-update/<int:pk>/', views.PositionRetrieveUpdateView.as_view(),
         name='position-retrieve-update'),
    path('position-delete/<int:pk>/', views.PositionDeleteView.as_view(),
         name='position-delete'),
    path('position-activate/<int:pk>/', views.PositionActivateView.as_view(),
         name='position-activate'),
]