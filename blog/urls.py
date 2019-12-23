from . import views
from .views import ListPostView,DetailPostView,CreatePostView,UpdatePostView,DeletePostView,UserListPostView
from django.urls import path

urlpatterns = [
    path('', ListPostView.as_view(), name='blog-home'),
    path('user/<str:username>', UserListPostView.as_view(), name='user-posts'),
    path('post/like', views.like_post, name="like_post"),
    path('post/<int:pk>/update/', UpdatePostView.as_view(), name='post-update'),
    path('post/<int:id>/', views.post_detail, name='post-detail'),
    path('post/new', CreatePostView.as_view(), name='post-create'),
    path('post/<int:pk>/delete', DeletePostView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about')
]

