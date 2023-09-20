from django.urls import path, include
from rest_framework import routers
from .views import CustomUserViewSet, ImageView

router = routers.DefaultRouter()
router.register(r"user", CustomUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('upload/', ImageView.as_view(), name='image-upload'),
]