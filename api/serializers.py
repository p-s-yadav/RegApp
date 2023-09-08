from rest_framework import serializers
from .models import BizData

class BizDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizData
        fields = '__all__'
