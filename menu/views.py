from .models import Category, Item, Option
from . serializers import CategorySerializer, Itemserializer, OptionSerializer
from django.shortcuts import render
from rest_framework import generics


# creating a single model instance
class CategoryCreateAPI(generics.CreateAPIView):
    model = Category
    serializer_class = CategorySerializer


# representing a collection of model instances
class CategoryListAPI(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# updating a single model instance
class CategoryUpdateAPI(generics.UpdateAPIView):
    lookup_field = 'pk'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# deleting a single model instance
class CategoryDeleteAPI(generics.DestroyAPIView):
    lookup_field = 'pk'
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
