from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .serializers import UserSerializer


class RegisterUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer
