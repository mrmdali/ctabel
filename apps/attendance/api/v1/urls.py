from django.urls import path
from . import views

urlpatterns = [
    path('working-hour-list/', views.WorkingHourListView.as_view()),
    path('working-hour-create/', views.WorkingHourCreateView.as_view()),
    path('working-hour-rud/<int:pk>/', views.WorkingHourRUDView.as_view()),
    path('attendance-list-create/', views.AttendanceListCreateView.as_view()),
    path('attendance-rud/<int:pk>/', views.AttendanceRUDView.as_view()),
    path('reason-list/', views.ReasonListView.as_view()),
    path('reason-create/', views.ReasonCreateView.as_view()),
    path('reason-rud/<int:pk>/', views.ReasonRUDView.as_view()),
]
