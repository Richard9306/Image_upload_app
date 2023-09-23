from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import CustomUser, Tiers, Images, ExpiringLink
from .serializers import CustomUserSerializer, ImageSerializer, TierSerializer, ExpiringLinkSerializer

class UserList(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class ImageList(generics.ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Images.objects.all()
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)
        return queryset

class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ImageSerializer
    queryset = Images.objects.all()



class ExpiringLinkView(generics.ListCreateAPIView):
    serializer_class = ExpiringLinkSerializer
    permission_classes = [IsAuthenticated]
    queryset = ExpiringLink.objects.all()
    def create(self, request, *args, **kwargs):
        try:
            image_id = request.data['uploaded_image']
            expiration_time = int(request.data['expiration_time'])
        except (KeyError, ValueError):
            return Response({'detail': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure the expiration time is within the allowed range (300 to 30000 seconds)
        if not (300 <= expiration_time <= 30000):
            return Response({'detail': 'Expiration time out of range. The available time is between 300 and 30000 seconds'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uploaded_image = Images.objects.get(id=image_id, user=request.user)
        except Images.DoesNotExist:
            return Response({'detail': 'Image not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create the expiring link
        expiring_link = ExpiringLink.objects.create(
            uploaded_image=uploaded_image,
            expiration_time=expiration_time
        )

        return Response(ExpiringLinkSerializer(expiring_link).data, status=status.HTTP_201_CREATED)














# from rest_framework.response import Response
# from rest_framework import viewsets, status
# from .models import CustomUser, Images
# from .serializers import CustomUserSerializer, ImageUploadSerializer
# from PIL import Image
# from io import BytesIO
# from django.core.files.uploadedfile import InMemoryUploadedFile
#
#
# class CustomUserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#
#
# THUMBNAIL_SIZES = {
#     'thumbnail_200': (200, 200),
#     'thumbnail_400': (400, 400),
#     'original': None,  # No resizing for the original image
# }
#
#
# class ImageUploadViewSet(viewsets.ModelViewSet):
#     queryset = Images.objects.all()
#     serializer_class = ImageUploadSerializer
#
#     def generate_thumbnail(self, image, size):
#         img = Image.open(image)
#         img.thumbnail(size, Image.ANTIALIAS)
#
#         buffer = BytesIO()
#         img.save(buffer, format='JPEG')  # You can choose another format if needed
#         buffer.seek(0)
#
#         return InMemoryUploadedFile(
#             buffer, None, image.name, 'image/jpeg', buffer.tell(), None
#         )
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         # Get the image file from the request
#         image = serializer.validated_data['image']
#
#         # Create the uploaded image and save the original image
#         uploaded_image = Images.objects.create(user=request.user, image=image)
#
#         # Generate and save the thumbnails
#         for thumbnail_name, size in THUMBNAIL_SIZES.items():
#             if size:
#                 thumbnail = self.generate_thumbnail(image, size)
#                 setattr(uploaded_image, thumbnail_name, thumbnail)
#
#         uploaded_image.save()
#
#         return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
