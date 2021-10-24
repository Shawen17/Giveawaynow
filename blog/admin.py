from django.contrib import admin
from .models import Blog, Comment
from django.contrib.admin import ModelAdmin


@admin.register(Blog)
class BlogAdmin(ModelAdmin):
    list_display=('title','description','image','date','genre','story')
    ordering= ('-date','-genre')
    search_fields=('title','genre')


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    list_display= ('email','created','body','active')
    ordering = ('-created',)
    list_filter= ('active','created')
    search_fields = ('email','body')
    actions = ['approved_comments']

    def approved_comments(self,request,queryset):
        queryset.update(active=True)



