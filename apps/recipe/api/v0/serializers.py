from rest_framework import serializers
from apps.recipe.models import Recipe, Category, RateRecipe, Comment, CommentLike


class RateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateRecipe
        fields = ['recipe', 'rate']


class RecipeListSerializer(serializers.ModelSerializer):
    rate = RateRecipeSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'rate']


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'text', 'created_at']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id', 'comment', 'liked', 'disliked', 'created_at']


class CommentLikeSerializer(serializers.Serializer):
    liked = serializers.IntegerField()

    def validate(self, attrs):
        if not (attrs['liked'] == '1' or attrs['liked'] == '0'):
            raise ValueError('liked must be 0 or 1')
        return attrs


