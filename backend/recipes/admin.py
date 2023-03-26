from django.contrib import admin
from users.models import User, Follow
from .models import (Tag, Ingredient, Recipe,
                     Favorite, ShoppingCart, RecipeIngredient)


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


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through


class RecipeOptions(admin.ModelAdmin):
    inlines = [RecipeIngredientInline, ]
    min_num = 1


admin.site.register(User, UserAdmin)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(Recipe, RecipeOptions)
admin.site.register(RecipeIngredient)
admin.site.register(Follow)
admin.site.register(Favorite)
admin.site.register(ShoppingCart)