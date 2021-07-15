from django.urls import path, include

urlpatterns = [
    path('v1/', include('apps.terminal.api.v1.urls')),
]