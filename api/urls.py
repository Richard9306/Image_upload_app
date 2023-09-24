from django.urls import path

from .views import (
    UserList,
    UserDetail,
    ImageDetail,
    ExpiringLinkView,
    RetrieveExpiringLinkView,
    ImageUploadAndThumbnailView,
)


urlpatterns = [
    path("user/", UserList.as_view()),
    path("user/<int:pk>/", UserDetail.as_view()),
    path("image_upload/", ImageUploadAndThumbnailView.as_view()),
    path("image_upload/<int:pk>", ImageDetail.as_view()),
    path("expiring-link/", ExpiringLinkView.as_view()),
    path("expiring-link/<int:img_id>", RetrieveExpiringLinkView.as_view()),
]
