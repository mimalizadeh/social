from django.urls import path
from home.views import HomeView, PostDetailView, PostDeleteView, PostUpdateView, PostCreateViewTwo, CommentReplyView, \
    VotesLikeView

app_name = 'home'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<slug:post_slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/delete/<int:post_id>', PostDeleteView.as_view(), name='post_delete'),
    path('post/update/<int:post_id>', PostUpdateView.as_view(), name='post_update'),
    # path('post/create/', PostCreateView.as_view(), name='post_create')
    path('post/create/', PostCreateViewTwo.as_view(), name='post_create'),
    path('reply/<post_id>/<comment_id>/ ', CommentReplyView.as_view(), name='reply_comment'),
    path('like/<post_id>/', VotesLikeView.as_view(), name='post_like')
]
