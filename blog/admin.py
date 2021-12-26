from django.contrib import admin
from .models import Post, Comment

admin.site.register(Post)
admin.site.register(Comment)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'post', 'created_on', 'approved_comment')
    list_filter = ('approved_comment', 'created_on')
    search_fields = ('author', 'email', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
