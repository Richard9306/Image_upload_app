from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, status
import os
from .models import CustomUser
from .serializers import CustomUserSerializer, ImageUploadSerializer
from image_upload_app import settings


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class ImageView(APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']
            # You can process the image here if needed
            # For example, you can save it to a specific directory
            image_path = os.path.join(settings.MEDIA_ROOT, image.name)
            with open(image_path, 'wb') as f:
                f.write(image.read())

            return Response({'message': 'Image uploaded successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


