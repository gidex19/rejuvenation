from django import template
from redcloud.models import Post
from django.db.models import Count
from redcloud.models import Comment
register = template.Library()

@register.simple_tag
def total_posts():
    return Post.objects.count()
@register.simple_tag
def total_comments():
    return Comment.objects.count()

@register.simple_tag
def tag_author(exa):
    return exa.author

@register.simple_tag
def get_most_commented_posts(count = 5):
    return Post.objects.annotate(items=Count('comments')).order_by('-items')[:count]

@register.inclusion_tag('redcloud/customised/latest.html')
def display_latest_posts(count=5):
    latest_posts = Post.objects.order_by('-date_posted')[:count]
    return {'latest_posts':latest_posts}

@register.inclusion_tag('redcloud/customised/all_tags.html')
def display_all_tags(count=4):
    all_tags = Post.tags.all()[:count]
    return {'all_tags':all_tags}

@register.inclusion_tag('redcloud/customised/like_btn.html')
def display_like_colours(post):
    all_likes = post.likes.all()
    return {'all_likes':all_likes}
