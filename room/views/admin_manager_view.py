
from room.serializer.admin_setting_serializer import CountySerializer,\
                                                     ProvinceSerializer, OwnerProfileSerializer, CustomerSerializer
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from room.models import County, Province, OwnerProfile, CustomerProfile
from rest_framework.decorators import action
from room.pagination import CustomPagination


class AdminSettingCounty(viewsets.ModelViewSet):
    '''
    this class for create county or update or delete by admin
    '''

    queryset = County.objects.all()
    serializer_class = CountySerializer
    pagination_class = CustomPagination


class AdminSettingProvince(viewsets.ModelViewSet):
    '''
    this class viewset for create or update or delete province by admin
    '''
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    pagination_class = CustomPagination


class AdminSettingUsers(viewsets.ModelViewSet):
    '''
    admin can create and update and delete users
    users include customer or owner
    '''
    queryset = OwnerProfile.objects.all()
    serializer_class = OwnerProfileSerializer
    pagination_class = CustomPagination

    @action(methods=['get', 'post', 'patch', 'delete'], detail=True)
    def customer_profile(self, request, pk):
        '''
            this method for create and update delete or get
            customers users
        '''
        if request.method == "POST":
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "GEt":
            if pk == "0":
                self.queryset = CustomerProfile.objects.all()
                serializer = CustomerSerializer(self.queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            self.queryset = get_object_or_404(CustomerProfile, pk=pk)
            serializer = CustomerSerializer(self.queryset)
            return Response(serializer.data, status=status.HTTP_200_OK)

        if request.method == "PATCH":
            self.queryset = get_object_or_404(CustomerProfile, pk=pk)
            serializer = CustomerSerializer(self.queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if request.method == 'DELETE':
            self.queryset = get_object_or_404(CustomerProfile, pk=pk)
            self.queryset.delete()
            return Response({"message": "deleted"}, status=status.HTTP_200_OK)
