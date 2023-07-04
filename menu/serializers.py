import os
from .models import *
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.StringRelatedField()
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


class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemImage
        fields = ('id', 'image', 'item')
        extra_kwargs = {'item': {'write_only': True}}


class ItemSerializer(serializers.ModelSerializer):
    # to set default availability to true
    availability = serializers.BooleanField(default=True)
    category_name = serializers.CharField(source='category', read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)
    # a list of IDs of removed images
    removed_images = serializers.ListField(child=serializers.IntegerField(), allow_null=True)
    
    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'category_name', 'price', 'description', 'options', 'availability', 'images', 'removed_images')

    # overriding this method to add images manually
    def create(self, validated_data):
        request_data = self.context['request'].data.items()
        # calling super().create() to handle many_to_many fields (here, options) automatically
        item = super().create(validated_data)

        # adding images
        for data in request_data:
            if data[0] not in validated_data.keys():
                item_image_serializer = ItemImageSerializer(data={"image":data[1], "item":item.id})

                if item_image_serializer.is_valid():
                    item_image_serializer.save()

        return item

