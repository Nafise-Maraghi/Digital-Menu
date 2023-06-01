from .models import Category, CategoryIcon, Item, Option
from .serializers import *
from django.shortcuts import render
from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated


def change_category_icon_availability(pk):
    category_icon = CategoryIcon.objects.get(pk=pk)

    try:
        if category_icon.category:
            category_icon.availability = False
    
    except:
        category_icon.availability = True

    category_icon.save()


# ______________________________

# Category views

# creating a single model instance
class CategoryCreateAPI(generics.CreateAPIView):
    model = Category
    # permission_classes = [IsAuthenticated]
    serializer_class = CategoryCreateUpdateSerializer
    
    def perform_create(self, serializer):
        category_icon_pk = serializer.validated_data["icon"].pk
        serializer.save()
        change_category_icon_availability(category_icon_pk)


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

    def perform_update(self, serializer):

        # check id "icon" is being updated:
        if "icon" in serializer.validated_data:
            old_category_icon_pk = self.get_object().icon.pk
            serializer.save()
            new_category_icon_pk = serializer.data["icon"]
            change_category_icon_availability(old_category_icon_pk)
            change_category_icon_availability(new_category_icon_pk)

        else:
            serializer.save()


# deleting a single model instance
class CategoryDeleteAPI(generics.DestroyAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()

    def perform_destroy(self, instance):
        instance.delete()
        category_icon_pk = instance.icon.pk
        change_category_icon_availability(category_icon_pk)


# ______________________________

# Item views

# creating a single model instance
class ItemCreateAPI(generics.CreateAPIView):
    model = Item
    # permission_classes = [IsAuthenticated]
    serializer_class = ItemCreateUpdateSerializer


# representing a single model instance
class ItemRetrieveAPI(generics.RetrieveAPIView):
    lookup_field = 'pk'
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# representing a collection of model instances
class ItemListAPI(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


# updating a single model instance
class ItemUpdateAPI(generics.UpdateAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()
    serializer_class = ItemCreateUpdateSerializer


# deleting a single model instance
class ItemDeleteAPI(generics.DestroyAPIView):
    lookup_field = 'pk'
    # permission_classes = [IsAuthenticated]
    queryset = Item.objects.all()


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
