from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

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
    time_minutes = models.IntegerField()
    image = models.ImageField(upload_to='recipes/images/')
    video = models.FileField(upload_to='recipes/videos/', null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class RecipeSaved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='saved')

    class Meta:
        verbose_name = "Recipe saved"
        verbose_name_plural = "Recipes saved"

    def __str__(self):
        return self.recipe.title


class RateRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rates')
    rate = models.IntegerField(default=0)

    def __str__(self):
        return str(self.rate)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient_image = models.ImageField(upload_to='recipes/')
    ingredient_title = models.CharField(max_length=100)
    procedure = models.JSONField(default=dict)

    def __str__(self):
        return self.recipe.title


class RecipeProcedure(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    step = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.recipe.title


class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
