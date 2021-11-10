from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import IncomeSerializer
from .models import Income
from rest_framework import permissions
from .permissions import IsOwner
from  rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status


# class IncomeListAPIView(ListCreateAPIView):
class IncomeViewSet(ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        try:
            
            return self.queryset.filter(owner=self.request.user)
        except:
            return Response({
                'status': 'error',
                'message':' You need to be authenticated to access this page'
            }, status= status.HTTP_401_UNAUTHORIZED) 