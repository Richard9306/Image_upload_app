from django.urls import path, include
from rest_framework import routers
from .views import CustomUserViewSet, ImageUploadViewSet

router = routers.DefaultRouter()
router.register(r"user", CustomUserViewSet)

router.register(r'images', ImageUploadViewSet, basename='image-upload')
urlpatterns = router.urls

urlpatterns = [
    path('api/', include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path('upload/', ImageView.as_view(), name='image-upload'),
]