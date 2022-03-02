from django.contrib import admin

from users.models import User
from baskets.admin import BasketAdminInline


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (BasketAdminInline,)
    list_display = ('username', 'first_name', 'last_name', 'email')
    fields = ('username', 'first_name', 'last_name', 'email')
    search_fields = ('last_name',)
    ordering = ('last_name',)