from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView, DestroyAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.recipe.api.v0.filters import RecipeFilter
from apps.recipe.api.v0.permissions import IsOwner
from apps.recipe.api.v0.serializers import RecipeCreateSerializer, RecipeUpdateSerializer, RecipeListSerializer, \
    CategoryListSerializer, RateRecipeSerializer, CommentSerializer, CommentLikeSerializer, LikeSerializer
from apps.recipe.models import Recipe, Category, RateRecipe, Comment, CommentLike


class RecipeCreateAPIView(CreateAPIView):
    serializer_class = RecipeCreateSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RecipeUpdateAPIView(UpdateAPIView):
    serializer_class = RecipeUpdateSerializer
    queryset = Recipe.objects.all()
    permission_classes = [IsOwner]

    # lookup_field = 'id'

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class RecipeDeleteAPIView(DestroyAPIView):
    permission_classes = [IsOwner]

    def get_object(self):
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj


class RecipeListAPIView(ListAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (OrderingFilter,)
    filterset_class = RecipeFilter
    ordering_fields = ['created_at']



class CategoryListAPIView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class RateRecipeAPIView(ListAPIView):
    queryset = RateRecipe.objects.all()
    serializer_class = RateRecipeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        recipe_id = self.kwargs['recipe']
        return RateRecipe.objects.filter(recipe_id=recipe_id)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def delete(self, request, *args, **kwargs):
        comment = self.get_object()
        self.check_object_permissions(self.request, comment)
        comment.delete()
        return Response(f"{comment.user} deleted successfully.", status=status.HTTP_200_OK)


class LikeCommentAPIView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        data = CommentLikeSerializer(request.data).__getitem__('liked').value
        commit = get_object_or_404(Comment, pk=pk)
        like_comment, created = CommentLike.objects.get_or_create(comment=commit, user=1)
        if data == 1:
            if like_comment.liked is True and like_comment.disliked is False:
                like_comment.liked = False
            else:
                like_comment.liked = True
                like_comment.disliked = False
            like_comment.save()
            serializer = LikeSerializer(like_comment)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if data == 0:
            if like_comment.disliked is True and like_comment.liked is False:
                like_comment.disliked = False
                like_comment.liked = True
            else:
                like_comment.disliked = True
                like_comment.liked = False

            like_comment.save()

            serializer = LikeSerializer(like_comment)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(f"{like_comment.user} Not Liked.", status=status.HTTP_400_BAD_REQUEST)


recipe_create = RecipeCreateAPIView.as_view()
recipe_list = RecipeListAPIView.as_view()
recipe_update = RecipeUpdateAPIView.as_view()
recipe_category = CategoryListAPIView.as_view()
recipe_delete = RecipeDeleteAPIView.as_view()
recipe_comment_create = CommentCreateAPIView.as_view()
recipe_comment_list = CommentListAPIView.as_view()
recipe_comment_delete = CommentDeleteAPIView.as_view()
like_dislike_comment = LikeCommentAPIView.as_view()
rate_recipe = RateRecipeAPIView.as_view()
