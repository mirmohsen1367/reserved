from django.contrib import admin
from room.models import Cuser, County, Province, Hotel, Room, Reserved, CustomerProfile, \
                        OwnerProfile
from django.contrib.auth.admin import UserAdmin


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_display_links = ('name',)
    list_filter = ("name",)
    search_fields = ("name",)


@admin.register(County)
class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'province_id')
    list_filter = ('name',)
    list_display_links = ('name',)
    search_fields = ('name', )


@admin.register(Hotel)
class HolteAdmin(admin.ModelAdmin):
    list_display = ('name',  'address', 'phone_number', 'county', 'rating', 'owner_profile_id')
    list_display_links = ('name',)
    list_filter = ("name", 'county__name')
    search_fields = ("name",)
    fieldsets = ((None, {'fields': ("name", "address", 'county', 'rating')}),
                 ('owner', {'fields': ('owner_profile',)}))


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no', 'room_type', 'no_of_beds', 'hotel_id')
    list_display_links = ('hotel_id',)
    list_filter = ('hotel__name',)
    search_fields = ('hotel__name',)


@admin.register(Reserved)
class ReservedAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'room_id', 'from_date', 'to_date')
    list_filter = ('from_date', 'to_date')
    search_fields = ('from_date', 'to_date')


@admin.register(CustomerProfile)
class CustomerProfiledmin(admin.ModelAdmin):
    list_display = ('address', 'national_code', 'postal_code', 'user_id')
    list_filter = ('national_code',)
    search_fields = ('national_code',)


@admin.register(OwnerProfile)
class OwnerProfiledmin(admin.ModelAdmin):
    list_display = ('address', 'national_code', 'postal_code', 'user_id')
    list_filter = ('national_code',)
    search_fields = ('national_code',)


@admin.register(Cuser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'password', 'first_name', 'last_name', 'full_name',
                    'email', 'mobile']
    list_display_links = ('username',)
    list_filter = ('username', 'mobile')
    search_fields = ('username', 'mobile')
