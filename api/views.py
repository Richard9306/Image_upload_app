from django.utils import timezone
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from PIL import Image
from io import BytesIO
import tempfile
from .models import CustomUser, Tiers, Images, ExpiringLink
from .serializers import (
    CustomUserSerializer,
    ImageUploadSerializer,
    TierSerializer,
    ExpiringLinkSerializer,
)


class UserList(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ImageDetail(generics.RetrieveAPIView):
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

        # Generate thumbnails based on the user's account tier
        user_account = self.request.user.status
        image_instance = serializer.instance

        if user_account:
            # Customize thumbnail heights based on account tier settings
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
        # Resize the image to the specified height while keeping the width constant
        img.thumbnail((img.width, height), Image.LANCZOS)
        thumbnail_buffer = BytesIO()
        img = img.convert("RGB")
        img.save(thumbnail_buffer, format="PNG")
        thumbnail_data = thumbnail_buffer.getvalue()
        thumbnail_buffer.close()
        # Create a temporary in-memory file and assign it to the image field
        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            temp_file.write(thumbnail_data)
            temp_file.flush()
            print(image_field.name)
            # image_field.name = image_field.name.rstrip(".png") + f'_thumbnail_{height}.jpg'  # Assign a unique name
            image_field.file = temp_file

        return img  # Return the modified image field


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



