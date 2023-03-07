from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # generate jwt token
    TokenRefreshView,  # generate jwt refresh token
)

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRouters),
    path('projects/', views.getProjects),
    path('projects/<str:pk>/', views.getProject),
    path('projects/<str:pk>/vote/', views.projectVote),

    path('remove-tag/', views.removeTag)
]
