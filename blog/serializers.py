from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post
from django.core.files.base import ContentFile
import base64

class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    image = serializers.CharField(allow_null=True, required=False)

    class Meta:
        model = Post
        fields = ('author', 'title', 'text', 'created_date', 'published_date', 'image')

    def create(self, validated_data):
        # 이미지 데이터를 디코딩하여 모델에 저장
        image_data = validated_data.pop('image', None)
        if image_data:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            decoded_image = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            validated_data['image'] = decoded_image
        return super().create(validated_data)

    
    