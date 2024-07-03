from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=100)
    description = models.TextField()
    time_minutes = models.IntegerField()
    rating = models.IntegerField(default=0)
    image = models.ImageField(upload_to='recipes/')
    video = models.FileField(upload_to='recipes/', null=True, blank=True)
    saved = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


class RateRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rates')
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.rate


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient_image = models.ImageField(upload_to='recipes/')
    ingredient_title = models.CharField(max_length=100)
    procedure = models.JSONField(default=dict)

    def __str__(self):
        return self.recipe.title


class RecipeProcedure(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    order = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.recipe.title


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" {self.id} {self.text}"


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
