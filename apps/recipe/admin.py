from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import (
    Recipe, RateRecipe, Category, Tag, RecipeIngredient,
    RecipeProcedure, Comment, CommentLike, RecipeSaved
)


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    list_display = ['id', 'name', 'recipe_count']
    search_fields = ['name']

    def recipe_count(self, obj):
        return obj.recipes.count()

    recipe_count.short_description = 'Recipe count'


class RecipeIngredientInlineModel(admin.TabularInline):
    model = RecipeIngredient
    fields = ['ingredient_title', 'ingredient_image']
    can_delete = False


class RecipeProcedureInlineModel(admin.TabularInline):
    model = RecipeProcedure
    fields = ['step', 'description']
    can_delete = False


@admin.register(Recipe)
class RecipeAdmin(ImportExportModelAdmin):
    fields = ['user', 'title', 'category', 'time_minutes', 'image' , 'video']
    list_display = ['title', 'category']
    list_filter = ['category',]
    search_fields = ['title', 'category__name']
    inlines = [RecipeIngredientInlineModel, RecipeProcedureInlineModel]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(ImportExportModelAdmin):
    list_display = ['ingredient_title', 'recipe']


@admin.register(RecipeProcedure)
class RecipeIngredientAdmin(ImportExportModelAdmin):
    list_display = ['step', 'recipe']


admin.site.register(RateRecipe)
admin.site.register(Tag)
admin.site.register(CommentLike)
admin.site.register(Comment)
admin.site.register(RecipeSaved)
