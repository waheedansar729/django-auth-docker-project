from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # Sirf wohi user access kar sakega jo logged-in hoga (Day 6 Auth & Permissions)
    permission_classes = [IsAuthenticated]