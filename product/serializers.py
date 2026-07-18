from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Category, Product, Review

# ==================== БАЗОВЫЕ СЕРИАЛИЗАТОРЫ (ВЫВОД ДАННЫХ) ====================

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, category):
        return category.products.count()

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']

class ProductReviewsSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'reviews', 'rating']

    def get_rating(self, product):
        reviews = product.reviews.all()
        if not reviews.exists():
            return 0.0
        total_stars = sum([review.stars for review in reviews])
        return round(total_stars / reviews.count(), 1)


# ==================== СЕРИАЛИЗАТОРЫ ВАЛИДАЦИИ (ВХОДЯЩИЕ ДАННЫЕ) ====================

class CategoryValidateSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, max_length=255, min_length=2)

    def validate_name(self, name):
        # Пример кастомной валидации: проверка на уникальность имени категории
        if Category.objects.filter(name=name).exists():
            raise ValidationError("Категория с таким названием уже существует.")
        return name


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, max_length=255, min_length=3)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    category_id = serializers.IntegerField(required=True)

    def validate_price(self, price):
        if price <= 0:
            raise ValidationError("Цена должна быть больше нуля.")
        return price

    def validate_category_id(self, category_id):
        # Проверяем, существует ли указанная категория в базе данных
        if not Category.objects.filter(id=category_id).exists():
            raise ValidationError("Категория с указанным ID не существует.")
        return category_id


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=5)
    stars = serializers.IntegerField(required=False, default=5)
    product_id = serializers.IntegerField(required=True)

    def validate_stars(self, stars):
        if stars < 1 or stars > 5:
            raise ValidationError("Оценка должна быть в диапазоне от 1 до 5.")
        return stars

    def validate_product_id(self, product_id):
        # Проверяем, существует ли товар, к которому пишется отзыв
        if not Product.objects.filter(id=product_id).exists():
            raise ValidationError("Товар с указанным ID не существует.")
        return product_id