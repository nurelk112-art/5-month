from rest_framework import serializers
from .models import Category, Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']

class CategorySerializer(serializers.ModelSerializer):
    # Оставляем только базовые поля для создания/изменения
    class Meta:
        model = Category
        fields = ['id', 'name']

class CategoryListSerializer(serializers.ModelSerializer):
    # Отдельный сериализатор для вывода списка (с подсчетом)
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