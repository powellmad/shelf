from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from shelfapi.models import Order, OrderProduct, Product

class OrderView(ViewSet):
    """Order items for Shelf customers"""

    def create(self, request):
        """Handle POST operation for a new order/shopping cart

        Returns:
            Response -- JSON serialized order instance
        """
        order_item = OrderProduct()
        order_item.product = Product.objects.get(pk=request.data["product_id"])

        user = User.objects.get(pk=request.auth.user.id)
        order, created = Order.objects.get_or_create(
            is_open=True,
            user_id=user.id
        )

        order_item.order = order
        order_item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to orders resource
        Returns:
            Response -- JSON serialized list of shops
        """
        user = User.objects.get(pk=request.auth.user.id)
        shops = Order.objects.filter(user_id=user.id)

        serializer = OrderSerializer(
            shops, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order
        Returns:
            Response -- JSON serialized order instance
        """
        try:
            order = Order.objects.get(pk=pk)
            serializer = OrderSerializer(order, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


class OrderSerializer(serializers.ModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers
    """

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'payment_type', 'user_id', 'is_open', 'products')
        depth = 1
