from django.db import models


class CategoryIcon(models.Model):
    class Meta:
        db_table = "menu_category_icon"
        
    icon = models.ImageField(upload_to="uploads/icons/", blank=False, null=False)

    def __str__(self):
        return self.icon.url


class Category(models.Model):
    class Meta:
        verbose_name_plural = "categories"

    name = models.CharField(max_length=100, blank=False, null=False)
    icon = models.OneToOneField(CategoryIcon, blank=False, null=False, on_delete=models.RESTRICT)

    def __str__(self):
        return self.name


class Option(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    description = models.CharField(max_length=250, help_text='ingredients', blank=True, null=True)
    options = models.ManyToManyField(Option, related_name='options', blank=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ItemImage(models.Model):
    image = models.ImageField(upload_to="uploads/images/", blank=False, null=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images', blank=False, null=False)

    def __str__(self):
        return self.image.url
