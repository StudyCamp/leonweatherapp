from django.contrib import admin
from .models import User, Post, UserFriend

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')
    readonly_fields = ('id',)

class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'poster', 'timestamp')
    readonly_fields = ('id',)

class UserFriendAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'friending_user_id', 'time_created')
    readonly_fields = ('id',)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserFriend, UserFriendAdmin)