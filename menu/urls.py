from .views import *
from django.urls import path

urlpatterns = [
    path('category/create/', CategoryCreateAPI.as_view()),
    path('category/list/', CategoryListAPI.as_view()),
    path('category/update/<int:pk>', CategoryUpdateAPI.as_view()),
    path('category/delete/<int:pk>', CategoryDeleteAPI.as_view()),
]