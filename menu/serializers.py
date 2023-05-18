from .models import Category, Item, Option
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['name', 'price']


class Itemserializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
