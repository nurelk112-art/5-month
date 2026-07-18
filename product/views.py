from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

# --- КАТЕГОРИИ ---

@api_view(['GET'])
def category_list_api_view(request):
    """Вывод списка всех категорий"""
    categories = Category.objects.all()
    # many=True говорит сериализатору, что мы передаем список (массив) объектов, а не один
    serializer = CategorySerializer(categories, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def category_detail_api_view(request, id):
    """Вывод одной категории по её id"""
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        # Если объекта с таким id нет в базе — возвращаем ошибку 404 Not Found
        return Response(data={'errors': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CategorySerializer(category)
    return Response(data=serializer.data)


# --- ТОВАРЫ ---

@api_view(['GET'])
def product_list_api_view(request):
    """Вывод списка всех товаров"""
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def product_detail_api_view(request, id):
    """Вывод одного товара по его id"""
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'errors': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductSerializer(product)
    return Response(data=serializer.data)


# --- ОТЗЫВЫ ---

@api_view(['GET'])
def review_list_api_view(request):
    """Вывод списка всех отзывов"""
    reviews = Review.objects.all()
    serializer = ReviewSerializer(reviews, many=True)
    return Response(data=serializer.data)

@api_view(['GET'])
def review_detail_api_view(request, id):
    """Вывод одного отзыва по его id"""
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'errors': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = ReviewSerializer(review)
    return Response(data=serializer.data)