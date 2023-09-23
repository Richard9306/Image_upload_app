from .models import CustomUser, Images, Tiers, ExpiringLink
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('__all__')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ('__all__')



class TierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tiers
        fields = ('__all__')


class ExpiringLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpiringLink
        fields = ('__all__')