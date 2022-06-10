from django.db import models
from django.urls import reverse
from django import forms


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Beat(models.Model):
    name = models.CharField(max_length=100, unique=True)
    artist = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='beat', blank=True)
    audio_file = models.FileField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=12)
    stock = models.IntegerField(null=True)
    youtube = models.CharField(max_length=250, blank=True)
    instagram = models.CharField(max_length=250, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)
        verbose_name = 'beat'
        verbose_name_plural = 'beats'

    def get_url(self):
        return reverse('beat_details', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']
        db_table = 'Cart'

    def __str__(self):
        return self.cart_id


# Добавление таблицы в БД "CartItem". Одна корзина может иметь много айтемов
class CartItem(models.Model):
    beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def full_sum(self):
        return self.beat.price * self.quantity

    def __str__(self):
        return self.beat
