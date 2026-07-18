from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    # decimal_places=2 означает две цифры после запятой для копеек/центов
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    # Связь «один ко многим»: у одной категории может быть много товаров
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")

    def __str__(self):
        return self.title

class Review(models.Model):
    text = models.TextField(verbose_name="Текст отзыва")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews', verbose_name="Товар")
    
    # Новое поле для рейтинга от 1 до 5
    STAR_CHOICES = (
        (1, '★'),
        (2, '★★'),
        (3, '★★★'),
        (4, '★★★★'),
        (5, '★★★★★'),
    )
    stars = models.IntegerField(default=5, choices=STAR_CHOICES, verbose_name="Оценка")

    def __str__(self):
        return f"Отзыв ({self.stars}★) для {self.product.title}"