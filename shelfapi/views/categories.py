from django.http import HttpResponseServerError
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.contrib.auth.models import User
from shelfapi.models import Category, category

class CategoryView(ViewSet):

    def list(self, request):
        """Handle GET requests to categories resource
        Returns:
            Response -- JSON serialized list of categories
        """
        categories = Category.objects.all().order_by('label')

        category = self.request.query_params.get('categoryId', None)
        if category is not None:
            categories = categories.filter(category__id=category)

        serializer = CategorySerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category
        Returns:
            Response -- JSON serialized category instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized category instance
        """

        # Create a new Python instance of the Category class
        # and set its properties from what was sent in the
        # body of the request from the client.
        category = Category()
        category.label = request.data["label"]
       

        # Try to save the new category to the database, then
        # serialize the category instance as JSON, and send the
        # JSON as a response to the client request
        try:
            category.save()
            serializer = PostCategorySerializer(category, context={'request': request})
            return Response(serializer.data)

        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        fields = ('id', 'label' )
        depth = 1

class PostCategorySerializer(serializers.ModelSerializer):
    """JSON serializer for categories"""

    class Meta:
        model = Category
        fields = ( 'label', )
        depth = 1
