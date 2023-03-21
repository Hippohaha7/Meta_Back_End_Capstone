from rest_framework import serializers
from .models import MenuItem,Category,Order,Cart,OrderItem,Menu
from django.utils import timezone
from datetime import date

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']

class MenuItemSerializer(serializers.HyperlinkedModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    # category = serializers.HyperlinkedRelatedField(queryset = Category.objects.all(),view_name='category-detail')
    class Meta:
        model = MenuItem
        fields = ['id','title', 'price','featured','category','category_id']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['id', 'user', 'unit_price', 'price']

    # def validate_menuitem(self, value):
    #     """
    #     Check that the menuitem is available
    #     """
    #     if not value.featured:
    #         raise serializers.ValidationError("Selected item is not available")
    #     return value

    def create(self, validated_data):
        """
        Create and return a new Cart instance, given the validated data.
        """
        menuitem = validated_data.pop('menuitem')
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = menuitem.price * validated_data['quantity']
        cart = Cart.objects.create(menuitem=menuitem, **validated_data)
        return cart
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date']
        read_only_fields = ['id', 'user', 'total', 'date']

    def create(self, validated_data):
        user = self.context['request'].user
        cart_items = Cart.objects.filter(user=user)
        order_items = []
        total_price = 0

        for cart in cart_items:
            order_item = OrderItem(
                order=None, 
                menuitem=cart.menuitem, 
                quantity=cart.quantity,
                unit_price=cart.unit_price,
                price=cart.price
            )
            order_items.append(order_item)
            total_price += cart.price
        
        

        order = Order.objects.create(
            user=user,
            delivery_crew=validated_data.get('delivery_crew', None),
            status=validated_data.get('status', False),
            total=total_price,
            date=date.today,
        )

        for order_item in order_items:
            order_item.order = order
            order_item.save()

        cart_items.delete()
        
        return order


class OrderItemSerializer2(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer2(serializers.ModelSerializer):
    order_items = OrderItemSerializer2(many=True, read_only=True)
    cart_items = serializers.PrimaryKeyRelatedField(many=True, queryset=Cart.objects.all(), write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items', 'cart_items']
        read_only_fields = ['id', 'status', 'total', 'order_items']

    def create(self, validated_data):
        cart_items = validated_data.pop('cart_items')
        order = Order.objects.create(**validated_data)

        total_price = 0
        order_items_data = []

        for cart_item in cart_items:
            menuitem = cart_item.menuitem
            quantity = cart_item.quantity
            unit_price = cart_item.unit_price
            price = cart_item.price

            total_price += price
            order_items_data.append({
                'order': order,
                'menuitem': menuitem,
                'quantity': quantity,
                'unit_price': unit_price,
                'price': price
            })

        order.total = total_price
        order.save()

        order_items = OrderItem.objects.bulk_create([OrderItem(**item_data) for item_data in order_items_data])
        order.order_items.set(order_items)

        return order
