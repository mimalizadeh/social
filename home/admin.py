from django.contrib import admin
from home.models import Post, Comment, Vote


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'slug', 'updated', 'created')
    search_fields = ('slug', 'body')
    list_filter = ('updated',)
    prepopulated_fields = {'slug': ('body',)}
    raw_id_fields = ('user',)


admin.site.register(Post, PostAdmin)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'created', 'is_replay']
    raw_id_fields = ['user', 'post', 'replay']


@admin.register(Vote)
class VotesAdmin(admin.ModelAdmin):
    pass
