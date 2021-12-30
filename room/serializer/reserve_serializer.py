
from rest_framework import serializers
from room.models import Reserved
from django.db.models import Q
from room.serializer.admin_setting_serializer import CustomerSerializer


class ReserveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserved
        fields = ("id", "room", "from_date", "to_date", "customer")

    def validate(self, attrs):
        '''
            check if room is rserved rais exceptions
        '''
        if attrs['from_date'] > attrs['to_date']:
            raise serializers.ValidationError("to_date must occur after from_date")

        reserved = Reserved.objects.\
            filter(Q(room=attrs["room"], from_date__range=(attrs["from_date"], attrs["to_date"]))|
                   Q(room=attrs["room"], to_date__range=(attrs["from_date"], attrs["to_date"])))

        if reserved:
            raise serializers.ValidationError("this date is reserved")

        return attrs

    def to_representation(self, instance):
        response = super(ReserveSerializer, self).to_representation(instance)
        response["customer"] = CustomerSerializer(instance.customer).data
        return response

    def create(self, validated_data):
        return Reserved.objects.create(**validated_data)