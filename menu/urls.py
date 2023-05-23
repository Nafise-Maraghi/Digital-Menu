from .views import *
from django.urls import path

urlpatterns = [
    path('category/list/', CategoryListAPI.as_view()),
    path('item/create/', ItemCreateAPI.as_view()),
    path('item/list/', ItemListAPI.as_view()),
    path('item/update/<int:pk>/', ItemUpdateAPI.as_view()),
    path('item/delete/<int:pk>/', ItemDeleteAPI.as_view()),
    path('option/create/', OptionCreateAPI.as_view()),
    path('option/list/', OptionListAPI.as_view()),
    path('option/update/<int:pk>/', OptionUpdateAPI.as_view()),
    path('option/delete/<int:pk>/', OptionDeleteAPI.as_view()),
]
