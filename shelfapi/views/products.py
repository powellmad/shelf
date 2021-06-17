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
        user = User.objects.get(user=request.auth.user)
        products = Product.objects.all()

        current_user = self.request.query_params.get('user', None)
        if current_user is not None:
            products = products.filter(user=user)

        serializer = ProductSerializer(
            products, many=True, context={'request': request})
        return Response(serializer.data)

