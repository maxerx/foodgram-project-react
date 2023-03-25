from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet,
                       TagViewSet, UsersViewSet)

app_name = 'api'

router = DefaultRouter()
router.register(r'tags', TagViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'ingredients', IngredientViewSet)
router.register(r'users', UsersViewSet)

extra_patterns = [
    path('auth/', include('djoser.urls.authtoken'))
]

urlpatterns = [
    path('', include(extra_patterns)),
    path('', include(router.urls))
]
