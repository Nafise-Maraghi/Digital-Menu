from .views import *
from django.urls import path

urlpatterns = [
    # /category
    path('category/create/', CategoryCreateAPI.as_view()),
    path('category/list/', CategoryListAPI.as_view()),
    path('category/list/<int:pk>/', CategoryRetrieveAPI.as_view()),
    path('category/update/<int:pk>/', CategoryUpdateAPI.as_view()),
    path('category/delete/<int:pk>/', CategoryDeleteAPI.as_view()),

    # /item
    path('item/create/', ItemCreateAPI.as_view()),
    path('item/list/', ItemListAPI.as_view()),
    path('item/list/<int:pk>/', ItemRetrieveAPI.as_view()),
    path('item/update/<int:pk>/', ItemUpdateAPI.as_view()),
    path('item/delete/<int:pk>/', ItemDeleteAPI.as_view()),

    # /option
    path('option/create/', OptionCreateAPI.as_view()),
    path('option/list/', OptionListAPI.as_view()),
    path('option/list/<int:pk>/', OptionRetrieveAPI.as_view()),
    path('option/update/<int:pk>/', OptionUpdateAPI.as_view()),
    path('option/delete/<int:pk>/', OptionDeleteAPI.as_view()),
]
