from .models import *
from rest_framework import serializers
class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = '__all__'


class WordBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'name', 'category', 'english', 'uzb']
        read_only_fields = ['id', 'created_at']


class WordUseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = [ 'name',  'english', 'uzb', 'example_en', 'example_uz']
        read_only_fields = ['id', 'created_at']