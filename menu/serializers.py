from .models import Category, Item, Option
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.CharField(read_only=True)
    # showing "items" related to this category in the respond
    # items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Category
        fields = '__all__'


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Item
        fields = '__all__'


class ItemCreateUpdateSerializer(serializers.ModelSerializer):
    availability = serializers.BooleanField(default=True)
    
    class Meta:
        model = Item
        fields = '__all__'
