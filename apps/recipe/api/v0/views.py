from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.recipe.api.v0.permissions import IsOwner
from apps.recipe.api.v0.serializers import RecipeCreateSerializer, RecipeUpdateSerializer, RecipeListSerializer
from apps.recipe.models import Recipe


class RecipeCreateAPIView(CreateAPIView):
    serializer_class = RecipeCreateSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


recipe_create = RecipeCreateAPIView.as_view()


class RecipeUpdateAPIView(UpdateAPIView):
    serializer_class = RecipeUpdateSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsOwner]

    # lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


recipe_update = RecipeUpdateAPIView.as_view()


class RecipeListAPIView(ListAPIView):
    serializer_class = RecipeListSerializer
    queryset = Recipe.objects.all()


recipe_list = RecipeListAPIView.as_view()


class RecipeDeleteAPIView(DestroyAPIView):
    permission_classes = [IsOwner]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


recipe_delete = RecipeDeleteAPIView.as_view()


