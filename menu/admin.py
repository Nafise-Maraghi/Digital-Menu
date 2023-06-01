from .models import Category, CategoryIcon, Item, Option 
from django.contrib import admin


admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Option)

@admin.register(CategoryIcon)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['id', 'availability']