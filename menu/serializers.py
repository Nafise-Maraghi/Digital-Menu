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


class ItemBaseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category', read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'category_name', 'price', 'description', 'options', 'availability', 'images')


class ItemCreateSerializer(ItemBaseSerializer, serializers.ModelSerializer):
    # to set default availability to true
    availability = serializers.BooleanField(default=True)

    # overriding this method to add images manually
    def create(self, validated_data):
        request_data = self.context['request'].data.items()
        # calling super().create() to create an instance
        item = super().create(validated_data)

        # adding images
        for data in request_data:
            if data[0] not in validated_data.keys():
                item_image_serializer = ItemImageSerializer(data={"image":data[1], "item":item.id})

                if item_image_serializer.is_valid():
                    item_image_serializer.save()

        return item


class ItemUpdateSerializer(ItemBaseSerializer, serializers.ModelSerializer):
    # a list of IDs of removed images
    removed_images = serializers.ListField(child=serializers.IntegerField(), allow_null=True)
    
    class Meta:
        model = Item
        fields = ('id', 'name', 'category', 'category_name', 'price', 'description', 'options', 'availability', 'images', 'removed_images')

    # overriding this method to update images manually
    def update(self, instance, validated_data):
        request_data = self.context['request'].data.items()

        # removing old images
        if 'removed_images' in validated_data:
            removed_images = validated_data['removed_images']
            
            for item_image in instance.images.all():
                if item_image.id in removed_images:
                    os.remove(item_image.image.path)
                    item_image.delete()

        # adding new images
        for data in request_data:
            if data[0] not in validated_data.keys():
                item_image_serializer = ItemImageSerializer(data={"image":data[1], "item":instance.id})

                if item_image_serializer.is_valid():
                    item_image_serializer.save()

        # calling super().update() to update values in validated_data
        return super().update(instance, validated_data)
