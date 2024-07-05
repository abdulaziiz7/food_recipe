from django.contrib import admin
from .models import Recipe, RateRecipe, Category, Tag, RecipeIngredient, RecipeProcedure, Comment, CommentLike

admin.site.register([Recipe, RateRecipe, Category, Tag, RecipeIngredient, RecipeProcedure, Comment, CommentLike])