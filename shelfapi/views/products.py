from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from shelfapi.models import Product

class ProductView(ViewSet):
    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
        # Get the current authenticated user
        products = Product.objects.all()

        current_user = self.request.query_params.get('user', None)
        if current_user is not None:
            products = products.filter(user=request.auth.user)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product
        Returns:
            Response -- JSON serialized product instance
        """
        try:
            product = Product.objects.get(pk=pk)
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    
class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'image_path', 'quantity', 'description', 'price', 'subcategory', 'shop')
        depth = 1