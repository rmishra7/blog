
from django.conf.urls import url

from posts import apis

urlpatterns = [
    url(r'^$', apis.BlogPostsApi.as_view(), name="api_posts"),
    url(r'^ID:(?P<post_id>\d+)/$', apis.BlogPostsDetailApi.as_view(), name="api_posts_detail"),
    url(r'^ID:(?P<post_id>\d+)/comments/$', apis.BlogPostCommentsApi.as_view(), name="api_comments"),
    url(r'^ID:(?P<post_id>\d+)/comments/(?P<comment_id>\d+)/$', apis.BlogPostCommentsDetailApi.as_view(), name="api_coomments_detail"),
    url(r'^ID:(?P<post_id>\d+)/likes/$', apis.BlogPostLikesApi.as_view(), name="api_posts"),
    # url(r'^ID:(?P<post_id>\d+)/comments/(?P<comment_id>\d+)/likes/$', apis.BlogCommentsLikesApi.as_view(), name="api_posts")
]
