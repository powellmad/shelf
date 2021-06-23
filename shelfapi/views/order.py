from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from shelfapi.models import Order, OrderProduct, Product
from .products import ProductSerializer

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


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for orders
    Arguments:
        serializers
    """

    line_items = ProductSerializer(many=True)

    class Meta:
        model = Order
        url = serializers.HyperlinkedIdentityField(
            view_name='order',
            lookup_field='id'
        )
        fields = ('id', 'payment_type', 'user_id', 'is_open', 'line_items',)
        depth = 1
