
from rest_framework import viewsets
from room.models import Hotel, Cuser, OwnerProfile, Room
from room.serializer.owner_Serializer import HotelSerializer, RoomSerializer
from rest_framework.response import Response
from rest_framework import status
from room.pagination import CustomPagination
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist
from django_filters import rest_framework as filters
from room.filters import HotelFilter, ReservedFilter
from room.serializer.reserve_serializer import ReserveSerializer


class OwnerHotelView(viewsets.ModelViewSet):
    """
    this end point for only owner or admin create hotel for reservrd
    """
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = HotelFilter

    def perform_create(self, serializer):
        owner_profile =self.request.data.pop('owner_profile')
        owner = OwnerProfile.objects.get(pk=owner_profile)
        serializer.save(owner_profile=owner)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def list_hotels(self):
        '''
            list of hotels paginations the curtomer and owner and admin can see
        '''

        page = self.paginate_queryset(self.queryset)
        if page is not None:
            response = self.get_paginated_response(HotelSerializer(page, many=True).data).data
        else:
            response = HotelSerializer(self.queryset, many=True).data
        return (response, "200")

    @action(methods=["POST"], detail=False)
    def room_filter(self, request):
        '''
            this method for filter of hotels by post method
            the filter data posted
            can see by customer and owner and so admin
        '''

        if request.data:
            self.queryset = HotelFilter(data=request.data, queryset=self.queryset).qs
            result = self.list_hotels(self)
            return Response(result[0], status=result[1])

        result = self.list_hotels(self)
        return Response(result[0], status=result[1])

    @action(methods=["delete", "patch"], detail=True)
    def room_actions(self, request, pk):
        '''
            this method for delete room of hotel or patch
            can by admin or owner
        '''
        if request.method == "PATCH":
            try:
                obj = Room.objects.get(pk=pk)
                serializer = RoomSerializer(obj, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except ObjectDoesNotExist:
                return Response({"message": "object does not exsist"}, status=status.HTTP_400_BAD_REQUEST)

        if request.method == "DELETE":
            # can action by admin or owner
            try:
                obj = Room.objects.get(pk=pk)
                obj.delete()
                return Response({"message": "deleted"}, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response({"message": "object does not exsist"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=True)
    def reserved_room_filter(self, request, pk):
        '''
            this method for informations reserved room
            and filter data posted to filtering
        '''
        try:
            obj = Room.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"message": "object does not exsist"}, status=status.HTTP_404_NOT_FOUND)
        reserved = obj.reserveds.all()
        if request.data:
            reserved = ReservedFilter(data=request.data, queryset=reserved).qs
            if reserved:
                page = self.paginate_queryset(reserved)
                if page is not None:
                    response = self.get_paginated_response(ReserveSerializer(page, many=True).data).data
                else:
                    response = ReserveSerializer(reserved, many=True).data
                return Response(response, status=status.HTTP_200_OK)
        page = self.paginate_queryset(reserved)
        if page is not None:
            response = self.get_paginated_response(ReserveSerializer(page, many=True).data).data
        else:
            response = ReserveSerializer(reserved, many=True).data
        return Response(response, status=status.HTTP_200_OK)

