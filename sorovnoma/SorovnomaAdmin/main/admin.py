from django.contrib import admin

from main.models import RequiredChannel, Sorovnoma, User, Vote, Variant


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_filter = ['is_admin', 'is_human']
    list_editable = ['is_active']
    list_display = ['tg_id', 'full_name', 'phone_number', 'is_admin', 'is_active']


class VoteAdmin(admin.ModelAdmin):
    list_filter = ['variant', 'created_at']
    list_display = ['id', 'variant', 'user']


class VariantAdmin(admin.ModelAdmin):
    list_filter = [ 'created_at']
    list_display = ['id', 'name']


class SorovnomaAdmin(admin.ModelAdmin):
    list_filter = ['deadline', 'is_active', "created_at"]
    search_fields = ['admin__full_name', 'description']
    list_display = ['id', 'admin', 'description', 'number_of_votes', "deadline", "is_active"]


class ChannelAdmin(admin.ModelAdmin):
    list_filter = ['sorovnoma__description', 'created_at']
    list_editable = ['is_active']
    search_fields = ['admin__full_name', 'sorovnoma__description', 'sorovnoma__variant']
    list_display = ['username', 'number_of_planed_users', 'number_of_joined_users', 'admin', 'is_active', 'sorovnoma']


admin.site.register(User, UserAdmin)
admin.site.register(Vote, VoteAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Sorovnoma, SorovnomaAdmin)

admin.site.register(RequiredChannel, ChannelAdmin)
