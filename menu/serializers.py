from .models import Category, Item
from rest_framework import serializers


# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Option
#         fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
