from django.db.models import Avg
from rest_framework import serializers

from apps.recipe.models import Comment, Category, Tag, Recipe
from apps.recipe.models import RateRecipe, CommentLike
from apps.user.api.v0.serializers import UserSerializer


class RateRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateRecipe
        fields = ['rate']


class RecipeListSerializer(serializers.ModelSerializer):
    rates = RateRecipeSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'image', 'rates', 'user']

    def to_representation(self, instance):
        tr = super().to_representation(instance)
        tr['rate'] = instance.rates.aggregate(avg=Avg('rate'))['avg'] or 0
        return tr


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


class CreateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ['category', 'title', 'time_minutes', 'image', 'video', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for tag in tags_data:
            recipe.tags.add(tag)

        return recipe


class RecipeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'video', 'time_minutes']


class RecipeDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
