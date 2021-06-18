from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from shelfapi.models import Product, Subcategory, Shop

class ProductView(ViewSet):
    def list(self, request):
        """Handle GET requests to products resource
        Returns:
            Response -- JSON serialized list of products
        """
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

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized product instance
        """

        # Create a new Python instance of the Product class
        # and set its properties from what was sent in the
        # body of the request from the client.
        product = Product()
        product.name = request.data["name"]
        product.image_path = request.data["image_path"]
        product.quantity = request.data["quantity"]
        product.description = request.data["description"]
        product.price = request.data["price"]
        
        subcategory = Subcategory.objects.get(pk=request.data["subcategory_id"])
        product.subcategory = subcategory
        
        shop = Shop.objects.get(pk=request.data["shop_id"])
        product.shop = shop

        # Try to save the new product to the database, then
        # serialize the product instance as JSON, and send the
        # JSON as a response to the client request
        try:
            product.save()
            serializer = ProductSerializer(product, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a product

        Returns:
            Response -- Empty body with 204 status code
        """
        product = Product.objects.get(pk=pk)
        product.name = request.data["name"]
        product.image_path = request.data["image_path"]
        product.quantity = request.data["quantity"]
        product.description = request.data["description"]
        product.price = request.data["price"]

        subcategory = Subcategory.objects.get(pk=request.data["subcategory_id"])
        product.subcategory = subcategory
        
        shop = Shop.objects.get(pk=request.data["shop_id"])
        product.shop = shop

        try:
            product.save()
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)        

    
class ProductSerializer(serializers.ModelSerializer):
    """JSON serializer for products"""

    class Meta:
        model = Product
        fields = ('id', 'name', 'image_path', 'quantity', 'description', 'price', 'subcategory', 'shop')
        depth = 1