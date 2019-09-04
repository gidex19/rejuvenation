from django.contrib import admin

from .models import Post
from .models import Comment
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author','title','date_posted')
    list_filter = ('date_posted','author')
    search_fields = ('title','content')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)
    #prepopulated_fields = {'title':('content',)}


#admin.site.register(Comment)
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentor','text','post')
    list_filter = ('post','date_commented','active')
    search_fields = ('text',)
    #ordering = ('-date_commented')