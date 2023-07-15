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

    def validate(self, data):
        if data['images'] is not None and data['preview_image'] is None:
            raise serializers.ValidationError("preview image is required")

        return data

    # overriding this method to add images manually
    def create(self, validated_data):
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
    # a list of new images
    images = serializers.ListField(child=serializers.ImageField(), max_length=5, allow_null=False, default=None, write_only=True)
    # if the new preview image is uploaded
    new_preview_image = serializers.ImageField(write_only=True)
    # if the new preview image already exists
    new_preview_image_id = serializers.IntegerField(write_only=True)
    # a list of IDs of removed images
    removed_images = serializers.ListField(child=serializers.IntegerField(), allow_null=False, write_only=True)
    # a list of IDs of removed options
    removed_options = serializers.ListField(child=serializers.IntegerField(), allow_null=False, write_only=True)
    
    class Meta(ItemBaseSerializer.Meta):
        fields = ItemBaseSerializer.Meta.fields + ('removed_images', 'new_preview_image_id', 'new_preview_image', 'removed_options')
    

    def validate_new_preview_image_id(self, value):
        images_id = [x['id'] for x in self.instance.images.all().values()]
        preview_image_id = self.instance.images.get(preview=True).id

        if value not in images_id:
            raise serializers.ValidationError(f"invalid id \"{value}\"")
        
        if value == preview_image_id:
            raise serializers.ValidationError("new value is required")
            
        return value


    def validate_removed_images(self, value):
        images_id = [x['id'] for x in self.instance.images.all().values()]
        
        for x in value:
            if x not in images_id:
                raise serializers.ValidationError(f"Invalid pk \"{x}\" - object does not exist.")
        
        return value


    def validate_removed_options(self, value):
        options_id = [x['id'] for x in self.instance.options.all().values()]

        for x in value:
            if x not in options_id:
                raise serializers.ValidationError(f"Invalid pk \"{x}\" - object does not exist.")

        return value


    def validate(self, data):
        preview_image_id = self.instance.images.get(preview=True).id

        if 'removed_images' in data and preview_image_id in data['removed_images']:
            if 'new_preview_image' not in data and 'new_preview_image_id' not in data:
                raise serializers.ValidationError("new preview image is required")

        if 'new_preview_image_id' in data and 'new_preview_image' in data:
            raise serializers.ValidationError("preview image must be unique")

        if 'images' in data:
            new_images = len(data['images'])
            images = self.instance.images.count()

            try:
                removed_images = len(data['removed_images'])
                
            except:
                removed_images = 0

            if new_images + images - removed_images > 5:
                raise serializers.ValidationError("maximum number of images exceeded")

        return data


    # overriding this method to update images manually
    def update(self, instance, validated_data):
        # changing new preview image
        if 'new_preview_image_id' in validated_data:
            old_preview_image = self.instance.images.get(preview=True)
            old_preview_image.preview = False
            old_preview_image.save()
            new_id = validated_data.pop('new_preview_image_id')
            new_item_image = ItemImage.objects.get(id=new_id)
            new_item_image.preview = True
            new_item_image.save()
        
        elif 'new_preview_image' in validated_data:
            old_preview_image = self.instance.images.get(preview=True)
            old_preview_image.preview = False
            old_preview_image.save()
            new_image = validated_data.pop('new_preview_image')
            serializer = ItemImageSerializer(data={'image': new_image, 'item': instance.id, 'preview': True})

        # removing old images
        if 'removed_images' in validated_data:
            removed_images = validated_data.pop('removed_images')
            images = instance.images.all()

            for item_image in images:
                if item_image.id in removed_images:
                    os.remove(item_image.image.path)
                    item_image.delete()

        # adding new images
        if 'images' in validated_data:
            images = validated_data.pop('images')

            for image in images:
                serializer = ItemImageSerializer(data={'image': image, 'item': instance.id, 'preview': False})

                if serializer.is_valid():
                    serializer.save()

        # adding new options
        if 'options' in validated_data:
            options = validated_data.pop('options')

            for option in options:
                instance.options.add(option)

        # removing old options
        if 'removed_options' in validated_data:
            removed_options = validated_data.pop('removed_options')
            options = instance.options.all()

            for option in options:
                if option.id in removed_options:
                    instance.options.remove(option)
                    # instance.remove(option)
                    instance.save()
        
        # calling super().update() to update values in validated_data
        return super().update(instance, validated_data)
