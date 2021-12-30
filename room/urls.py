
from rest_framework import routers
from room.views.admin_manager_view import AdminSettingCounty, AdminSettingProvince, AdminSettingUsers
from room.views.hotel_view import OwnerHotelView
from room.views.reports import HotelsReportView
from room.views.reserved_view import ReserveView

room_routers = routers.DefaultRouter()
room_routers.register(r'admin/province', viewset=AdminSettingProvince, basename='admin/province')
room_routers.register(r'admin/county', viewset=AdminSettingCounty, basename='admin/county')
room_routers.register(r'admin/users', viewset=AdminSettingUsers, basename='admin/users')
room_routers.register(r'owner', viewset=OwnerHotelView, basename='owner')
room_routers.register(r'reserved', viewset=ReserveView, basename='reserved')
room_routers.register(r'reserved/reports', viewset=HotelsReportView, basename='reserved/reports')
