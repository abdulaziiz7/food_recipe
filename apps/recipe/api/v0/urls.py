from django.urls import path
from .views import recipe_list, recipe_category, recipe_comment_create, recipe_comment_list, recipe_comment_delete, \
    like_dislike_comment

app_name = 'recipe_api'

urlpatterns = [
    path('recipe-list/', recipe_list, name='recipe-list'),
    path('recipe-category/', recipe_category, name='recipe-category'),
    path('recipe-comment-create/', recipe_comment_create, name='recipe-comment-create'),
    path('recipe-comment-list/', recipe_comment_list, name='recipe-comment-list'),
    path('recipe-comment-delete/<int:pk>', recipe_comment_delete, name='recipe-comment-delete'),
    path('like-dislike-comment/<int:pk>', like_dislike_comment , name='like-dislike-comment'),


]