from rest_framework import serializers
from .models import AnimateImage
from django.contrib.auth.models import User

import base64
from rest_framework import serializers
from django.core.files import File


class PreprocessedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimateImage
        fields = ["animate", "image", "left_right", "toon_comic", "ani_effect", "transition_effect", "image_base64"]