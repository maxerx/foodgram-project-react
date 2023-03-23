from django.contrib import admin
from users.models import User, Follow
from .models import (Tag, Ingredient, Recipe, Favorite)


class UserAdmin(admin.ModelAdmin):
    list_display = ('pk',
                    'role',
                    'username',
                    'password',
                    'email',
                    'first_name',
                    'last_name'
                    )
    search_fields = ('username',)
    list_filter = ('username', 'email')
    list_editable = ('password',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Follow)
admin.site.register(Favorite)