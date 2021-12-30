
from rest_framework.response import Response
from room.filters import ReservedFilter
from room.models import Reserved, Hotel
from rest_framework.viewsets import ModelViewSet
from room.serializer.reserve_serializer import ReserveSerializer
from rest_framework.decorators import action
from rest_framework import status
from django.shortcuts import render


class HotelsReportView(ModelViewSet):
    queryset = Reserved.objects.all()
    serializer_class = ReserveSerializer

    @action(methods=["get"], detail=True)
    def reports(self, request, pk):
        '''
        this method for reports of hotels rooms and response of browser
        :param request: data params from_date and to_date params is filtering
        '''
        hotel = Hotel.objects.get(pk=pk)
        reserved = Reserved.objects.filter(room__hotel_id=hotel.id)
        if reserved:
            if request.GET:
                reserved = ReservedFilter(data=request.GET, queryset=reserved).qs
                context = {'reserved': reserved}
                return render(request, 'hotel_reports.html', context)
            context = {'reserved': reserved}
            return render(request, 'hotel_reports.html', context)
        return Response({"message": "this hotel rooms not reserved"}, status=status.HTTP_400_BAD_REQUEST)
