from rest_framework import serializers
from .models import Category, Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'text', 'stars', 'product']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, category):
        return category.products.count()


# --- ВОТ ЭТОТ КЛАСС НУЖНО ДОБАВИТЬ/ВЕРНУТЬ ---
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__' 


class ProductReviewsSerializer(serializers.ModelSerializer):
    """Специальный сериализатор для вывода товаров вместе с их отзывами и средним рейтингом"""
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