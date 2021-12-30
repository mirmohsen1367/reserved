from rest_framework import serializers
from room.models import Province, County, Hotel, Room, Cuser, OwnerProfile, CustomerProfile


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = "__all__"


class CountySerializer(serializers.ModelSerializer):

    class Meta:
        model = County
        fields = "__all__"

    def to_representation(self, instance):
        response = super(CountySerializer, self).to_representation(instance)
        response["province"] = ProvinceSerializer(instance.province).data
        return response


class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = ("name", "address", "phone_number", "county", "rating",
                  "owner_profile", "rooms", "id", "cover_link")


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ('room_no', 'room_type', 'no_of_beds', 'hotel', "id")

    def to_representation(self, instance):
        response = super(RoomSerializer, self).to_representation(instance)
        response["room_type"] = instance.get_room_type_display()
        response["hotel"] = HotelSerializer(instance.hotel).data
        return response


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Cuser
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
                  'full_name', 'email', 'mobile')


class OwnerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = OwnerProfile
        fields = ("id", 'address', 'national_code', 'postal_code', 'user')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = Cuser.objects.create_user(**user_data)
        return OwnerProfile.objects.create(**validated_data, user=user)


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CustomerProfile
        fields = ("id", "address", "national_code", "postal_code", "user")

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = Cuser.objects.create_user(**user_data)
        return CustomerProfile.objects.create(**validated_data, user=user)
