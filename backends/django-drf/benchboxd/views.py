from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["POST"])
def reset(request):
    User.objects.all().delete()
    return Response(None, status=status.HTTP_204_NO_CONTENT)
