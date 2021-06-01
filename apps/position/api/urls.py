from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.position.api.v1.urls')),
]