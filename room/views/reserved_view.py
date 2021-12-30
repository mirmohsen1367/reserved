
from rest_framework import status
from rest_framework import viewsets
from room.models import Reserved, CustomerProfile
from room.serializer.reserve_serializer import ReserveSerializer
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


class ReserveView(viewsets.ModelViewSet):
    '''
    this class for create reserve by customer
    '''
    queryset = Reserved.objects.all()
    serializer_class = ReserveSerializer

    def perform_create(self, serializer):
        try:
            customer = self.request.data.pop("customer")
            customer_profile = CustomerProfile.objects.get(pk=customer)
            serializer.save(customer=customer_profile)
        except ObjectDoesNotExist:
            return Response({"message" "objects does not exsist"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        '''
            this method for create reserved hotels
        '''
        serializer = ReserveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Reserved(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


