from django.urls import path

from .views import (
    recipe_list, recipe_category,
    recipe_comment_create, recipe_comment_list,
    recipe_comment_delete,
    recipe_list_for_user, saved_recipe, recipe_create, recipe_update, rate_recipe, like_dislike_comment, recipe_delete
)
app_name = 'recipe_api'

urlpatterns = [
    path('recipe_list_for_user/', recipe_list_for_user, name='recipe_list_for_user'),
    path('saved-recipe/<int:pk>', saved_recipe, name='saved_recipe'),
    path('recipe-create/', recipe_create, name='recipe_create'),
    path('recipe-update/<int:pk>', recipe_update, name='recipe_update'),
    path('recipe-list/', recipe_list, name='recipe_list'),
    path('recipe-category/', recipe_category, name='recipe_category'),
    path('recipe-rate/<int:pk>', rate_recipe, name='rate_recipe'),
    path('recipe_list_for_user/', recipe_list_for_user, name='recipe_list_for_user'),
    path('recipe-comment-create/', recipe_comment_create, name='recipe_comment-create'),
    path('recipe-comment-list/', recipe_comment_list, name='recipe_comment-list'),
    path('recipe-comment-delete/<int:pk>', recipe_comment_delete, name='recipe_comment-delete'),
    path('like-dislike-comment/<int:pk>', like_dislike_comment, name='like-dislike-comment'),
    path('rate-recipe/<int:pk>', rate_recipe, name='rate_recipe'),
    path('recipe-delete/<int:pk>', recipe_delete, name='recipe_delete'),
]
