from django.contrib import admin

from .models import Post, Group, Comment, Follow


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'author', 'pub_date', 'group')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    list_editable = ('group',)
    empty_value_display = '-пусто-'


class GroupAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)
    prepopulated_fields = {"slug": ("title",)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'post')
    search_fields = ('author',)
    empty_value_display = '-пусто-'


class FolllowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(Follow, FolllowAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
