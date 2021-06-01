from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('account-register/', views.AccountRegisterView.as_view(), name='register-account'),
    path('account-detail-update/<int:pk>/', views.AccountDetailUpdateView.as_view(), name='account-detail-update'),
    path('account-change-password/<int:pk>/', views.ChangePasswordView.as_view(), name='account-change-password'),


    path('all-workers-list/', views.AllWorkersListView.as_view(), name='list-header-worker'),
    path('dismissed-workers-list/', views.DismissedWorkersListView.as_view(), name='list-dismissed-worker'),
    path('worker-list/', views.WorkerListView.as_view(), name='list-header-worker'),
    path('worker-detail-update/<int:pk>/', views.WorkerRetrieveUpdateView.as_view(), name='detail-update-worker'),
    path('worker-dismiss/<int:pk>/', views.WorkerDismissView.as_view(), name='dismiss-worker'),
    path('worker-activate/<int:pk>/', views.WorkerActivateView.as_view(), name='dismiss-worker'),
    # path('logout/', views.AccountLogoutView.as_view(), name='logout-account'),

    # tokens
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # http://127.0.0.1:8000/api/account/v1/login/

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # http://127.0.0.1:8000/api/account/v1/refresh/
]
