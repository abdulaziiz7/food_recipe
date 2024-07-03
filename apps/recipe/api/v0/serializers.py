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


