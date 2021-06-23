from shelfapi.views import categories
from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from shelfapi.models import Shop, Category

class ShopView(ViewSet):

    def list(self, request):
        """Handle GET requests to shops resource
        Returns:
            Response -- JSON serialized list of shops
        """
        shops = Shop.objects.all().order_by('category')

        serializer = ShopSerializer(
            shops, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category
        Returns:
            Response -- JSON serialized category instance
        """
        try:
            shop = Shop.objects.get(pk=pk)
            serializer = ShopDetailSerializer(shop, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized shop instance
        """

        # Create a new Python instance of the Category class
        # and set its properties from what was sent in the
        # body of the request from the client.
        shop = Shop()
        shop.name = request.data["name"]
        shop.logo_path = request.data["logo_path"]
        shop.user = request.auth.user

        category = Category.objects.get(pk=request.data["category_id"])
        shop.category = category
       

        # Try to save the new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
        try:
            shop.save()
            serializer = ShopSerializer(shop, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """Handle PUT requests for a shop

        Returns:
            Response -- Empty body with 204 status code
        """
        shop = Shop.objects.get(pk=pk)
        shop.name = request.data["name"]
        shop.user = request.auth.user
        shop.logo_path = request.data["logo_path"]

        category = Category.objects.get(pk=request.data["category_id"])
        shop.category = category

        try:
            shop.save()
        except ValidationError as ex:
            return Response({'reason': ex.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)        


class ShopSerializer(serializers.ModelSerializer):
    """JSON serializer for shops"""

    class Meta:
        model = Shop
        fields = ('id', 'user', 'category', 'name', 'logo_path' )
        depth = 1

class ShopDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = ( 'name', 'logo_path', 'user', 'category', 'products' )
        depth = 1
