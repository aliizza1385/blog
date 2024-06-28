from django.urls import path,include
from . import views
from rest_framework import routers
from .views import UserCrud,handle_react_data,TagCrud,CategoryCrud ,Comments_RUD ,Main ,post_detail,filter_category, search,Login, Register,Logout_view, main_left, replis, like_post


router = routers.SimpleRouter()

urlpatterns = [
    # path('upload_file', views.upload_file,name='cart'),
    # path('upload_file/<int:id>', views.Post_detail),
    path('posts', handle_react_data.as_view({'get': 'list', 'post':'create'})),
    path('posts/<int:pk>', handle_react_data.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('users', UserCrud.as_view({'get': 'list', 'post':'create'})),
    path('users/<int:pk>', UserCrud.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('tags', TagCrud.as_view({'get': 'list', 'post':'create'})),
    path('tags/<int:pk>', TagCrud.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('category', CategoryCrud.as_view({'get': 'list', 'post':'create'})),
    path('category/<int:pk>', CategoryCrud.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('comments', Comments_RUD.as_view({'get': 'list', 'post':'create'})),
    path('comments/<int:pk>', Comments_RUD.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # above for react-admin
    # and behind is main page
    path('main',Main ,name='main'),
    path('main-left',main_left ,name='main-left'),
    path('',Main ,name='main'),
    path('login/',Login, name='login'),
    path('logout/',Logout_view,name='logout'),
    path('register',Register, name='register'),
    path('main/posts/<int:pk>', post_detail, name='post_detail'),
    path('main/category/<slug:slug>', filter_category, name='filter_category'),
    path('search/', search, name='search'),
    path('replis/', replis, name='replis'),
    path('like/<int:post_id>', like_post, name='like_post'),


]