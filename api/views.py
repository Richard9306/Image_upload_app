
from rest_framework.response import Response

from rest_framework import viewsets, status

from .models import CustomUser, Images
from .serializers import CustomUserSerializer, ImageUploadSerializer

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


THUMBNAIL_SIZES = {
    'thumbnail_200': (200, 200),
    'thumbnail_400': (400, 400),
    'original': None,  # No resizing for the original image
}


class ImageUploadViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    serializer_class = ImageUploadSerializer

    def generate_thumbnail(self, image, size):
        img = Image.open(image)
        img.thumbnail(size, Image.ANTIALIAS)

        buffer = BytesIO()
        img.save(buffer, format='JPEG')  # You can choose another format if needed
        buffer.seek(0)

        return InMemoryUploadedFile(
            buffer, None, image.name, 'image/jpeg', buffer.tell(), None
        )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get the image file from the request
        image = serializer.validated_data['image']

        # Create the uploaded image and save the original image
        uploaded_image = Images.objects.create(user=request.user, image=image)

        # Generate and save the thumbnails
        for thumbnail_name, size in THUMBNAIL_SIZES.items():
            if size:
                thumbnail = self.generate_thumbnail(image, size)
                setattr(uploaded_image, thumbnail_name, thumbnail)

        uploaded_image.save()

        return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
