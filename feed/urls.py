# from django.urls import path
# from .views import FeedListView, FeedDetailView, FeedCreateView, FeedUpdateView, FeedDeleteView, FeedLike
# from . import views
# from users import views as user_views

# urlpatterns = [
#     path('', FeedListView.as_view(), name='blog-home'),
#     path('feed/<int:pk>/', FeedDetailView.as_view(), name='feed-detail'),
#     path('feed/new/', FeedCreateView.as_view(), name='feed-create'),
#     path('feed/<int:pk>/update/', FeedUpdateView.as_view(), name='feed-update'),
#     path('feed/<int:pk>/delete/', FeedDeleteView.as_view(), name='feed-delete'),
#     path('about/', views.about, name='blog-about'),
#     path('profile/<int:pk>', user_views.profile, name='profile'),
#     #path('feed-like/<int:pk>', FeedLike, name='feed_like'),
# ]
