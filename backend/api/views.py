# from django.shortcuts import get_object_or_404
from rest_framework import viewsets
# from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    Simple model view set (testing)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    # def list(self, request):
    #     serializer = UserSerializer(self.queryset, many=True)
    #     return Response(serializer.data)
    
    # def retrieve(self, request, pk=None):
    #     # queryset = User.objects.all()
    #     user = get_object_or_404(self.queryset, pk=pk)
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)
        