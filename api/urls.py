from django.urls import path

from .views import UserList, UserDetail, ImageList, ImageDetail, ExpiringLinkView


urlpatterns = [
    path('user/', UserList.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('image/', ImageList.as_view()),
    path('image/<int:pk>/', ImageDetail.as_view()),
    path('expiring-link/', ExpiringLinkView.as_view())
]