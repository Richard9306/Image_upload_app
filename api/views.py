from django.utils import timezone
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from PIL import Image
from io import BytesIO
from django.core.files import File
from .models import CustomUser, Images, ExpiringLink
from .serializers import (
    CustomUserSerializer,
    ImageUploadSerializer,
    ExpiringLinkSerializer,
)


class UserList(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated]
    queryset = Images.objects.all()


class ImageUploadAndThumbnailView(generics.ListCreateAPIView):
    queryset = Images.objects.all()
    serializer_class = ImageUploadSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        queryset = Images.objects.all()
        user = self.request.query_params.get("user")
        if user:
            queryset = queryset.filter(user=user)
        return queryset

    def perform_create(self, serializer):
        # Associate the uploaded image with the authenticated user
        serializer.save(user=self.request.user)
        user_account = self.request.user.status
        image_instance = serializer.instance
        if user_account:
            if user_account.tier_type == "basic":
                thumbnail_heights = [200]
            elif user_account.tier_type == "premium":
                thumbnail_heights = [200, 400]

            elif user_account.tier_type == "enterprise":
                thumbnail_heights = [200, 400]
            for height in thumbnail_heights:
                thumbnail_data = self.generate_thumbnail(
                    image_instance.original_image, height
                )
                setattr(image_instance, f"thumbnail_{height}", thumbnail_data)
                image_instance.save()

    def generate_thumbnail(self, image_field, height):
        img = Image.open(image_field)
        img.load()
        thumbnail_buffer = BytesIO()
        img.thumbnail((img.width, height), Image.LANCZOS)
        img = img.convert("RGB")
        img.save(thumbnail_buffer, format="PNG")
        thumbnail_file = File(img)
        thumbnail_buffer.close()
        return thumbnail_file


class ExpiringLinkView(generics.ListCreateAPIView):
    serializer_class = ExpiringLinkSerializer
    permission_classes = [IsAuthenticated]
    queryset = ExpiringLink.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            image_id = request.data["uploaded_image"]
            expiration_time = int(request.data["expiration_time"])
        except (KeyError, ValueError):
            return Response(
                {"detail": "Invalid request data"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Ensure the expiration time is within the allowed range (300 to 30000 seconds)
        if not (300 <= expiration_time <= 30000):
            return Response(
                {
                    "detail": "Expiration time out of range. The available time is between 300 and 30000 seconds"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            uploaded_image = Images.objects.get(id=image_id, user=request.user)
        except Images.DoesNotExist:
            return Response(
                {"detail": "Image not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Create the expiring link
        expiring_link = ExpiringLink.objects.create(
            uploaded_image=uploaded_image, expiration_time=expiration_time
        )

        return Response(
            ExpiringLinkSerializer(expiring_link).data, status=status.HTTP_201_CREATED
        )


class RetrieveExpiringLinkView(generics.RetrieveAPIView):
    queryset = ExpiringLink.objects.all()
    serializer_class = ExpiringLinkSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "image_id"

    def retrieve(self, request, *args, **kwargs):
        try:
            expiring_link = ExpiringLink.objects.get(
                uploaded_image__user=request.user, uploaded_image__id=kwargs["image_id"]
            )
            if timezone.now() > expiring_link.created_at + timezone.timedelta(
                seconds=expiring_link.expiration_time
            ):
                return Response(
                    {"detail": "Expiring link has expired"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ExpiringLink.DoesNotExist:
            return Response(
                {"detail": "Expiring link not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(ExpiringLinkSerializer(expiring_link).data)
