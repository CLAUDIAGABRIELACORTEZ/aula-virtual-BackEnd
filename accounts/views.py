from rest_framework import viewsets
from .models import CustomUser
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from accounts.permissions import IsDirector
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsDirector
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
#     permission_classes = [IsAuthenticated, IsDirector]

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return []  # Permitir crear usuarios sin autenticación
        return [IsAuthenticated(), IsDirector()]
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class VistaSoloDirector(APIView):
    permission_classes = [IsAuthenticated, IsDirector]

    def get(self, request):
        return Response({
            "mensaje": f"Hola {request.user.nombre}, tienes acceso porque eres director.",
            "usuario": request.user.email,
            "rol": request.user.rol
        })


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)