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


from rest_framework import serializers

from apps.recipe.models import Comment, Category, Tag, Recipe


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class RecipeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['category', 'title', 'description', 'time_minutes', 'image', 'video']

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            tag, created = Tag.objects.get_or_create(**tag)
            recipe.tags.add(tag)

        return recipe


class RecipeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'time_minutes']


class RecipeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'


