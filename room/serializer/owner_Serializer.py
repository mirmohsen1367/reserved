
from rest_framework import serializers
from room.models import Hotel, Room
from room.serializer.admin_setting_serializer import CountySerializer, OwnerProfileSerializer


class RoomSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)

    class Meta:
        model = Room
        fields = ("id", "room_no", "room_type", "no_of_beds")


class HotelSerializer(serializers.ModelSerializer):
    '''
    owner create self hotels
    '''
    owner_profile = OwnerProfileSerializer(read_only=True)
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Hotel
        fields = ("name", "address", "phone_number", "county", "rating",
                  "owner_profile", "rooms", "id", "cover_link")

    def create(self, validated_data):
        rooms_data = validated_data.pop('rooms')
        hotel = Hotel.objects.create(**validated_data)
        for room_data in rooms_data:
            Room.objects.create(**room_data, hotel=hotel)
        return hotel

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.county = validated_data.get('county', instance.county)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.save()
        rooms_item = validated_data.get('rooms')
        for room_item in rooms_item:
            room_id = room_item.get('id', None)
            if room_id:
                ins_room = Room.objects.get(id=room_id, hotel=instance)
                ins_room.room_no = room_item.get("room_no", ins_room.room_no)
                ins_room.room_type = room_item.get("room_type", ins_room.room_type)
                ins_room.no_of_beds = room_item.get("no_of_beds", ins_room.no_of_beds)
                ins_room.save()
            else:
                Room.objects.create(hotel=instance, **room_item)

        return instance

    def to_representation(self, instance):
        response = super(HotelSerializer, self).to_representation(instance)
        response['county'] = CountySerializer(instance.county).data
        return response
