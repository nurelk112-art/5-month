from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product, Review
from .serializers import (
    CategorySerializer, CategoryListSerializer, CategoryValidateSerializer,
    ProductSerializer, ProductReviewsSerializer, ProductValidateSerializer,
    ReviewSerializer, ReviewValidateSerializer
)

# --- КАТЕГОРИИ ---

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategoryListSerializer(categories, many=True)
        return Response(data=serializer.data)
        
    elif request.method == 'POST':
        # Передаем входящие данные в валидатор
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            # Если данные корректны, создаем объект вручную из валидированных данных
            category = Category.objects.create(
                name=serializer.validated_data.get('name')
            )
            return Response(data=CategorySerializer(category).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'errors': 'Категория не найдена'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(data=serializer.data)
        
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        if serializer.is_valid():
            category.name = serializer.validated_data.get('name')
            category.save()
            return Response(data=CategorySerializer(category).data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- ТОВАРЫ ---

@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(data=serializer.data)
        
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create(
                title=serializer.validated_data.get('title'),
                description=serializer.validated_data.get('description'),
                price=serializer.validated_data.get('price'),
                category_id=serializer.validated_data.get('category_id')
            )
            return Response(data=ProductSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'errors': 'Товар не найден'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)
        
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        if serializer.is_valid():
            product.title = serializer.validated_data.get('title')
            product.description = serializer.validated_data.get('description')
            product.price = serializer.validated_data.get('price')
            product.category_id = serializer.validated_data.get('category_id')
            product.save()
            return Response(data=ProductSerializer(product).data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- ОТЗЫВЫ ---

@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
        
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():
            review = Review.objects.create(
                text=serializer.validated_data.get('text'),
                stars=serializer.validated_data.get('stars'),
                product_id=serializer.validated_data.get('product_id')
            )
            return Response(data=ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'errors': 'Отзыв не найден'}, status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(data=serializer.data)
        
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        if serializer.is_valid():
            review.text = serializer.validated_data.get('text')
            review.stars = serializer.validated_data.get('stars')
            review.product_id = serializer.validated_data.get('product_id')
            review.save()
            return Response(data=ReviewSerializer(review).data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --- ТОВАРЫ С ОТЗЫВАМИ ---
@api_view(['GET'])
def product_reviews_list_api_view(request):
    products = Product.objects.all()
    serializer = ProductReviewsSerializer(products, many=True)
    return Response(data=serializer.data)