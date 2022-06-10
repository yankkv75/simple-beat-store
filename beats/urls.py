from django.urls import path, include
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>', views.home, name='beats_by_category'),
    path('category/<slug:category_slug>/<slug:beat_slug>', views.beat, name='beat_details'),
    path('cart', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:beat_id>', views.add_cart, name='add_cart'),
    path('account/create/', views.sign_up_view, name='signup'),
    path('account/signin/', views.sign_in_view, name='signin'),
    path('account/signout/', views.sign_out, name='signout'),
]


