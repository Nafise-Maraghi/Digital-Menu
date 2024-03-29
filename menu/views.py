import os
from .models import Category, Item, Option
from .serializers import CategorySerializer, CategoryCreateUpdateSerializer, ItemBaseSerializer, ItemCreateSerializer, ItemUpdateSerializer, OptionSerializer
from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated


# Category views

# creating a single model instance
class CategoryCreateAPI(generics.CreateAPIView):
    model = Category
    # permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateUpdateSerializer


# representing a single model instance
class CategoryRetrieveAPI(generics.RetrieveAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# representing a collection of model instances
class CategoryListAPI(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# updating a single model instance
class CategoryUpdateAPI(generics.UpdateAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryCreateUpdateSerializer


# deleting a single model instance
class CategoryDeleteAPI(generics.DestroyAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    def perform_destroy(self, instance):
        items = instance.items.all()

        # removing images locally
        for item in items:
            images = item.images.all()

            if images:
                for item_image in images:
                    try:
                        os.remove(item_image.image.path)
                    except:
                        pass

        return super().perform_destroy(instance)

# ______________________________

# Item views

# creating a single model instance
class ItemCreateAPI(generics.CreateAPIView):
    model = Item
    # permission_classes = [IsAuthenticated]
    serializer_class = ItemCreateSerializer


# representing a single model instance
class ItemRetrieveAPI(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Item.objects.all()
    serializer_class = ItemBaseSerializer


# representing a collection of model instances
class ItemListAPI(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemBaseSerializer


# updating a single model instance
class ItemUpdateAPI(generics.UpdateAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemUpdateSerializer


# deleting a single model instance
class ItemDeleteAPI(generics.DestroyAPIView):
    lookup_field = 'pk'
    queryset = Item.objects.all()

    # permission_classes = [IsAuthenticated]
    def perform_destroy(self, instance):
        images = instance.images.all()

        # removing images locally
        if images:
            for item_image in images:
                os.remove(item_image.image.path)

        return super().perform_destroy(instance)

# ______________________________

# Option views

# creating a single model instance
class OptionCreateAPI(generics.CreateAPIView):
    model = Option
    # permission_classes = [IsAuthenticated]
    serializer_class = OptionSerializer


# representing a single model instance
class OptionRetrieveAPI(generics.RetrieveAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


# representing a collection of model instances
class OptionListAPI(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


# updating a single model instance
class OptionUpdateAPI(generics.UpdateAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


# deleting a single model instance
class OptionDeleteAPI(generics.DestroyAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
