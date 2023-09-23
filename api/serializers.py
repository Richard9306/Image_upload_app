from .models import CustomUser, Images
from rest_framework import serializers

class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "status", "img_uploaded"]


class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()