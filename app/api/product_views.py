from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .product_models import Product, Cart, Checkout  # Updated import
from .serializers import ProductSerializer, CartSerializer, CheckoutSerializer

class ProductView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Create a new product
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddToCartView(APIView):
    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewCartView(APIView):
    def get(self, request):
        cart_items = Cart.objects.all()
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)

class CheckoutView(APIView):
    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if serializer.is_valid():
            # Process each item in the cart
            cart_items = Cart.objects.filter(id__in=request.data.get('cart', []))
            
            # Check inventory first
            for item in cart_items:
                if item.product.inventory < item.quantity:
                    return Response(
                        {'error': f'Not enough inventory for {item.product.name}'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            # Update inventory
            for item in cart_items:
                item.product.inventory -= item.quantity
                item.product.save()
            
            # Create checkout record
            checkout = serializer.save()
            
            # Clear the cart (optional)
            cart_items.delete()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateCartView(APIView):
    def put(self, request, item_id):
        try:
            cart_item = Cart.objects.get(id=item_id)
            serializer = CartSerializer(cart_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RemoveCartView(APIView):
    def delete(self, request, item_id):
        try:
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
