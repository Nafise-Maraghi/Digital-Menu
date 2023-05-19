from .views import *
from django.urls import path

urlpatterns = [
    path('/category/create/', CategoryCreateAPI.as_view()),
    path('/category/list/', CategoryCreateAPI.as_view()),
    path('/category/update/<int:pk>', CategoryCreateAPI.as_view()),
    path('/category/delete/<int:pk>', CategoryCreateAPI.as_view()),
]