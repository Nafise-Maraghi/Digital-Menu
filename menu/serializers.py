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
        fields = ('id', 'image', 'item', 'preview')
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
    # the image that should be previewed in the main page
    preview_image = serializers.ImageField(default=None, write_only=True)
    images = serializers.ListField(child=serializers.ImageField(), max_length=5, allow_null=False, default=None, write_only=True)

    class Meta(ItemBaseSerializer.Meta):
        fields = ItemBaseSerializer.Meta.fields + ('preview_image',)

    # overriding this method to add images manually
    def create(self, validated_data):
        print(validated_data)
        preview_image = validated_data.pop('preview_image')
        images = validated_data.pop('images')
        options = validated_data.pop('options')
        item = Item.objects.create(**validated_data)

        if preview_image:
            serializer = ItemImageSerializer(data={'image': preview_image, 'item': item.id, 'preview': True})

            if serializer.is_valid():
                serializer.save()
        
        if images:
            for image in images:
                serializer = ItemImageSerializer(data={'image': image, 'item': item.id, 'preview': False})

                if serializer.is_valid():
                    serializer.save()
        
        if options:
            item.options.add(*options)

        return item


class ItemUpdateSerializer(ItemBaseSerializer, serializers.ModelSerializer):
    # a list of IDs of removed images
    removed_images = serializers.ListField(child=serializers.IntegerField(), allow_null=False, write_only=True)
    # a list of new images
    images = serializers.ListField(child=serializers.ImageField(), max_length=5, allow_null=False, default=None, write_only=True)
    old_preview_image_id = serializers.IntegerField(write_only=True)
    # if the new preview image already exists
    new_preview_image_id = serializers.IntegerField(write_only=True)
    # if the new preview image is uploaded
    new_preview_image = serializers.ImageField(write_only=True)
    
    class Meta(ItemBaseSerializer.Meta):
        fields = ItemBaseSerializer.Meta.fields + ('removed_images', 'old_preview_image_id', 'new_preview_image_id', 'new_preview_image')

    # overriding this method to update images manually
    def update(self, instance, validated_data):
        # removing old images
        if 'removed_images' in validated_data:
            removed_images = validated_data['removed_images']
            
            for item_image in instance.images.all():
                if item_image.id in removed_images:
                    os.remove(item_image.image.path)
                    item_image.delete()

        # adding new images
        if 'images' in validated_data:
            images = validated_data['images']

            for image in images:
                serializer = ItemImageSerializer(data={'image': image, 'item': instance.id, 'preview': False})

                if serializer.is_valid():
                    serializer.save()
        
        if 'new_preview_image_id' in validated_data:
            new_id = validated_data['new_preview_image_id']
            new_item_image = ItemImage.objects.get(id=new_id)
            new_item_image.preview = True
            new_item_image.save()

        
        elif 'new_preview_image' in validated_data:
            new_image = validated_data['new_preview_image']
            serializer = ItemImageSerializer(data={'image': new_image, 'item': instance.id, 'preview': True})

            if serializer.is_valid():
                serializer.save()

        if 'old_preview_image_id' in validated_data:
            old_id = validated_data['old_preview_image_id']

            try:
                old_item_image = ItemImage.objects.get(id=old_id)
                old_item_image.preview = False
                old_item_image.save()
            except:
                pass


        # calling super().update() to update values in validated_data
        return super().update(instance, validated_data)
