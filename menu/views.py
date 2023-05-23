from .models import Category, Item, Option
from .serializers import CategorySerializer, ItemSerializer, OptionSerializer
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


# Category views

# representing a collection of model instances
class CategoryListAPI(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# ______________________________

# Item views

# creating a single model instance
class ItemCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    model = Item
    serializer_class = ItemSerializer


# representing a collection of model instances
class ItemListAPI(generics.ListAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


# updating a single model instance
class ItemUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


# deleting a single model instance
class ItemDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


# ______________________________

# Option views

# creating a single model instance
class OptionCreateAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    model = Option
    serializer_class = OptionSerializer


# representing a collection of model instances
class OptionListAPI(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OptionSerializer
    queryset = Option.objects.all()


# updating a single model instance
class OptionUpdateAPI(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = OptionSerializer
    queryset = Option.objects.all()


# deleting a single model instance
class OptionDeleteAPI(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    serializer_class = OptionSerializer
    queryset = Option.objects.all()
