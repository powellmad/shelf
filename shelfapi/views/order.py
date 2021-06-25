from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from rest_framework import status
from shelfapi.models import Order, OrderProduct, Product

class OrderView(ViewSet):
    """Order items for Shelf customers"""
    @action(methods=['put'], detail=True)
    def checkout(self, request, pk=None):

        try: 
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(
                {'message': 'Order does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == "PUT":
            try:
                order.is_open = True
                
                order.save()
                return Response({}, status=status.HTTP_200_OK)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        return Response({}, status=status.HTTP_201_CREATED)

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
        order = Order.objects.get(pk=pk)
        serializer = OrderSerializer(order, context={'request': request})
        return Response(serializer.data)


    def destroy(self, request, pk=None):
        """Handle DELETE requests for single product in the order
        Returns:
            Response -- JSON serialized order instance
        """

        try:
            user = request.auth.user
            
            order = Order.objects.filter(user=user).get(pk=pk)
            
            qs = OrderProduct.objects.filter(order=order).filter(product_id=request.data["product_id"])
            item = qs[0]
            item.delete()

            serializer = OrderSerializer(qs, many=True)
            return Response(serializer.data)

        except IndexError:
            return Response({'message': 'item not in cart'}, status=status.HTTP_404_NOT_FOUND)


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
