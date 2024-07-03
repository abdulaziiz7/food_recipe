from django.urls import path

from apps.recipe.api.v0.views import recipe_create, recipe_list, recipe_update, recipe_delete

urlpatterns = [
    path('recipe-create/', recipe_create, name='recipe_create'),
    path('recipe-list/', recipe_list, name='recipe_list'),
    path('recipe-update/<int:pk>', recipe_update, name='recipe_update'),
    path('recipe-delete/<int:pk>', recipe_delete, name='recipe_delete'),
]