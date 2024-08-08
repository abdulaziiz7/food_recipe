from django_filters import FilterSet, filters

from apps.recipe.models import Recipe


class RecipeFilter(FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='iexact')
    rate = filters.NumberFilter(field_name='rates__rate', lookup_expr='exact')

    class Meta:
        model = Recipe
        fields = ['category', 'rate']
