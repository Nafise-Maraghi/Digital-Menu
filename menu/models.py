from django.db import models


class CategoryIcon(models.Model):
    icon = models.ImageField(upload_to="uploads/icons/", blank=False, null=False)
    availability = models.BooleanField(default=False)

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
    availability = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items', blank=False, null=False)
    description = models.CharField(max_length=250, help_text='ingredients', blank=True, null=True)
    image = models.ImageField(upload_to="uploads/images/", blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.PositiveIntegerField(blank=False, null=False)
    options = models.ManyToManyField(Option, related_name='options', blank=True)

    def __str__(self):
        return self.name
