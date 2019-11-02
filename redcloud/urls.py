from django.urls import path
from . import views
from .views import PostListView,PostDetailView,PostCreateView,PostUpdateView, PostDeleteView, PostLikeToggle
urlpatterns = [
    #path('', PostListView.as_view(), name = 'blog-home'),
    path('', views.landingpage, name='landing'),
    path('first/', views.firstview, name = 'blog-first'),
    path('home/', views.home, name = 'blog-home'),
    path('tag/<slug:tag_slug>', views.home, name = 'post_list_by_tag'),
    #path('post/<int:pk>', views.post_detail, name = 'post-detail'),
    path('about/', views.about, name = 'blog-about'),
    path('post/<int:pk>/', PostDetailView.as_view(), name = 'post-detail'),
    path('post/<int:pk>/like', PostLikeToggle.as_view(), name = 'post-like'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name = 'post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name = 'post-delete'),
    path('post/new/', PostCreateView.as_view(), name = 'post-create'),
]



#<app>/<model>_<viewtype>.html