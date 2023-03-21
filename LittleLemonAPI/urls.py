from django.urls import path 
from . import views 
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [ 
    #path('', views.index, name='index'), 
    # path('test/', views.test),
    # path('orders/', views.OrderView.as_view()),
    # path('orders/<int:pk>', views.OrderView.as_view()),
    # path('orderview/',views.OrderView.as_view()),
    path('menu-item/', views.MenuItemView.as_view()),
    # path('menu-item/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items/',views.menu_items),
    path('menu-items/<str:pk>',views.menu_items),
    # path('menu-items/<int:id>', views.single_menu_items),
    path('categories', views.CategoryView.as_view()),
    path('category/<int:pk>', views.SingleCategoryView.as_view()),
    path('categories/<int:pk>', views.category_detail,name = 'category-detail'),
    path('secret/', views.secret),
    path('api-token-auth/',obtain_auth_token),
    path('manager-view/',views.manager_view),
    path('groups/manager/users',views.managers),
    path('groups/manager/users/<int:id>',views.managers),
    path('groups/delivery-crew/users',views.deliverycrew),
    path('groups/delivery-crew/users/<int:id>',views.deliverycrew),
    path('cart/menu-items',views.cart),
    path('orders/',views.orderView),
    path('orders/<int:pk>',views.orderView),
    path('throttle-check/',views.throttle_check),
    path('throttle-check-auth/',views.throttle_check_auth),


    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu_list, name="menu"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    # path('menu_item/<int:pk>/', views.menu_detail, name="menu_item"),  

    path('bookings/', views.bookings, name='bookings'), 
]