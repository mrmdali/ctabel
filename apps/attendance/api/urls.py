from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.attendance.api.v1.urls')),
]