from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view,throttle_classes
from rest_framework.views import APIView
from rest_framework import generics
from .models import MenuItem, Order,Cart,OrderItem,Menu,Booking, Menu
from .models import  Category
from .serializers import OrderSerializer,CartSerializer,OrderItemSerializer2
from .serializers import MenuItemSerializer, CategorySerializer, MenuSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group
from datetime import date,datetime
from django.db import IntegrityError
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework.pagination import PageNumberPagination
from .forms import BookingForm
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,HttpResponseBadRequest
from rest_framework.response import Response

# @csrf_exempt
# class MenuList(generics.ListCreateAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def patch(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)
    
# @csrf_exempt
# class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Menu.objects.all()
#     serializer_class = MenuSerializer

# @csrf_exempt
# def menu(request):
#     menu_data = MenuList.as_view()(request).data
#     main_data = {"menu": menu_data}
#     return render(request, 'menu.html', {"menu": main_data})


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def menu_list(request,pk=None):
    if request.method == 'POST':
        serializer = MenuSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            menus = Menu.objects.all()
            serializer = MenuSerializer(menus, many=True)
            main_data = serializer.data
            return render(request, 'menu.html', {"menu": main_data})
        else:
            return HttpResponse(status=400)

    elif request.method == 'GET':
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        main_data = serializer.data
        return render(request, 'menu.html', {"menu": main_data})

        
    elif request.method == 'PUT':
        menu_items = Menu.objects.all()
        menu_item = menu_items.filter(name=request.data['name']).first()
        if menu_item:
            serializer = MenuSerializer(menu_item, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':
        menu_items = Menu.objects.all()
        menu_item = menu_items.filter(name=request.data['name']).first()
        if menu_item:
            serializer = MenuSerializer(menu_item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)
        
    elif request.method == 'DELETE':
            menu_items = Menu.objects.all()
            menu_item = menu_items.filter(name=request.data['name']).first()
            if menu_item:
                menu_item.delete()
                return Response({'message': 'Menu item deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

@csrf_exempt
@api_view(['GET', 'POST','PATCH','PUT','DELETE'])
def menu_detail(request, pk):
    try:
        menu = Menu.objects.get(pk=pk)
    except Menu.DoesNotExist:
        return Response({'error': 'Menu not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MenuSerializer(menu)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = MenuSerializer(menu, data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PATCH':
        serializer = MenuSerializer(menu, data=request.POST, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        menu.delete()
        return Response({'message': 'Menu deleted successfully'}, status=status.HTTP_204_NO_CONTENT)



def home(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')

def reservations(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 

@csrf_exempt
def bookings(request):
    if request.method == 'GET':
        bookings = Booking.objects.all()
        booking_json = serializers.serialize('json', bookings)
        return HttpResponse(booking_json, content_type='application/json')

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
                reservation_slot=data['reservation_slot']).exists()
            if not exist:
                booking = Booking(
                    first_name=data['first_name'],
                    reservation_date=data['reservation_date'],
                    reservation_slot=data['reservation_slot'],
                )
                booking.save()
                response_data = {'success': True}
            else:
                response_data = {'error': 'Booking already exists.'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except:
            return HttpResponseBadRequest("Invalid input.")

    elif request.method == 'PUT' or request.method == 'PATCH' :
        try:
            data = json.loads(request.body)
            booking = Booking.objects.get(id=data['id'])
            booking.first_name = data['first_name']
            booking.reservation_date = data['reservation_date']
            booking.reservation_slot = data['reservation_slot']
            booking.save()
            response_data = {'success': True}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except:
            return HttpResponseBadRequest("Invalid input.")

    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            booking = Booking.objects.get(id=data['id'])
            booking.delete()
            response_data = {'success': True}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        except:
            return HttpResponseBadRequest("Invalid input.")

    else:
        response_data = {'error': 'Method not allowed.'}
        return HttpResponse(json.dumps(response_data), content_type='application/json')


# def bookings(request):
#     if request.method == 'POST':
#         data = json.load(request)
#         exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
#             reservation_slot=data['reservation_slot']).exists()
#         if exist==False:
#             booking = Booking(
#                 first_name=data['first_name'],
#                 reservation_date=data['reservation_date'],
#                 reservation_slot=data['reservation_slot'],
#             )
#             booking.save()
#         else:
#             return HttpResponse("{'error':1}", content_type='application/json')
    
#     date = request.GET.get('date',datetime.today().date())

#     bookings = Booking.objects.all().filter(reservation_date=date)
#     booking_json = serializers.serialize('json', bookings)

#     return HttpResponse(booking_json, content_type='application/json')


# Serializer for MenuItem
#https://www.coursera.org/learn/apis/lecture/oCEa9/relationship-serializers
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.select_related('category').all()
    serializer_class = MenuItemSerializer

# Serializer for MenuItem
class SingleMenuItemView(generics.RetrieveAPIView,generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

# Serializer for CategoryView
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Serializer for CategoryView
class SingleCategoryView(generics.RetrieveAPIView,generics.DestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class SingleOrderView(generics.RetrieveAPIView,generics.DestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


@api_view()
def category_detail(request,pk):
    category = get_object_or_404(Category,pk = pk)
    serialized_category = CategorySerializer(category,many=True)
    return Response(serialized_category.data)



@api_view(['Get','POST','PUT','PATCH','DELETE'])
@permission_classes([IsAuthenticated])
def menu_items(request,pk=None):
    paginator = PageNumberPagination()
    paginator.page_size = 5


    if request.method == 'GET' and pk is None:
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        if category_name:
            items = items.filter(category__title__icontains = category_name)
        
        to_price= request.query_params.get('to_price')
        if to_price:
            items = items.filter(price__lte = to_price)

        search = request.query_params.get('search')
        if search:
            items = items.filter(title__icontains = search)

        ordering = request.query_params.get('ordering')
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        result_page = paginator.paginate_queryset(items, request)
        serialized_item = MenuItemSerializer(result_page, many = True)
        return paginator.get_paginated_response(serialized_item.data)
    


    # if request.method == 'GET' and pk is None:
    #     items = MenuItem.objects.select_related('category').all()
    #     serialized_item = MenuItemSerializer(items, many = True)
    #     return Response(serialized_item.data,status.HTTP_200_OK)
    else:
        if request.user.groups.filter(name="Manager").exists():
            if pk is None:
                if request.method == 'POST':
                    serialized_item = MenuItemSerializer(data=request.data)
                    serialized_item.is_valid(raise_exception=True)
                    serialized_item.save()
                    return Response(serialized_item.data, status=status.HTTP_201_CREATED)
            else:
                if request.method == 'GET':
                    items = MenuItem.objects.select_related('category').get(title = pk)
                    serialized_item = MenuItemSerializer(items)
                    return Response(serialized_item.data,status.HTTP_200_OK)
                elif request.method == 'PUT' or request.method == 'PATCH':
                    try:
                        item = MenuItem.objects.get(title = pk)
                    except MenuItem.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                    serialized_item = MenuItemSerializer(item, data=request.data)
                    serialized_item.is_valid(raise_exception=True)
                    serialized_item.save()
                    return Response(serialized_item.data, status=status.HTTP_201_CREATED)
                elif request.method == 'DELETE':
                    try:
                        item = MenuItem.objects.get(title = pk)
                    except MenuItem.DoesNotExist:
                        return Response(status=status.HTTP_404_NOT_FOUND)
                    item.delete()
                    response_data = {'Menu-item id is deleted' : pk}
                    return Response(response_data)
        elif request.method == 'GET':
            items = MenuItem.objects.select_related('category').get(title = pk)
            serialized_item = MenuItemSerializer(items)
            return Response(serialized_item.data,status.HTTP_200_OK)
                    
        else:
            return Response({"message":"You are not authroized, need to be manager level"}, 403)

@api_view(['POST','GET'])
def single_menu_items(request,id):
    items = get_object_or_404(MenuItem,pk=id)
    serialized_item = MenuItemSerializer(items)
    return Response(serialized_item.data)


@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some Secret!"})


@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name="Manager").exists():
        return Response({"message": "Only manager can see this"})
    else:
        return Response({"message":"You are not authroized, need to be manager level"}, 403)




@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def managers(request,id=None):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET':
            # ======tobe continue
            group = Group.objects.get(name="Manager")
            users = group.user_set.all()
            user_list = [user.username for user in users]
            return Response(user_list)
        elif request.method == "DELETE":
            singleuser = get_object_or_404(User,id = id)
            managers = Group.objects.get(name="Manager")
            managers.user_set.remove(singleuser)
            return Response({"message":"Delete: removed from manager role"},status.HTTP_200_OK) 
        else:
            username = request.data['username']
            if username:
                user = get_object_or_404(User,username = username)
                managers = Group.objects.get(name="Manager")
                if request.method == 'POST':
                    managers.user_set.add(user)
                    return Response({"message":"Added ok " + username + " to be manager Added"},status.HTTP_201_CREATED)   
            else:
                return Response({"message":"No User Found"}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"You are not authroized, need to be manager level"}, 403)


@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def deliverycrew(request,id=None):
    if request.user.groups.filter(name="Manager").exists():
        if request.method == 'GET':
            group = Group.objects.get(name="Delivery-crew")
            users = group.user_set.all()
            user_list = [user.username for user in users]
            return Response(user_list)
        elif request.method == "DELETE":
            singleuser = get_object_or_404(User,id = id)
            managers = Group.objects.get(name="Delivery-crew")
            managers.user_set.remove(singleuser)
            return Response({"message":"Delete: removed from manager role"},status.HTTP_200_OK) 
        else:
            username = request.data['username']
            if username:
                user = get_object_or_404(User,username = username)
                crew = Group.objects.get(name="Delivery-crew")
                if request.method == 'POST':
                    crew.user_set.add(user)
                    return Response({"message":"Added ok " + username + " to be delivery crew Added"},status.HTTP_201_CREATED)   
            else:
                return Response({"message":"No User Found"}, status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message":"You are not authroized, need to be manager level"}, 403)





@api_view(['GET','POST','DELETE'])
@permission_classes([IsAuthenticated])
def cart(request):
    user = request.user
    if request.user.groups.filter(name="Customer").exists():
        if request.method == 'GET':
            try:
                cart_items = Cart.objects.filter(user=user)
                serializer = CartSerializer(cart_items, many=True)
                return Response(serializer.data,status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response({"message":"No Cart Found"},status=status.HTTP_404_NOT_FOUND)
        elif request.method == 'POST':
            existing_cart_item = Cart.objects.filter(user = user, menuitem = request.data['menuitem'],quantity=request.data['quantity'])
            if existing_cart_item.exists():
                return Response({"message": "This same item and quantity are already exists in the cart."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer = CartSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(user=request.user)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            try:
                    cart_items = Cart.objects.filter(user=user)
                    if cart_items.exists():
                        cart_items.delete()
                        return Response({"message":"Cart Deleted."},status=status.HTTP_204_NO_CONTENT)
            except Cart.DoesNotExist:
                return Response({"message":"No Cart Found"},status=status.HTTP_404_NOT_FOUND)

            return Response({"message":"Cart not found"},status=status.HTTP_404_NOT_FOUND)
    
    else:
        return Response({"message":"You are not a Customer"}, 403)


@api_view(['POST','GET','DELETE','PUT','PATCH'])
@permission_classes([IsAuthenticated])
def orderView(request,pk=None):
    if request.user.groups.filter(name="Customer").exists():

        if request.method == 'POST':
            user = request.user

            # Get the cart items for the current user
            cart_items = Cart.objects.filter(user=user)
            if cart_items.exists():

                # Calculate the total price
                total_price = sum(cart_item.price for cart_item in cart_items)

                # Create the order object
                order = Order.objects.create(
                    user=user,
                    total=total_price,
                    status=False,
                    date=date.today()
                )

                # Create the order items
                order_items = []
                for cart_item in cart_items:
                    order_item = OrderItem(
                        order=order,
                        menuitem=cart_item.menuitem,
                        quantity=cart_item.quantity,
                        unit_price=cart_item.unit_price,
                        price=cart_item.price
                    )
                    order_items.append(order_item)

                # Bulk create the order items
                OrderItem.objects.bulk_create(order_items)

                # Delete the cart items
                cart_items.delete()

                # Return the order object
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            else:
                return Response({"Message: Cart is Empty"},status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == 'GET':
            user = request.user
            if pk:
                try:
                    order = Order.objects.get(id=pk, user=request.user)
                    orderitem = OrderItem.objects.get(order_id = order.id)
                    serializer = OrderItemSerializer2(orderitem)
                    return Response(serializer.data)
                except Order.DoesNotExist:
                    return Response({'message': 'Order not found for this user.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                orders = Order.objects.filter(user=request.user)
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
        #Below is the Delete function, save for future 
        elif request.method == 'DELETE':
            # Get all orders for the current user
            try:
                user = request.user
            # Delete the orders and order items associated with the user
                Order.objects.filter(user=user).delete()
                OrderItem.objects.filter(order__user=user).delete()

                # Return a success message
                return Response({'message': 'All orders and order items deleted for user.'})
                
            except Order.DoesNotExist:
                return Response({"message":"No Order Found"},status=status.HTTP_404_NOT_FOUND)
    elif request.user.groups.filter(name="Manager").exists():
        if request.method == "GET":
            if pk:
                try:
                    order = Order.objects.get(id=pk)
                    orderitem = OrderItem.objects.get(order_id = order.id)
                    serializer = OrderItemSerializer2(orderitem)
                    return Response(serializer.data)
                except Order.DoesNotExist:
                    return Response({'message': 'Order not found for this user.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                orders = Order.objects.all()
                serializer = OrderSerializer(orders, many=True)
                return Response(serializer.data)
        elif request.method == 'DELETE':
            if pk:
                try:
                    order = Order.objects.get(id=pk)
                    orderitem = OrderItem.objects.get(order_id = order.id)
                    order.delete()
                    orderitem.delete()
                    return Response({'message': 'Order for this orderID ' + str(pk) + ' is Deleted.'},status=status.HTTP_200_OK)
                except:
                    return Response({'message': 'Order not found per this ID.'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'message': 'Manager would need the orderId for DELETE operation.'}, status=status.HTTP_404_NOT_FOUND)
        
        elif request.method == 'PATCH' or request.method == 'PUT':
            try:
                order = Order.objects.get(id=pk)
            except Order.DoesNotExist:
                return Response({'message': 'Order not found per this ID.'}, status=status.HTTP_404_NOT_FOUND)
            
            delivery_crew_id = request.data.get('delivery_crew', None)
            if delivery_crew_id:
                try:
                    delivery_crew = User.objects.get(pk=delivery_crew_id)
                    order.delivery_crew = delivery_crew
                except User.DoesNotExist:
                    return Response({'message': 'The delivery crew does not exist'}, status=status.HTTP_404_NOT_FOUND)

 
            if 'status' in request.data:
                order.status = request.data['status']
            order.save()

            return Response({'message': 'Order ID.' + str(pk)+' is updated.'}, status=status.HTTP_200_OK)
    
    elif request.user.groups.filter(name="Delivery-crew").exists():
        if pk:
            if request.method == 'PATCH':
                try:
                    order = Order.objects.filter(delivery_crew=request.user.id, id=pk).first()
                except Order.DoesNotExist:
                    return Response({'message': 'Order not found per this ID.'}, status=status.HTTP_404_NOT_FOUND)
                if 'status' in request.data:
                    order.status = request.data['status']
                    order.save()
                    return Response({'message': 'Order ID.' + str(pk)+' is updated.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'Only the status can be changed'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"message":"Only PATCH method allow for delivery crew with Order ID"}, status=status.HTTP_404_NOT_FOUND)
        else:
            if request.method == 'GET':
                if Order.objects.filter(delivery_crew=request.user.id).exists():
                    serializer = OrderSerializer(Order.objects.filter(delivery_crew=request.user.id), many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response({"message":"No orders found for this delivery crew"}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'message':'Current User does not belong to Customer, Manager or Delivery crew'}, status=status.HTTP_404_NOT_FOUND)
            
        
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"Successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([UserRateThrottle])
def throttle_check_auth(request):
    return Response({"message":"Message for the logged in users only"})



